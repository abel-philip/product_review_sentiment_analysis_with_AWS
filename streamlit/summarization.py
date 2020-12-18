import streamlit as st
import variable_store
import requests
import random

def app():
    if if variable_store.status == True:
        st.title("Translated key phrase for your product")
        radio_selection = st.radio('English or French', ['English', 'French'])
        exename = random.randint(100000000000,999999999999)
        keyname = random.randint(100000000000,999999999999)
        if radio_selection=='English':
            selection ='en' 
            res = requests.get(f"http://127.0.0.1:8000/keywordextract?ExeName={exename}&keyname={keyname}&TranslatedLanguage={selection}")
            result = res.json()
            st.write(result)
        if radio_selection=='English':
            selection ='fr'
            res = requests.get(f"http://127.0.0.1:8000/keywordextract?ExeName={exename}&keyname={keyname}&TranslatedLanguage={selection}")
            result = res.json(result)

