import streamlit as st
import variable_store

def app():
    if (variable_store.product!=None):
        st.title("Review for ", variable_store.product)
    else:
        st.write(variable_store.product_error_msg)
