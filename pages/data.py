import pandas as pd
import streamlit as st

tpd_df = pd.read_csv('data/viz.csv')
pdf_info_data = pd.read_csv('data/pdf_info_data.csv')
response_data = pd.read_csv('data/response_data.csv')

st.header("PDFs Info Data")
if st.checkbox("View PDFs Data Info"):
   st.dataframe(tpd_df)
if st.checkbox("View PDFs Preprocessed Data"):
   st.dataframe(pdf_info_data)
if st.checkbox("View Embeddings Data"):
   st.dataframe(response_data[:500])