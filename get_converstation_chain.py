# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationalRetrievalChain
# from langchain.chat_models import ChatOpenAI
# import streamlit as st


# def get_conversation_chain(vector_store):
#     llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0, max_tokens=2000)
#     memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
#     conversation_chain = ConversationalRetrievalChain.from_llm(
#         llm = llm,
#         retriever=vector_store.as_retriever(),
#         memory=memory,
#         chain_type='stuff'
#     )
#     return conversation_chain
from langchain.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import torch

def get_conversation_chain(vector_store):
    # Load a tokenizer and model from Hugging Face
    model_name = "EleutherAI/gpt-neox-20b"  # Replace with your desired model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Create a text generation pipeline
    pipe = pipeline(
        "text-generation", 
        model=model, 
        tokenizer=tokenizer, 
        max_length=2000,
        temperature=0.7,
        device=0 if torch.cuda.is_available() else -1  # Use GPU if available
    )

    # Integrate the HuggingFace pipeline with LangChain
    llm = HuggingFacePipeline(pipeline=pipe)

    # Setup memory and conversation chain
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory,
        chain_type='stuff'
    )

    return conversation_chain
