import pandas as pd
import streamlit as st
import docx2txt
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
#from nltk.stem import PorterStemmer
import helper
from io import StringIO
import requests
from bs4 import BeautifulSoup
nltk.download('punkt')
nltk.download('stopwords')
st.set_page_config(layout="wide")


st.title("Text Summarization")
user_input = st.radio("Choose ",("Text","File","Link"),horizontal=True)

if user_input == "Text":
    text = st.text_area("Enter Your Text",height=200, placeholder="Enter the Text")
    num_sentences = int(st.number_input("Enter number of Sentences", step=1))
    if st.button('Submit'):
        summary = helper.summary(text,num_sentences)
        p=summary


        
        words = p.split()

        df = pd.read_csv("synonyms.csv")

        filtered_df = df[df['Word'].isin(words)]
        filtered_df = filtered_df.reset_index(drop=True)
        col1, col2 = st.columns(2, gap= "large")

        col1,col2 = st.columns([4,2])
        # col1.header("Summary")
        # col1.write(p)

        with col1.container():
            background_color = "White"
            st.header("Summary")
            N = 1
            current_string = ""

            for i in p:
                if i == ".":
                    if current_string != "":
                        st.write(N, current_string,'.')
                        N += 1
                        current_string = ""
                else:
                    current_string += i
            if current_string != "":
                st.write(N, current_string,'.')
            
            # st.write(p)

        with col2.container():

            col2.header("Synonyms")
            col2.table(filtered_df)
        


elif user_input == "File":
    uploaded_file = st.file_uploader("Choose a file")
    num_sentences = int(st.number_input("Enter number of sentences", step=1))
    if st.button("Submit"):
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # To read file as string:
        text = stringio.read()
        summary = helper.summary(text,num_sentences)
        #st.write(summary[:])
        p=summary
        
        words = p.split()

        df = pd.read_csv("synonyms.csv")

        filtered_df = df[df['Word'].isin(words)]
        filtered_df = filtered_df.reset_index(drop=True)
        col1, col2 = st.columns(2)

        with col1.container():
            background_color = "white"
            st.header("Summary")
            N = 1
            current_string = ""

            for i in p:
                if i == ".":
                    if current_string != "":
                        st.write(N, current_string,'.')
                        N += 1
                        current_string = ""
                else:
                    current_string += i
            if current_string != "":
                st.write(N, current_string,'.')

            #st.write(p)

        with col2.container():

            col2.header("Synonyms")
            col2.table(filtered_df)
else:
    url = st.text_input("Paste URL here", placeholder="Enter URL")
    num_sentences = int(st.number_input("Enter number of sentences", step=1))
    # Get the website content
    if st.button("Submit"):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the article text
        article = soup.body
        text = ""
        for i in article.strings:
            text += i
        summary = helper.summary(text,num_sentences)
        p=summary
        
        words = p.split()

        df = pd.read_csv("synonyms.csv")

        filtered_df = df[df['Word'].isin(words)]
        filtered_df = filtered_df.reset_index(drop=True)
        col1, col2 = st.columns(2)

        with col1.container():
            background_color = "white"
            st.header("Summary")
            N = 1
            current_string = ""

            for i in summary:
                if i == ".":
                    if current_string != "":
                        st.write(N, current_string,'.')
                        N += 1
                        current_string = ""
                else:
                    current_string += i
            if current_string != "":
                st.write(N, current_string,'.')
                #st.write(p)

        with col2.container():

            col2.header("Synonyms")
            col2.table(filtered_df)
        
