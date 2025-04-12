"""
Streamlit web interface for the discharge summary generator.
"""

import streamlit as st
import json
import pandas as pd
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm.discharge_generator import DischargeSummaryGenerator
from llm.prompt_templates import TEMPLATE_MAP
import config


def load_example_files():
    """Load example patient data files from the data directory."""
    data_dir = Path(config.DATA_DIR)
    if not data_dir.exists():
        return []

    return [f for f in data_dir.glob("*.json") if f.is_file()]


def show_patient_overview(patient_data):
    """Display an overview of patient information."""
    if not patient_data:
        return

    try:
        # Patient demographics
        demo = patient_data.get("patient_demographics", {})
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Patient Information")
            st.write(f"**Name:** {demo.get('name', 'N/A')}")
            st.write(f"**Patient ID:** {patient_data.get('patient_id', 'N/A')}")
            st.write(f"**Age:** {demo.get('age', 'N/A')}")
            st.write(f"**Gender:** {demo.get('gender', 'N/A')}")

        with col2:
            st.subheader("Admission Details")
            st.write(f"**Admission Date:** {demo.get('admission_date', 'N/A')}")
            discharge_date = demo.get(
                "discharge_date", demo.get("expected_discharge_date", "N/A")
            )
            st.write(f"**Discharge Date:** {discharge_date}")

            # Display diagnosis if available
            if "diagnoses" in patient_data and len(patient_data["diagnoses"]) > 0:
                diagnosis = patient_data["diagnoses"][0]
                st.write(
                    f"**Primary Diagnosis:** {diagnosis.get('description', 'N/A')}"
                )
                st.write(f"**ICD Code:** {diagnosis.get('diagnosis_code', 'N/A')}")

        # Show a preview of encounters
        if "encounters" in patient_data and len(patient_data["encounters"]) > 0:
            st.subheader("Encounters Summary")
            encounters_df = pd.DataFrame(patient_data["encounters"])
            st.dataframe(encounters_df, use_container_width=True)

        # Show medications
        if "med_orders" in patient_data and len(patient_data["med_orders"]) > 0:
            st.subheader("Medications")
            meds_df = pd.DataFrame(patient_data["med_orders"])
            st.dataframe(meds_df, use_container_width=True)

    except Exception as e:
        st.error(f"Error displaying patient overview: {str(e)}")


def main():
    st.set_page_config(page_title=config.UI_TITLE, page_icon="🏥", layout="wide")

    # Header with logo and prof pic
    header_col1, header_col2, header_col3 = st.columns([1, 2, 1])

    # CMU logo on the left
    logo_path = Path(__file__).parent / "images" / "cmu_logo.png"
    if logo_path.exists():
        header_col1.image(str(logo_path), width=350)
    else:
        header_col1.error("CMU logo not found")

    # Title in the middle
    header_col2.title(config.UI_TITLE)
    header_col2.markdown(config.UI_DESCRIPTION)

    # Professor's picture on the right (smaller)
    prof_pic_path = Path(__file__).parent / "images" / "prof_pic.png"
    if prof_pic_path.exists():
        header_col3.image(str(prof_pic_path), width=120)
    else:
        header_col3.error("Professor image not found")

    # Add a divider for visual separation
    st.divider()

    # Display group information in the sidebar
    st.sidebar.header("Project Information")
    st.sidebar.markdown(
        """
        **Group:** SiAnDia:DischargeFormers (Group 3)
        **Members:**
        - Siva Komaragiri (skomarag)
        - Anu Subramanya (ahsubram)
        - India Etheridge (ietherid)
        """
    )
    st.sidebar.divider()  # Optional: Adds a visual separator

    # Initialize session state variables if they don't exist
    if "patient_data" not in st.session_state:
        st.session_state.patient_data = None
    if "generated_summary" not in st.session_state:
        st.session_state.generated_summary = None

    # Sidebar with options
    with st.sidebar:
        st.header("Options")

        # Input method selection
        input_method = st.radio(
            "Select input method",
            ["Upload JSON", "Load Example", "Enter JSON manually"],
        )

        # Template selection
        template_options = list(TEMPLATE_MAP.keys())
        template_type = st.selectbox("Summary template", template_options, index=0)

        # API key input
        api_key = st.text_input(
            "OpenAI API Key (optional)", value=config.OPENAI_API_KEY, type="password"
        )

        # Model selection
        model = st.selectbox(
            "LLM Model", ["gpt-4", "gpt-4.5-preview", "gpt-3.5-turbo"], index=0
        )

        # Generate button (in sidebar)
        generate_button = st.button("Generate Discharge Summary", type="primary")

    # Main content area
    if input_method == "Upload JSON":
        uploaded_file = st.file_uploader("Upload patient data (JSON)", type="json")

        if uploaded_file:
            try:
                patient_data = json.load(uploaded_file)
                st.session_state.patient_data = patient_data
                st.success("Patient data loaded successfully!")
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")

    elif input_method == "Load Example":
        example_files = load_example_files()
        if example_files:
            selected_file = st.selectbox(
                "Select example patient data",
                options=example_files,
                format_func=lambda x: x.name,
            )

            if selected_file:
                try:
                    with open(selected_file) as f:
                        patient_data = json.load(f)
                        st.session_state.patient_data = patient_data
                        st.success(f"Loaded example: {selected_file.name}")
                except Exception as e:
                    st.error(f"Error loading example: {str(e)}")
        else:
            st.warning("No example files found in the data directory.")

    elif input_method == "Enter JSON manually":
        json_input = st.text_area("Enter patient data JSON", height=300)

        if json_input:
            try:
                patient_data = json.loads(json_input)
                st.session_state.patient_data = patient_data
                st.success("Patient data loaded successfully!")
            except json.JSONDecodeError:
                st.error("Invalid JSON format. Please check your input.")

    # Display patient overview if data is loaded
    if st.session_state.patient_data:
        show_patient_overview(st.session_state.patient_data)

    # Generate summary when the button is clicked
    if generate_button and st.session_state.patient_data:
        with st.spinner("Generating discharge summary..."):
            try:
                generator = DischargeSummaryGenerator(api_key=api_key, model=model)
                summary = generator.generate_summary(
                    st.session_state.patient_data, template_type=template_type
                )
                st.session_state.generated_summary = summary
                st.success("Summary generated successfully!")
            except Exception as e:
                st.error(f"Error generating summary: {str(e)}")

    # Display the generated summary if available
    if st.session_state.generated_summary:
        st.header("Generated Discharge Summary")
        st.markdown(st.session_state.generated_summary)

        # Add download button for the summary
        st.download_button(
            label="Download Summary",
            data=st.session_state.generated_summary,
            file_name="discharge_summary.txt",
            mime="text/plain",
        )

    # Add info about other pages
    st.markdown("---")
    st.subheader("Additional Features")
    st.info(
        """
    👈 Use the sidebar navigation to access these features:
    - **Prompt Editor**: View and customize prompt templates
    - **Log Viewer**: Track application activity through logs
    - **Chat Assistant**: Ask questions and get help with a chatbot that remembers conversation history
    """
    )


if __name__ == "__main__":
    main()
