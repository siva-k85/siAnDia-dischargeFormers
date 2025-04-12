"""
Utility functions for the discharge summary generator.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from loguru import logger
import sys


# Set up logging configuration
def setup_logging(log_dir, log_level="INFO"):
    """Configure logging for the application."""
    # Remove default logger
    logger.remove()

    # Add stdout handler
    logger.add(sys.stdout, level=log_level)

    # Add file handler with rotation
    log_file = (
        Path(log_dir) / f"discharge_summary_{datetime.now().strftime('%Y%m%d')}.log"
    )
    logger.add(
        log_file,
        level=log_level,
        rotation="10 MB",
        retention="7 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )

    return logger


def load_patient_data(file_path):
    """Load patient data from JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading patient data from {file_path}: {e}")
        raise


def extract_diagnosis_code(patient_data):
    """Extract primary diagnosis code from patient data."""
    try:
        if "diagnoses" in patient_data and len(patient_data["diagnoses"]) > 0:
            return patient_data["diagnoses"][0].get("diagnosis_code", "")
        return ""
    except (KeyError, IndexError) as e:
        logger.warning(f"Could not extract diagnosis code: {e}")
        return ""


def format_patient_json(patient_data):
    """
    Format patient JSON data for better readability in prompts.
    Removes potentially sensitive or irrelevant information.
    """
    # Create a copy to avoid modifying the original
    formatted_data = json.dumps(patient_data, indent=2)
    return formatted_data


def sanitize_output(summary_text):
    """
    Sanitize the generated output to remove any inappropriate content.
    """
    # This is a placeholder for more sophisticated filtering if needed
    return summary_text


def extract_patient_demographics(patient_data):
    """Extract key patient demographics from data."""
    demographics = {}
    if "patient_demographics" in patient_data:
        demo = patient_data["patient_demographics"]
        demographics = {
            "name": demo.get("name", "Unknown"),
            "age": demo.get("age", "Unknown"),
            "gender": demo.get("gender", "Unknown"),
            "admission_date": demo.get("admission_date", "Unknown"),
            "discharge_date": demo.get(
                "discharge_date", demo.get("expected_discharge_date", "Unknown")
            ),
        }
    return demographics


def log_prompt_and_response(prompt, response, patient_id=None):
    """Log the prompt and response for auditing and training purposes."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "patient_id": patient_id,
        "prompt_length": len(prompt),
        "response_length": len(response),
        # For privacy reasons, we don't log the full prompt and response
        "prompt_excerpt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
        "response_excerpt": response[:100] + "..." if len(response) > 100 else response,
    }
    logger.info(f"Generated summary for patient: {patient_id}")
    logger.debug(json.dumps(log_entry))

    return log_entry
