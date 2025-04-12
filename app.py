"""
Medical Discharge Summary Generator
Generate professional discharge summaries from patient data

Group: SiAnDia:DischargeFormers (Group 3)
Members:
- Siva Komaragiri (skomarag)
- Anu Subramanya (ahsubram)
- India Etheridge (ietherid)
"""

import os
import sys
import argparse
from pathlib import Path

# Add the current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from llm.utils import setup_logging
import config


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Discharge Summary Generator")
    parser.add_argument(
        "--mode",
        choices=["web", "generate"],
        default="web",
        help="Run mode: 'web' for web UI, 'generate' for CLI generation",
    )
    parser.add_argument(
        "--input", type=str, help="Input JSON file path (for generate mode)"
    )
    parser.add_argument(
        "--output", type=str, help="Output text file path (for generate mode)"
    )
    parser.add_argument(
        "--template",
        type=str,
        default="general",
        help="Template type to use (for generate mode)",
    )

    return parser.parse_args()


def run_web_ui():
    """Run the web UI using Streamlit."""
    # Setup logging
    logger = setup_logging(config.LOGS_DIR, config.LOG_LEVEL)
    logger.info("Starting web UI")

    # Use streamlit CLI to run the app
    import subprocess

    subprocess.run(
        [
            "streamlit",
            "run",
            str(Path(__file__).parent / "ui" / "streamlit_app.py"),
            "--server.port=8501",
        ]
    )


def run_cli_generation(input_file, output_file, template_type):
    """Run CLI-based generation of a discharge summary."""
    # Setup logging
    logger = setup_logging(config.LOGS_DIR, config.LOG_LEVEL)
    logger.info(f"CLI generation mode: {input_file} -> {output_file}")

    # Import the generator
    from llm.discharge_generator import DischargeSummaryGenerator

    # Generate the summary
    generator = DischargeSummaryGenerator()
    summary = generator.generate_summary_from_file(input_file, template_type)

    # Write to output file or stdout
    if output_file:
        with open(output_file, "w") as f:
            f.write(summary)
        logger.info(f"Summary written to {output_file}")
    else:
        print(summary)


def main():
    """Main application entry point."""
    args = parse_args()

    if args.mode == "web":
        run_web_ui()
    elif args.mode == "generate":
        if not args.input:
            print("Error: --input file is required for generate mode")
            sys.exit(1)
        run_cli_generation(args.input, args.output, args.template)


if __name__ == "__main__":
    main()
