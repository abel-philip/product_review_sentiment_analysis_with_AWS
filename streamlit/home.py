import streamlit as st
import variable_store

def app():
    if variable_store.status == True:
        st.write("Welcome To Your Home Page")
    else:
        st.write("Please login first")