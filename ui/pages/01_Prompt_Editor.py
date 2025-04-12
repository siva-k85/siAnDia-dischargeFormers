"""
Prompt editor page for modifying discharge summary templates.
"""

import streamlit as st
import sys
from pathlib import Path
import json

# Add the parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from llm.prompt_templates import TEMPLATE_MAP
from llm.discharge_generator import DischargeSummaryGenerator
from llm.utils import load_patient_data
import config


st.set_page_config(page_title="Prompt Editor", page_icon="📝", layout="wide")

st.title("Prompt Template Editor")
st.markdown("View and edit prompt templates to customize discharge summary generation")


def main():
    # Initialize state
    if "edited_templates" not in st.session_state:
        st.session_state.edited_templates = {
            key: value for key, value in TEMPLATE_MAP.items()
        }

    if "current_patient_data" not in st.session_state:
        st.session_state.current_patient_data = None

    if "comparison_output" not in st.session_state:
        st.session_state.comparison_output = {}

    # Sidebar controls
    with st.sidebar:
        st.header("Controls")

        # Template selection
        template_name = st.selectbox(
            "Select Template to Edit", options=list(TEMPLATE_MAP.keys())
        )

        # Load patient data for testing
        st.subheader("Patient Data for Testing")
        example_files = []
        data_dir = Path(config.DATA_DIR)
        if data_dir.exists():
            example_files = [f for f in data_dir.glob("*.json") if f.is_file()]

        if example_files:
            selected_file = st.selectbox(
                "Select patient data",
                options=example_files,
                format_func=lambda x: x.name,
            )

            if st.button("Load Patient Data"):
                try:
                    st.session_state.current_patient_data = load_patient_data(
                        selected_file
                    )
                    st.success(f"Loaded patient data: {selected_file.name}")
                except Exception as e:
                    st.error(f"Error loading data: {str(e)}")
        else:
            st.warning("No example files found in the data directory.")

        # API key and model selection
        api_key = st.text_input(
            "OpenAI API Key", value=config.OPENAI_API_KEY, type="password"
        )

        model = st.selectbox(
            "LLM Model", ["gpt-4", "gpt-4.5-preview", "gpt-3.5-turbo"], index=0
        )

        # Compare button
        if st.session_state.current_patient_data:
            if st.button("Compare Outputs"):
                with st.spinner("Generating comparison..."):
                    try:
                        generator = DischargeSummaryGenerator(
                            api_key=api_key, model=model
                        )

                        # Generate summary with original template
                        original_summary = generator.generate_summary(
                            st.session_state.current_patient_data,
                            template_type=template_name,
                        )

                        # Override template temporarily for comparison
                        temp_template = st.session_state.edited_templates[template_name]
                        TEMPLATE_MAP[template_name] = temp_template

                        # Generate with edited template
                        edited_summary = generator.generate_summary(
                            st.session_state.current_patient_data,
                            template_type=template_name,
                        )

                        # Restore original template
                        TEMPLATE_MAP[template_name] = TEMPLATE_MAP[template_name]

                        # Store results
                        st.session_state.comparison_output = {
                            "original": original_summary,
                            "edited": edited_summary,
                        }

                    except Exception as e:
                        st.error(f"Error generating comparison: {str(e)}")

    # Main content area
    st.subheader(f"Editing Template: {template_name}")

    # Display and edit current template
    current_template = st.session_state.edited_templates[template_name]
    edited_template = st.text_area("Edit Template", value=current_template, height=400)

    if edited_template != current_template:
        st.session_state.edited_templates[template_name] = edited_template
        st.success("Template updated! Click 'Compare Outputs' to see the effect.")

    # Reset button
    if st.button("Reset to Original"):
        st.session_state.edited_templates[template_name] = TEMPLATE_MAP[template_name]
        st.success("Template reset to original")

    # Display comparison outputs if available
    if "comparison_output" in st.session_state and st.session_state.comparison_output:
        st.header("Output Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Template Output")
            st.markdown(st.session_state.comparison_output["original"])

        with col2:
            st.subheader("Edited Template Output")
            st.markdown(st.session_state.comparison_output["edited"])

    st.markdown("---")
    st.caption(
        "Note: Changes made here are temporary and will reset when the application restarts."
    )


if __name__ == "__main__":
    main()
