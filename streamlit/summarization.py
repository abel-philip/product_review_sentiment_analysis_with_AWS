import streamlit as st
import variable_store
import requests

def app():
    url = "https://news-summarizer.p.rapidapi.com/summarize"
    text = 
    payload = "{\r\n    \"input_link\": \"\",\r\n    \"input_text\": \"  {text}\"\r\n}"
    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': "71bc212db5mshc4194f3139b5410p14d0e4jsn1d89d35f8c32",
        'x-rapidapi-host': "news-summarizer.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

