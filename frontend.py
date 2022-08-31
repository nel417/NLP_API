import streamlit
import requests
import json


def run():
    streamlit.title("Lets Analyze Text")
    sentence = streamlit.text_input("Type Sentence Here")

    data = {
        'sentence': sentence
    }

    if streamlit.button("Analyze Text", key=1):
        response = requests.post("https://nlp-appi.herokuapp.com/analyze_text", json=data)
        analyze = response.text
        streamlit.success(f"Here you go: {analyze}")

    if streamlit.button("Analyze Sentiment", key=2):
        response = requests.post("https://nlp-appi.herokuapp.com/sentiment_analysis", json=data)
        analyze = response.text
        streamlit.success(f"Here you go: {analyze}")

    if streamlit.button("Named Entity Recognition", key="3"):
        response = requests.post("https://nlp-appi.herokuapp.com/entity_recognition", json=data)
        analyze = response.text
        streamlit.success(f"Here you go: {analyze}")


run()