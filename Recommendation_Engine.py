import streamlit as st
import pandas as pd
from langchain_community.llms import Cohere
import cohere

# Load sentiment data
sentiment_data = pd.read_csv("FlipKart_Dataset_with_Sentiment_Analysis.csv")

# Initialize Cohere (Replace with your Cohere API Key)
cohere_api_key ='Wq0FyPF9tr0n7PBq1gRLXGxr3Bct2iIIJoz1a3PS'
co = cohere.Client(cohere_api_key)

# Function to recommend products based on user query
def recommend_products(query, sentiment_data):
    # Analyze the user's input using Cohere
    response = co.generate(prompt=query, model='command-xlarge-nightly')
    
    # Process response (you can also use a custom NLP method if needed)
    search_keywords = response.generations[0].text.strip().split()
    
    # Filter sentiment data based on query analysis (e.g., find related product names or positive reviews)
    recommendations = sentiment_data[sentiment_data['Cleaned_Review'].str.contains('|'.join(search_keywords))]
    
    # Sort products by sentiment score
    recommendations = recommendations.sort_values(by='TextBlob_Sentiment_Score', ascending=False)
    
    # Return top 5 products (Name and Price only)
    return recommendations[['Product Name', 'Price']].head(5)

# Set page config
st.set_page_config(page_title="Flipkart Product Recommendation", layout="centered")

# Streamlit App Interface
st.markdown("<h1 style='text-align: center; color: #00BFFF;'>📲 Flipkart Product Recommendation Engine</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFFFFF;'>Find the best-rated phones based on user reviews and sentiment analysis!</h3>", unsafe_allow_html=True)

# Add a relevant phone banner image for better UI
st.image("https://mir-s3-cdn-cf.behance.net/projects/404/e4887c180973059.Y3JvcCwxMTEyLDg3MCw2Niww.jpg", use_column_width=True)

# User input section with styled markdown
st.markdown("<h4 style='color: #800000;'>🚀 Enter your preferences to get the best phone recommendations:</h4>", unsafe_allow_html=True)  # Maroon color
st.markdown("<p style='color: #FAEBD7;'>For example: <b>best camera phone</b>, <b>lightweight</b>, <b>long battery life</b>, etc.</p>", unsafe_allow_html=True)  # Linen color

# Add disclaimer about input length
st.markdown("<p style='color: #FF4500;'>⚠️ Disclaimer: Please limit your input to 100 words or less.</p>", unsafe_allow_html=True)

# Create a container for input elements
with st.container():
    query = st.text_area("Describe your ideal phone features or type:", height=100)
    recommend_button = st.button("🔍 Recommend")

# Show recommendations when the button is clicked
if recommend_button and query:
    recommended_products = recommend_products(query, sentiment_data)
    
    if not recommended_products.empty:
        st.markdown("<h3 style='color: #32CD32;'>🎊 Top 5 Recommended Phones:</h3>", unsafe_allow_html=True)
        
        # Display product name and price with colored text in a structured format
        for idx, row in recommended_products.iterrows():
            st.markdown(f"<div style='border: 1px solid #00BFFF; border-radius: 10px; padding: 10px; margin: 10px 0; background-color: #1E1E1E;'><p style='font-size:18px; color:#FFFFFF;'><b>{row['Product Name']}</b> - <span style='color:#FF4500;'>₹{row['Price']}</span></p></div>", unsafe_allow_html=True)
    else:
        st.warning("No matching products found. Please try a different query.")

# Add the new footer with your name
st.markdown("<p style='text-align: center; font-size:14px; color:gray;'>Flipkart Product Recommendation Engine by <b>Vinith</b></p>", unsafe_allow_html=True)



# streamlit run D:\Guvi\projects\Flipkart/Recommendation_Engine.py

