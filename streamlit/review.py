import streamlit as st
import variable_store
import requests, pandas as pd
def app():
    if variable_store.status == True:
        if (variable_store.product!=None):
            title_value = "Review for " + variable_store.product
            st.header(title_value)  
            id = variable_store.product_references[variable_store.product][0]
            print(id)
            # res = requests.get(f"https://h7xbsv1m5l.execute-api.us-east-1.amazonaws.com/prod/product_reviews?product_id={id}")
            
            res = requests.get(f"http://127.0.0.1:8000/product_reviews?product_id=B00B9U44NY")
            result = res.json()
            positive = result[0]
            negative = result[1]
            df = pd.DataFrame({'Positive': pd.Series(positive), 'Negative': pd.Series(negative)})
            st.table(df)
            # st.plotly_chart(df)
        else:
            st.write(variable_store.product_error_msg)
