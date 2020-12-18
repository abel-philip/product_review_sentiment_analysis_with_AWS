import streamlit as st
import variable_store

def app():
    option = st.selectbox('Please choose your category', ('Electronics', 'Clothing and Shoes'))
    
    if option=='Electronics':
        st.write('You selected ', option)
        product = st.selectbox('Please choose your Electronic product', ('Gopro case', 'Apple Watch', 'Laptop', 'Camera Grip Strap', 'Headphones'))
    if option=='Clothing and Shoes':
        st.write('You selected ', option)
        product = st.selectbox('Please choose your Clothing or Shoes product', ('Green Shoes', 'Nike T-shirt', 'Adidas Shoes', 'Socks'))
    st.write(product)
    variable_store.product = product
    st.write(variable_store.product)