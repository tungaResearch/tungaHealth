import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd
from preprocess_text import preprocess_text
from collections import Counter
from wordcloud import WordCloud
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from get_vector_store import get_vector_store
import umap.umap_ as umap
import ast

tpd_df = pd.read_csv('data/viz.csv')
pdf_info_data = pd.read_csv('data/pdf_info_data.csv')
response_data = pd.read_csv('data/response_data.csv')
response_data['embedding'] = response_data['embedding'].apply(ast.literal_eval)
response_data['pdf_name'] = response_data['source'].str.extract(r'/([^/]+)\.pdf$')
# response_data = st.session_state.embeddings_meta_df


sns.set_style("darkgrid")

pdf_info_data['Preprocessed_text'] = pdf_info_data['Page Content'].apply(preprocess_text)
# Concatenate all preprocessed documents into a single string
all_text = ' '.join(pdf_info_data['Preprocessed_text'])

# Tokenize the text into words
all_words = all_text.split()

# Compute word frequencies
word_freq = Counter(all_words)

# Determine the threshold frequency (you can adjust this value)
threshold_freq = 0.5 * len(pdf_info_data)  # For example, consider words that appear in at least 80% of documents as common

# Define a function to filter out stop words from a document
def remove_common_words(text):
    words = text.split()
    filtered_words = [word for word in words if word not in common_words]
    return ' '.join(filtered_words)

# Identify common words (stop words) based on frequency
common_words = [word for word, freq in word_freq.items() if freq > threshold_freq]
pdf_info_data['Preprocessed_text'] = pdf_info_data['Preprocessed_text'].apply(remove_common_words)


def visualize_token_pdfs_dist():
    sns.set_style("darkgrid")
    # Set the width of each bar
    bar_width = 0.35

    x = np.arange(len(tpd_df['pdf_name']))
    plt.figure(figsize=(12,8))
    plt.bar(x - bar_width/2, tpd_df['pages'], width=bar_width, label='Pages')
    plt.bar(x + bar_width/2, tpd_df['tokens'], width=bar_width, label='Tokens')

    plt.xticks(x, tpd_df['pdf_name'], rotation=45)

    plt.xlabel('PDF')
    plt.ylabel('Count')
    plt.title('Pages and Tokens Count for Each PDF')
    plt.legend()

    plt.tight_layout()
    st.pyplot(plt)

#word cloud generator all
def word_cloud_generatior_all():
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=600, background_color='white').generate(all_text)
    # Display the word cloud
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Word Cloud of Preprocessed Text')
    plt.axis('off')
    st.pyplot(plt)

# Frequency Count for all Text
def frequency_count():
    # Generate word frequency counts for all combined texts
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([all_text])
    word_freq = dict(zip(vectorizer.get_feature_names_out(), np.asarray(X.sum(axis=0)).ravel()))

    # Get the top 20 words
    sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Plot bar chart for top words
    plt.figure(figsize=(8, 6))
    sns.barplot(x=[w[1] for w in sorted_word_freq], y=[w[0] for w in sorted_word_freq])
    plt.title('Top 20 Words for All Sources')
    plt.xlabel('Frequency')
    plt.ylabel('Word')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    st.pyplot(plt)



# Generate a word cloud for each sourc
# def word_cloud_generator():
#     # Create subplots for each document
#     fig, axes = plt.subplots(nrows=len(pdf_info_data['Source'].unique()), ncols=2, figsize=(15, 5*len(pdf_info_data['Source'].unique())))

#     # Iterate over each unique source
#     for i, source in enumerate(pdf_info_data['Source'].unique()):
#         source_df = pdf_info_data[pdf_info_data['Source'] == source]

#         # Generate WordCloud
#         wordcloud = WordCloud(width=400, height=300, background_color='white').generate(' '.join(source_df['Preprocessed_text']))
#         axes[i, 0].imshow(wordcloud, interpolation='bilinear')
#         axes[i, 0].set_title(f'Word Cloud for {source}')
#         axes[i, 0].axis('off')

#         # Plot bar chart for top words
#         vectorizer = CountVectorizer()
#         X = vectorizer.fit_transform(source_df['Preprocessed_text'])
#         word_freq = dict(zip(vectorizer.get_feature_names_out(), np.asarray(X.sum(axis=0)).ravel()))
#         sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
#         sns.barplot(x=[w[1] for w in sorted_word_freq], y=[w[0] for w in sorted_word_freq], ax=axes[i, 1])
#         axes[i, 1].set_title(f'Top 20 Words for {source}')
#         axes[i, 1].set_xlabel('Frequency')
#         axes[i, 1].set_ylabel('Word')
#         axes[i, 1].tick_params(axis='y', labelrotation=45)

#     plt.tight_layout()
#     st.pyplot(plt)
   
def umap_viz():
    # UMAP for dimensionality reduction
    sns.set_style("darkgrid")

    # Extracting embedding vectors
    
    embeddings = np.array(response_data['embedding']).tolist()

    umap_embeddings = umap.UMAP(n_neighbors=15, n_components=2, metric='cosine').fit_transform(embeddings)

    # Adding UMAP dimensions to DataFrame
    response_data['umap_1'] = umap_embeddings[:, 0]
    response_data['umap_2'] = umap_embeddings[:, 1]

    # Plot UMAP embeddings with Seaborn
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x="umap_1", y="umap_2", hue="pdf_name", data=response_data)
    plt.title("UMAP Dimensionality Reduction of Embeddings", fontsize=12)
    plt.xlabel("UMAP Dimension 1", fontsize=14)
    plt.ylabel("UMAP Dimension 2", fontsize=14)
    # Move legend to the side, outside the figure
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
    plt.tick_params(axis='both', which='major', labelsize=12)
    st.pyplot(plt)

# st.header("Text word Cloud Per PDF")
# word_cloud_generator()

st.header("Text word Cloud for all PDFs")
word_cloud_generatior_all()

st.header("Frequency Count for All Text")
frequency_count()

st.header("Token Distribution per Document")
visualize_token_pdfs_dist()

st.header("Token Mapping")
umap_viz()

# def select_folder():
#    root = tk.Tk()
#    root.withdraw()
#    folder_path = filedialog.askdirectory(master=root)
# #    root.destroy()
#    return folder_path



# selected_folder_path = st.session_state.get("folder_path", None)
# folder_select_button = st.button("Select Folder")
# if folder_select_button:
#   selected_folder_path = select_folder()
#   st.session_state.folder_path = selected_folder_path

# if selected_folder_path:
#    st.write('Selected folder path:', selected_folder_path)
