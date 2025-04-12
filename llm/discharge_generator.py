"""
Core functionality for generating discharge summaries using LLMs.
"""

import json
import openai
from openai import OpenAI
from loguru import logger

from . import prompt_templates
from . import utils
from config import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE, MAX_TOKENS


class DischargeSummaryGenerator:
    """
    Generates discharge summaries using OpenAI's GPT models.
    """

    def __init__(self, api_key=OPENAI_API_KEY, model=LLM_MODEL):
        """Initialize the generator with API credentials."""
        self.client = OpenAI(api_key=api_key)
        self.model = model
        logger.info(f"Initialized DischargeSummaryGenerator with model: {model}")

    def _prepare_prompt(self, patient_data, template_type=None):
        """
        Prepare a prompt for the LLM based on patient data.

        Args:
            patient_data (dict): Patient data dictionary
            template_type (str, optional): Template type to use. If None, will be
                                          determined from diagnosis code.

        Returns:
            str: Formatted prompt
        """
        # Format the patient data for the prompt
        formatted_data = utils.format_patient_json(patient_data)

        # Extract patient ID for logging
        patient_id = patient_data.get("patient_id", "unknown")

        # Determine which template to use based on diagnosis or specified template
        if template_type and template_type in prompt_templates.TEMPLATE_MAP:
            template = prompt_templates.TEMPLATE_MAP[template_type]
        else:
            diagnosis_code = utils.extract_diagnosis_code(patient_data)
            template = prompt_templates.get_template_by_diagnosis(diagnosis_code)

        # Format the prompt with patient data
        prompt = template.format(patient_data=formatted_data)

        logger.debug(
            f"Prepared prompt for patient {patient_id} using template type: {template_type}"
        )
        return prompt

    def generate_summary(self, patient_data, template_type=None):
        """
        Generate a discharge summary for a patient.

        Args:
            patient_data (dict): Patient data
            template_type (str, optional): Template type to use

        Returns:
            str: Generated discharge summary
        """
        patient_id = patient_data.get("patient_id", "unknown")
        prompt = self._prepare_prompt(patient_data, template_type)

        try:
            logger.info(f"Generating discharge summary for patient: {patient_id}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical professional creating discharge summaries.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=LLM_TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )

            summary = response.choices[0].message.content

            # Sanitize output
            summary = utils.sanitize_output(summary)

            # Log the interaction (with privacy considerations)
            utils.log_prompt_and_response(prompt, summary, patient_id)

            return summary

        except Exception as e:
            logger.error(f"Error generating summary for patient {patient_id}: {str(e)}")
            raise

    def generate_summary_from_file(self, file_path, template_type=None):
        """
        Generate a discharge summary from a patient data file.

        Args:
            file_path (str): Path to patient data JSON file
            template_type (str, optional): Template type to use

        Returns:
            str: Generated discharge summary
        """
        try:
            patient_data = utils.load_patient_data(file_path)
            return self.generate_summary(patient_data, template_type)
        except Exception as e:
            logger.error(f"Error generating summary from file {file_path}: {str(e)}")
            raise
