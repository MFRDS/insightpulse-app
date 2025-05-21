import os, asyncio
import pandas as pd
import streamlit as st
from app.config import FOLDER, STORED_PATH, TWITTER_TOKEN
from modules.crawler import crawl_tweets
from modules.process_tweets import load_and_clean_tweets
from modules.sentiment import load_model, predict_sentiment
from app.dashboard import visualization

def run_pipeline():
    st.header("Dashboard")
    st.write(f"🔍 Keyword: **{st.session_state.user_input}**")
    # st.write(f"📊 Jumlah Tweet: **{st.session_state.limit}**")

    if not st.session_state.scraped:
        with st.spinner("Scraping tweet..."):
            os.makedirs(FOLDER, exist_ok=True)
            if os.path.exists(STORED_PATH): os.remove(STORED_PATH)
            result = asyncio.run(crawl_tweets(
                st.session_state.user_input,
                st.session_state.limit,
                STORED_PATH,
                TWITTER_TOKEN
            ))
            if result:
                st.session_state.scraped = True
                st.rerun()
            else:
                st.error("Gagal scraping.")
                st.stop()

    if os.path.exists(STORED_PATH):
        df = pd.read_csv(STORED_PATH)
        # st.subheader("Hasil Scraping")
        # st.dataframe(df[['created_at', 'username', 'full_text']].head())

        if not st.session_state.cleaned:
            with st.spinner("Membersihkan teks..."):
                df_cleaned, error = load_and_clean_tweets(STORED_PATH)
                if error:
                    st.error(error)
                else:
                    st.session_state.df_cleaned = df_cleaned
                    st.session_state.cleaned = True
                    st.rerun()

        if st.session_state.cleaned and not st.session_state.analyzed:
            with st.spinner("Analisis sentimen..."):
                try:
                    tokenizer, model = load_model("models/sentiment_model")
                    sentiments, confidences = predict_sentiment(
                        st.session_state.df_cleaned["clean_text"].tolist(),
                        tokenizer, model
                    )
                    st.session_state.df_cleaned["sentiment"] = sentiments
                    st.session_state.analyzed = True
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

        if st.session_state.cleaned and st.session_state.analyzed:
            visualization()