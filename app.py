# app.py
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK data (first time only)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

st.title("Memory Palace Builder")
st.write("Transform text into memorable images for effective learning")

# Step 1: Collect material
study_material = st.text_area("Enter the text you want to memorize:")
user_language = st.selectbox("Select your learning language:", ["English", "Spanish", "French", "German", "Chinese"])

if st.button("Extract Keywords") and study_material:
    # Simple keyword extraction
    tokens = word_tokenize(study_material)
    keywords = [word for word in tokens if len(word) > 4][:10]
    
    st.subheader("Keywords for Visualization:")
    for i, keyword in enumerate(keywords, 1):
        st.write(f"{i}. {keyword}")
    
    st.info("In the full version, these keywords would be used to generate memorable images using AI")
