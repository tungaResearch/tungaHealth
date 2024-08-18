import streamlit as st
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Data loading
from pages.Utils.helper_code import load_reviews
reviews_df = load_reviews()  # Ensure this loads your data correctly

# Calculate average sentiment by theme
theme_sentiment = reviews_df.groupby('theme_name')['sentiment'].mean().reset_index()

# Distribution of ratings
rating_counts = reviews_df['overall_sentiment'].value_counts() 

# Filter for three hospitals
hospitals = ['Kenyatta National Hospital', 'Moi Teaching And Referral Hospital', 'The Mombasa Hospital']  
hospital_data = {hospital: reviews_df[reviews_df['hospital_name'] == hospital] for hospital in hospitals}

# Streamlit app
st.title('Patient Reviews Analysis')

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

# Hospital Sentiment Analysis
st.title("Hospital Sentiment Analysis")

# Create a subplot figure with 1 row and 3 columns
fig = make_subplots(
    rows=1, cols=3, 
    subplot_titles=hospitals, 
    shared_yaxes=False, 
    horizontal_spacing=0.1 
)

# Iterate through each hospital and add a bar chart to the subplot
for i, (hospital, data) in enumerate(hospital_data.items(), start=1):
    if not data.empty:
        theme_sentiment = data.groupby('theme_name')['sentiment'].mean().reset_index()

        # Create the bar chart for the specific hospital
        bar_chart = go.Bar(
            x=theme_sentiment['sentiment'],
            y=theme_sentiment['theme_name'],
            orientation='h',
            marker=dict(color=theme_sentiment['sentiment'], colorscale='Magma'),
            name=hospital
        )

        # Add the bar chart to the subplot
        fig.add_trace(bar_chart, row=1, col=i)

# Update layout to adjust appearance
fig.update_layout(
    title_text="Average Sentiment by Theme for Selected Hospitals",
    height=500,
    width=1200,  # Increase width for better spacing
    showlegend=False,
    yaxis=dict(title='Theme')
)

# Display the figure in Streamlit
st.plotly_chart(fig)

# WordCloud for all words, filtered by themes
st.subheader('Word Cloud of Reviews')
selected_theme = st.selectbox('Select a Theme', ['All'] + reviews_df['theme_name'].unique().tolist())

if selected_theme == 'All':
    text = ' '.join(reviews_df['cleaned_reviews'])
else:
    text = ' '.join(reviews_df[reviews_df['theme_name'] == selected_theme]['cleaned_reviews'])

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Display the word cloud using st.pyplot()
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)
