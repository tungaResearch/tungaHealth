import streamlit as st
import os
def upload_files(folder_name):
    uploaded_file = st.file_uploader(f"Upload files to {folder_name}", type=['pdf', 'docx'], key=folder_name)
    if uploaded_file is not None:
        with open(os.path.join(folder_name, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File uploaded to {folder_name}!")