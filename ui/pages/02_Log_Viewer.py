"""
Log viewer page for tracking application logs.
"""

import streamlit as st
import sys
from pathlib import Path
import glob
import os
import datetime

# Add the parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import config

st.set_page_config(page_title="Log Viewer", page_icon="📊", layout="wide")

st.title("Log Viewer")
st.markdown("View and analyze application logs")


def get_log_files():
    """Get available log files from the logs directory."""
    logs_dir = Path(config.LOGS_DIR)
    if not logs_dir.exists():
        return []

    log_files = list(logs_dir.glob("*.log"))
    return sorted(log_files, key=os.path.getmtime, reverse=True)


def parse_log_line(line):
    """Parse a log line into its components."""
    try:
        # Example format: 2025-04-12 15:31:57 | INFO | Starting web UI
        parts = line.split(" | ", 2)
        if len(parts) >= 3:
            timestamp = parts[0]
            level = parts[1]
            message = parts[2]

            return {"timestamp": timestamp, "level": level, "message": message}
        return None
    except Exception:
        return None


def filter_logs(logs, level=None, search_term=None, date_range=None):
    """Filter logs based on criteria."""
    filtered_logs = []

    for log in logs:
        if level and log["level"] != level:
            continue

        if search_term and search_term.lower() not in log["message"].lower():
            continue

        if date_range:
            try:
                log_date = datetime.datetime.strptime(
                    log["timestamp"], "%Y-%m-%d %H:%M:%S"
                ).date()
                if log_date < date_range[0] or log_date > date_range[1]:
                    continue
            except Exception:
                pass

        filtered_logs.append(log)

    return filtered_logs


def main():
    # Sidebar with filtering options
    with st.sidebar:
        st.header("Log Filters")

        # Log file selection
        log_files = get_log_files()

        if not log_files:
            st.warning("No log files found")
            return

        selected_log = st.selectbox(
            "Select Log File", options=log_files, format_func=lambda x: x.name
        )

        # Log level filter
        level_filter = st.selectbox(
            "Log Level",
            ["All", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            index=0,
        )

        # Text search
        search_term = st.text_input("Search in logs")

        # Date range
        use_date_filter = st.checkbox("Filter by date")
        date_range = None

        if use_date_filter:
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start date")
            with col2:
                end_date = st.date_input("End date")
            date_range = (start_date, end_date)

        refresh_button = st.button("Refresh Logs")

    # Main content area
    st.subheader(f"Viewing: {selected_log.name if selected_log else ''}")

    if selected_log:
        try:
            with open(selected_log, "r") as f:
                log_content = f.readlines()

            # Parse logs
            parsed_logs = []
            for line in log_content:
                line = line.strip()
                if line:
                    parsed_log = parse_log_line(line)
                    if parsed_log:
                        parsed_logs.append(parsed_log)

            # Apply filters
            if level_filter != "All":
                parsed_logs = [
                    log for log in parsed_logs if log["level"] == level_filter
                ]

            if search_term:
                parsed_logs = [
                    log
                    for log in parsed_logs
                    if search_term.lower() in log["message"].lower()
                ]

            if date_range:
                filtered_logs = []
                for log in parsed_logs:
                    try:
                        log_date = datetime.datetime.strptime(
                            log["timestamp"], "%Y-%m-%d %H:%M:%S"
                        ).date()
                        if date_range[0] <= log_date <= date_range[1]:
                            filtered_logs.append(log)
                    except Exception:
                        pass
                parsed_logs = filtered_logs

            # Display logs
            if parsed_logs:
                log_data = []
                for log in parsed_logs:
                    log_data.append(
                        {
                            "Timestamp": log["timestamp"],
                            "Level": log["level"],
                            "Message": log["message"],
                        }
                    )

                st.dataframe(log_data, use_container_width=True)
                st.info(f"Showing {len(log_data)} log entries")

                # Allow downloading filtered logs
                if log_data:
                    log_text = "\n".join(
                        [
                            f"{log['Timestamp']} | {log['Level']} | {log['Message']}"
                            for log in log_data
                        ]
                    )
                    st.download_button(
                        label="Download Filtered Logs",
                        data=log_text,
                        file_name=f"filtered_{selected_log.name}",
                        mime="text/plain",
                    )
            else:
                st.info("No logs match your filters")

        except Exception as e:
            st.error(f"Error reading log file: {str(e)}")
    else:
        st.info("Select a log file to view")


if __name__ == "__main__":
    main()
