import streamlit
import pandas as pd
import streamlit as st
import docx2txt
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Function to tokenize and preprocess text
def preprocess_text(text):
    # Tokenize text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if not word.lower() in stop_words]
    # Stem words
    ps = PorterStemmer()
    words = [ps.stem(word) for word in words]
    return sentences, words

# Function to calculate sentence scores based on word frequency
def calculate_sentence_scores(words, sentences):
    # Calculate word frequency
    word_frequency = {}
    for word in words:
        if word not in word_frequency:
            word_frequency[word] = 1
        else:
            word_frequency[word] += 1
    # Calculate sentence scores based on word frequency
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequency:
                if len(sentence.split(' ')) < 30:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_frequency[word]
                    else:
                        sentence_scores[sentence] += word_frequency[word]
    return sentence_scores

# Function to generate summary
def generate_summary(text, num_sentences):
    # Preprocess text
    sentences, words = preprocess_text(text)
    # Calculate sentence scores
    sentence_scores = calculate_sentence_scores(words, sentences)
    # Sort sentences by score in descending order
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    # Generate summary
    summary_sentences = [sentence[0] for sentence in sorted_sentences[:num_sentences]]
    summary = ' '.join(summary_sentences)
    return summary

def read_text(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']
        return raw_data.decode(encoding)
    
def summary(text,num_sentences):
    sentences, words = preprocess_text(text)
    sentence_scores = calculate_sentence_scores(words, sentences)
    summary = generate_summary(text, num_sentences)
    return summary