import oracledb
import getpass
import os
import mysql.connector
import streamlit as st
import streamlit_authenticator as stauth
import db



#boolLogin = db.verifyLogin('luffy123', 'luffypass')

#print(boolLogin)


def main():
    login_tab, account_tab = st.tabs(["Login", "Create Account"])

    with account_tab:
        st.markdown("""<div class="emptyDiv"></div>""", unsafe_allow_html=True)

        email = st.text_input("Create Email")
        password = st.text_input("Create Password", type="password")

        if st.button("Create Account"):
            st.write(db.addUser(email, password))

    with login_tab:
        st.markdown("""<div class="emptyDiv"></div>""", unsafe_allow_html=True)

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            db.login(email, password)
if "user" not in st.experimental_get_query_params():
    st.experimental_set_query_params(user="no")
if st.experimental_get_query_params()["user"][0] == "no":
    main()
else:
    st.title("You are logged in")
    print(st.experimental_get_query_params()["email"][0])
