import os
import re
import nltk
import PyPDF2
import nest_asyncio
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from llama_parse import LlamaParse
from langchain.schema import Document
from llama_index.core import SimpleDirectoryReader
from langchain_community.document_loaders import UnstructuredMarkdownLoader, TextLoader


# class CustomTextLoader(BaseLoader):
#     def __init__(self, file_path: str, encoding: str = 'utf-8'):
#         self.file_path = file_path
#         self.encoding = encoding

#     def load(self):
#         with open(self.file_path, 'r', encoding=self.encoding) as f:
#             text = f.read()
#         # Create a Document object from the text
#         document = Document(page_content=text)
#         return [document]
    

@st.cache_data
def get_pdf_text(loaded_pdfs):
    sources = []
    documents = []
    page_contents = []

    load_dotenv()
    # set up parser
    parser = LlamaParse(
        # api_key=llama_key,
        result_type="markdown"  # "markdown" and "text" are available
    )
    
    file_extractor = {".pdf": parser}
    #looping thru pdfs and storing content
    for pdf in loaded_pdfs:
        pages = SimpleDirectoryReader(input_files=[pdf], file_extractor=file_extractor).load_data(nest_asyncio.apply())
        pdf_name = re.search(r'[^/]+$', pdf).group(0)
        for document in pages:
            sources.append(pdf_name)
            metadata = {
                "source": f"{pdf_name}",
                # "author": "John Doe",
                # "title": "Example Document"
            }
            lp_parsed_documents = Document(page_content=document.text, metadata=metadata)
            documents.append(lp_parsed_documents)
            page_contents.append(document.text)
    
    print("Processing Markdown")
    with open('data/output.md', 'w', encoding='utf-8') as f:  
        for doc in documents:
            f.write(doc.page_content + '\n')
    
    # with open('data/output.md', 'r', encoding='utf-8') as f:
    #         text = f.read()
        # Create a Document object from the text
    # r_document = Document(page_content=text)
    # # markdown_path = r"data\output.md"
    # markdown_path = os.path.abspath("data/output.md")
    # # loader = UnstructuredMarkdownLoader(markdown_path)
    # # loader = TextLoader(markdown_path)
    # loader = CustomTextLoader(file_path=markdown_path, encoding='utf-8')

    # nltk.download('averaged_perceptron_tagger', quiet=False)
    # print("Loading documents")
    # # lp_parsed_documents = loader.load()
    # lp_parsed_documents = Document(page_content=text)
    print("Formulary processed successfully!")
    return sources, documents, page_contents