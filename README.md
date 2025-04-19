# Medical Discharge Summary Generator

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An AI-powered application for generating comprehensive, professional medical discharge summaries from structured patient data. This tool streamlines the documentation process for healthcare professionals while maintaining clinical accuracy.

## 👥 Team

- **Siva Komaragiri** (Andrew ID: skomarag)  
- **Anu Subramanya** (Andrew ID: ahsubram)  
- **India Etheridge** (Andrew ID: ietherid)

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Web Interface](#web-interface)
  - [Command Line Interface](#command-line-interface)
- [Project Structure](#project-structure)
- [Feature Documentation](#feature-documentation)
  - [Summary Generator](#summary-generator)
  - [Template System](#template-system)
  - [Chat Assistant](#chat-assistant)
  - [Prompt Editor](#prompt-editor)
  - [Log Viewer](#log-viewer)
- [Configuration](#configuration)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Development and Contribution](#development-and-contribution)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## 🔍 Overview

The Medical Discharge Summary Generator leverages advanced language models to transform structured patient data into comprehensive, clinically accurate discharge summaries. By automating this documentation process, healthcare professionals can save time while ensuring consistent, high-quality documentation.

Developed by the SiAnDia:DischargeFormers team (Group 3), this application bridges the gap between raw clinical data and professional medical documentation.

## ✨ Key Features

- **AI-Powered Summary Generation**: Utilizes OpenAI's advanced language models (GPT-4, GPT-4.5-Preview, GPT-3.5-Turbo) to create professional discharge summaries
- **Multiple Template Options**: Specialized templates for different medical contexts (cardiac, respiratory, surgical, etc.)
- **User-Friendly Web Interface**: Built with Streamlit for intuitive interaction
- **Flexible Data Input**: Upload JSON files, select from examples, or enter data manually
- **Interactive Chat Assistant**: Ask questions about discharge summaries and medical terminology
- **Custom Prompt Editor**: View and modify prompt templates to customize output
- **Log Tracking System**: Monitor application activities and review historical operations
- **Command-Line Interface**: Support for batch processing via CLI commands

## 💻 System Requirements

- Python 3.9 or higher
- OpenAI API key
- 2GB RAM minimum (4GB recommended)
- 1GB disk space

## 🛠️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/siAnDia-dischargeFormers.git
cd discharge-summary-generator
```

2. **Set up a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Configure your OpenAI API Key**

Create a `.env` file in the project root directory:

```plaintext
OPENAI_API_KEY=your_api_key_here
```

Alternatively, you can use a `credentials.json` file:

```json
{
  "openai_api_key": "your_api_key_here"
}
```

## 🚀 Usage

### Web Interface

Run the web interface:

```bash
python app.py --mode web
```

This will launch a Streamlit web application (default: <http://localhost:8501>) where you can:

- Upload patient data in JSON format
- View patient details
- Select template types
- Generate and download discharge summaries

### Command Line Interface

Generate a discharge summary directly from the command line:

```bash
python app.py --mode generate --input data/patient_data.json --output summary.txt --template cardiac
```

## 📂 Project Structure

- `llm/`: Core LLM integration and prompt engineering
- `ui/`: Web interface components
- `logs/`: Application logs (automatically created)
- `data/`: Example patient data files
- `config.py`: Application configuration
- `app.py`: Main entry point

## 🛠️ Feature Documentation

### Summary Generator

The core functionality of the application, transforming structured patient data into professional discharge summaries.

### Template System

Specialized templates for various medical contexts, allowing customization of the generated summaries.

### Chat Assistant

An interactive assistant to answer questions about discharge summaries and medical terminology.

### Prompt Editor

A tool to view and modify prompt templates, enabling customization of the output.

### Log Viewer

A system to monitor application activities and review historical operations.

## ⚙️ Configuration

All configuration settings are managed in `config.py`. Ensure your OpenAI API key is correctly set up in either `.env` or `credentials.json`.

## 🔒 Security Considerations

- Ensure your OpenAI API key is stored securely and not exposed in public repositories.
- Use HTTPS for secure communication when deploying the web interface.

## 🛠️ Troubleshooting

- If the application fails to start, ensure all dependencies are installed and the virtual environment is activated.
- Verify that your OpenAI API key is valid and correctly configured.

## 🤝 Development and Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code adheres to the project's coding standards.

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙏 Acknowledgments

Special thanks to the SiAnDia:DischargeFormers team (Group 3) for their contributions to this project.
