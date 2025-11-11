import os
import streamlit as st
import requests

class FileProcessorUI:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def upload_and_process(self, file):
        files = {'file': (file.name, file.getvalue())}
        headers = {'x-api-key': self.api_key}
        # Added timeout to avoid premature connection closing
        response = requests.post(self.api_url, files=files, headers=headers, timeout=60)
        response.raise_for_status()  # Raises exception if status_code >= 400
        return response

# Load backend URL and API key from environment variables
API_URL = os.getenv("BACKEND_URL", "https://example-backend.onrender.com/process-file")
API_KEY = os.getenv("API_KEY", "default-secret-key")

st.title("OOP File Processor UI")
st.write("Upload a PDF/CSV/Excel file and download the processed result.")

uploaded_file = st.file_uploader("Upload file", type=["pdf", "csv", "xls", "xlsx"])

if uploaded_file and st.button("Process & Download"):
    try:
        processor_ui = FileProcessorUI(API_URL, API_KEY)
        result = processor_ui.upload_and_process(uploaded_file)
        st.download_button(
            "Download processed file",
            data=result.content,
            file_name=f"processed_{uploaded_file.name}"
        )
    except requests.exceptions.RequestException as e:
        st.error(f"Error during processing: {e}")
