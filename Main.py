import subprocess
import sys

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain-google-genai==0.0.4"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain==0.1.0"])
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import PromptTemplate
from langchain import LLMChain
import streamlit as st
import os

# Set your Google API key using Streamlit secrets
os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]

# Streamlit App Title
st.header("Rap Song Generator - VK")
st.subheader("Generate rap songs in the style of famous artists using Generative AI")

# Create prompt template for generating rap songs
rap_template = """
Write a {length}-line rap song in the style of {artist} about {theme}.
"""

rap_prompt = PromptTemplate(
    template=rap_template,
    input_variables=['length', 'artist', 'theme']
)

# Initialize Google's Gemini model
gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")

# Create LLM chain using the prompt template and model
rap_chain = LLMChain(llm=gemini_model, prompt=rap_prompt)

# Streamlit UI
theme = st.text_input("Enter the theme of the rap song (e.g., struggle, success, love):")
artist = st.selectbox(
    "Choose the artist's style:",
    ["Eminem", "Tupac", "Snoop Dogg", "Kendrick Lamar", "Nicki Minaj", "Custom"]
)
length = st.slider("Number of lines in the rap song:", min_value=4, max_value=20, value=8, step=2)

if st.button("Generate Rap Song"):
    if theme and artist and length:
        # Invoke the chain to generate the rap song
        rap_song = rap_chain.run({"length": length, "artist": artist, "theme": theme})
        st.write("### Your Generated Rap Song:")
        st.write(rap_song)
    else:
        st.error("Please provide a theme, artist, and length.")
