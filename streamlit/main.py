import streamlit as st
import login, variable_store, home, categorize, review, prices, summarization

PAGELIST = {
    "Login": login,
    # "Home": home,
    "Select Product": categorize,
    "Review": review,
    "Prices": prices,
    "Summarization": summarization
}

def app():
    st.sidebar.title('Review Summarizer App')
    selection_default = st.sidebar.radio("Please Login First", list(PAGELIST.keys()))
    page = PAGELIST[selection_default]
    page.app()

if (__name__=="__main__"):
    app()