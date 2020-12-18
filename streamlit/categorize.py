import streamlit as st
import variable_store

def app():
    if variable_store.status == True:
        option = st.selectbox('Please choose your category', ('Electronics', 'Clothing and Shoes'))
        
        if option=='Electronics':
            st.write('You selected ', option)
            product = st.selectbox('Please choose your Electronic product', ('Control Cable', 'LG Disc Player', 'Storite Hard Drive', 'Bracket Pole Mount'))
        if option=='Clothing and Shoes':
            st.write('You selected ', option)
            product = st.selectbox('Please choose your Clothing or Shoes product', ('Adidas Shoes', 'Red Shoes'))
        # st.write(product)
        variable_store.product = product
        # st.write(variable_store.product)