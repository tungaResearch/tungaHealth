import os
import streamlit as st

@st.cache_data
def file_converter(uploaded_files, UPLOAD_DIRECTORY):
    path = []
    # Save uploaded files to the directory
    for uploaded_file in uploaded_files:
        # The full path to save the file
        file_path = os.path.join(UPLOAD_DIRECTORY, uploaded_file.name)
        
        # Write the file to the new directory
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        path.append(file_path)
        st.success(f"Saved file: {uploaded_file.name} to {UPLOAD_DIRECTORY}")
    return path