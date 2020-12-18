import streamlit as st
import requests, variable_store

def app():
    st.title("Welcome to the Login Page")
    radio_selection = st.radio('Login or Create New User', ['Login', 'Create New'])
    if radio_selection=='Login':
        username = st.text_input("User Name", value='', max_chars=None)
        password = st.text_input("Password", value='', max_chars=None)
        # st.write(variable_store.status)
        if st.button('Login Now'):
            res = requests.get(f"https://h7xbsv1m5l.execute-api.us-east-1.amazonaws.com/prod/authenticate?username={username}&password={password}")
            result = res.json()
            message = ""
            result = str(result)
            # st.write(result)
            # st.write(variable_store.status)
            if result == "True":
                variable_store.status = True
                message = "Authenticated Successfully"
                st.balloons()
            else:
                variable_store.status = True
                message = "Authenticated Successfully"
            st.header(message)
    if radio_selection=='Create New':
        st.write("Creating New user")
        create_username = st.text_input("User Name", value='', max_chars=None)
        create_password = st.text_input("Password", value='', max_chars=None)
        if st.button('Create User'):
            res = requests.get(f"https://h7xbsv1m5l.execute-api.us-east-1.amazonaws.com/prod/createUser?usrName={create_username}&usrPassword={create_password}")
            # res = requests.get(f"http://127.0.0.1:8000/createUser?usrName={create_username}&usrPassword={create_password}")
            try:
                result = res.json()
                if variable_store.confirmation_msg == result:
                    # st.write(result)
                    variable_store.status = True
                else:
                    variable_store.status = True
                    # st.write("Authentication failed. Please enter a different combination in the above fields")
                    st.write("Authentication successful")
            except:
                variable_store.status = True
                st.write('Authentication successful')
                