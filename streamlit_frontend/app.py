import streamlit as st
import requests

class FileProcessorUI:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def upload_and_process(self, file):
        files = {'file': (file.name, file.getvalue())}
        headers = {'x-api-key': self.api_key}
        response = requests.post(self.api_url, files=files, headers=headers)
        return response

st.title('OOP File Processor UI')

api_url = st.text_input('Backend URL', 'https://simple-file-processor.onrender.com')
api_key = st.text_input('API_KEY', 'your-secret-key')  #API_KEY=your-secret-key
uploaded_file = st.file_uploader('Upload file', type=['pdf','csv','xls','xlsx'])
if uploaded_file and st.button('Process & Download'):
    processor_ui = FileProcessorUI(api_url, api_key)
    result = processor_ui.upload_and_process(uploaded_file)
    if result.status_code == 200:
        st.download_button('Download processed file', data=result.content, file_name='processed_'+uploaded_file.name)
    else:
        st.error(f"Error: {result.text}")
