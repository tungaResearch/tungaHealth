# from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter

def get_text_chunks(documents):
    token_splitter = TokenTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 100,
        length_function = len
    )

    chunks = token_splitter.split_documents(documents)
    return chunks