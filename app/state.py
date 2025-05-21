import streamlit as st

def init_session():
    defaults = {
        "submitted": False, "scraped": False, "user_input": "",
        "limit": 100, "cleaned": False, "analyzed": False
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val