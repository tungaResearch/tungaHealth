import os
import streamlit as st

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        st.success(f"Folder '{folder_name}' created!")
    else:
        st.info(f"Folder '{folder_name}' already exists.")