import streamlit as st
import variable_store
import requests
import random

def app():
    if variable_store.status == True:
        st.title("Translated key phrase for your product")
        radio_selection = st.radio('English or French', ['English', 'French'])
        exename = st.text_input("exename", value='', max_chars=None)
        keyname = st.text_input("key Name", value='', max_chars=None)
        if st.button('Translate Now'):
            if radio_selection=='English':
                selection ='en' 
                res = requests.get(f"http://127.0.0.1:8000/keywordextract?ExeName={exename}&keyname={keyname}&TranslatedLanguage={selection}")
                result = res.json()
                st.write(result['events'][0]['executionSucceededEventDetails']['output'])
            if radio_selection=='French':
                selection ='fr'
                res = requests.get(f"http://127.0.0.1:8000/keywordextract?ExeName={exename}&keyname={keyname}&TranslatedLanguage={selection}")
                result = res.json()
                # st.write(result['events']['0']['executionSucceededEventDetails']['output'])
                st.write(result['events'][0]['executionSucceededEventDetails']['output'])


    else:
        st.write("Please login first")

