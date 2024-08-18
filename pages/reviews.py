import streamlit as st
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

if "shared" not in st.session_state:
   st.session_state["shared"] = True

from pages.Utils.helper_code import load_reviews
reviews_df = load_reviews()  # data import: ✅

# Calculate average sentiment by theme
theme_sentiment = reviews_df.groupby('theme_name')['sentiment'].mean().reset_index()

# Distribution of ratings
rating_counts = reviews_df['overall_sentiment'].value_counts() 

# Streamlit app

st.title('Customer Reviews Analysis')

# Average Sentiment by Theme using Plotly Express
st.subheader('Average Sentiment by Theme')
fig = px.bar(theme_sentiment, x='sentiment', y='theme_name', 
                color='sentiment', orientation='h', 
                color_continuous_scale='magma', 
                title='Average Sentiment by Theme')
st.plotly_chart(fig)

# Distribution of Ratings using Plotly Express
st.subheader('Distribution of Overall Sentiments')
fig = px.pie(values=rating_counts.values, names=rating_counts.index, 
                title='Distribution of Overall Sentiments', 
                color_discrete_sequence=px.colors.sequential.Magma)
st.plotly_chart(fig)

st.title('Customer Reviews Analysis')

# WordCloud for all words, filtered by themes
st.subheader('Word Cloud of Reviews')
selected_theme = st.selectbox('Select a Theme', ['All'] + reviews_df['theme_name'].unique().tolist())

if selected_theme == 'All':
    text = ' '.join(reviews_df['cleaned_reviews'])
else:
    text = ' '.join(reviews_df[reviews_df['theme_name'] == selected_theme]['cleaned_reviews'])

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)