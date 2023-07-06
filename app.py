import streamlit
import pandas as pd
import streamlit as st
import docx2txt
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import helper
from io import StringIO
import requests
from bs4 import BeautifulSoup

st.title("Text Summarization")
user_input = st.radio("Choose ",("Text","File","Link"),horizontal=True)
if user_input == "Text":
    text = st.text_input("Enter Your Text")
    num_sentences = int(st.number_input("Enter number of Line"))
    if st.button('Submit'):
        summary = helper.summary(text,num_sentences)
        st.write(summary)
        st.write(summary)
elif user_input == "File":
    uploaded_file = st.file_uploader("Choose a file")
    num_sentences = int(st.number_input("Enter number of Line"))
    if st.button("Submit"):
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # To read file as string:
        text = stringio.read()
        summary = helper.summary(text,num_sentences)
        st.write(summary[38:])
else:
    url = st.text_input("Paste URL here")
    num_sentences = int(st.number_input("Enter number of Line"))
    # Get the website content
    if st.button("Submit"):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the article text
        article = soup.find("article")
        text = article.get_text()
        summary = helper.summary(text,num_sentences)
        st.write(summary)
        
