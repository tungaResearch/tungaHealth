from langchain.text_splitter import TokenTextSplitter
import re 
from langchain.document_loaders import PyPDFLoader
import streamlit as st


# Create a function that stores no. of pages and no. of tokens per pdf

@st.cache_data
def pdf_token_pages(loaded_pdfs):
  token_text_splitter = TokenTextSplitter(
    chunk_size=500,
    chunk_overlap=80
)
  # a list to contain token and pages count data
  token_pages_data = []
  token_counter = 0
  page_counter = 0
  #looping thru pdfs and storing content
  for pdf in loaded_pdfs:
    loader = PyPDFLoader(pdf)
    pages = loader.load()
    pdf_name = re.search(r'[^/]+$', pdf).group(0)
    tokenized_pdf = token_text_splitter.split_documents(pages)
    pdf_tpd = {
        "pdf_name": pdf_name,
        "pages": len(pages),
        "tokens": len(tokenized_pdf)
    }
    token_pages_data.append(pdf_tpd)
    token_counter+=len(tokenized_pdf)
    page_counter+=len(pages)

  return token_pages_data