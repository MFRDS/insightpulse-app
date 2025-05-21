import sys
import asyncio
import os
from app.dashboard import interface, insightbot
from app.controller import run_pipeline
from app.state import init_session

def main():
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

    import streamlit as st
    from streamlit_option_menu import option_menu

    st.set_page_config(page_title="InsightPulse", page_icon="assets/ai_icon.png", layout="wide")
    init_session()

    if not st.session_state.submitted:
        interface()
    else:
        selected = option_menu(
            None,
            ["Dashboard", "InsightBot"],
            icons=["bar-chart-line", "robot"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )

        if selected == "Dashboard":
            run_pipeline()
        elif selected == "InsightBot":
            insightbot()
