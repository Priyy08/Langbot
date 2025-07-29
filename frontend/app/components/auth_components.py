import streamlit as st
from services.auth_client import handle_login, handle_register

def show_auth_page():
    """Renders the login and registration forms."""
    st.title("Welcome to the Real-Time Chatbot")
    st.write("Please log in or register to continue.")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if not email or not password:
                    st.warning("Please enter both email and password.")
                else:
                    handle_login(email, password)

    with tab2:
        with st.form("register_form"):
            display_name = st.text_input("Display Name")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Register")
            if submitted:
                if not all([display_name, email, password, confirm_password]):
                    st.warning("Please fill out all fields.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    handle_register(email, password, display_name)