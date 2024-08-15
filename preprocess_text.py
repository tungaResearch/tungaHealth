import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import seaborn as sns
import matplotlib.pyplot as plt
import re
import streamlit as st

nltk.download('punkt')

# Download NLTK stopwords
nltk.download('stopwords')

# Get the stopwords list
stop_words = set(stopwords.words('english'))

# Define a function to preprocess text and remove stopwords
@st.cache_data
def preprocess_text(text):
    # nltk.download('punkt')

    # # Download NLTK stopwords
    # nltk.download('stopwords')
    
    # Remove leading and trailing whitespace from each line
    text = '\n'.join(line.strip() for line in text.split('\n'))
    # Remove any empty lines
    text = re.sub(r'\n\s*\n', '\n', text)
    # Remove any leading or trailing whitespace
    text = text.strip()
    # Tokenize
    tokens = nltk.word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]  # Remove non-alphabetic tokens
    tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    return ' '.join(tokens)
