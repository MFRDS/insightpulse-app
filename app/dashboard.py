import streamlit as st
import plotly.express as px
from chatbot.chatbot import GeminiChatbot, get_chat_message, apply_css
from src.list_brand import tech_brands


def interface():
    
    col1, col2, col3, col4= st.columns([3, 1, 3,1])
    with col1:
        st.markdown("""
        <div style="font-size:12px; text-align: justify;">
            <br>
            <br>
            <h3>Selamat datang di <b>InsightPulse</b></h3>
            <p><b>Temukan apa yang sedang dibicarakan pengguna Twitter tentang brand teknologi favoritmu!</b></p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.image("assets/logo.png", width=400)
        st.session_state.user_input = st.text_input(
            "Masukkan keyword Brand Teknologi", placeholder="Contoh: Samsung, Apple, Xiaomi"
        )

        if st.button("Mulai"):
            user_input = st.session_state.user_input.strip()
           
            if not user_input:
                st.warning("Keyword tidak boleh kosong.")
            elif user_input.lower() not in [brand.lower() for brand in tech_brands]:
                st.error("Brand tidak dikenali. Silakan masukkan brand teknologi yang valid.")
            else:
                st.session_state.user_input = user_input 
                st.session_state.submitted = True
                st.rerun()

def visualization():

    df = st.session_state.df_cleaned
    df["sentiment"] = df["sentiment"].str.lower() 

    st.success("Analisis selesai!")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Data", len(df))
    with col2:
        positive_count = df[df["sentiment"] == "positive"].shape[0]
        st.metric("Sentimen Positif", positive_count)
    with col3:
        negative_count = df[df["sentiment"] == "negative"].shape[0]
        st.metric("Sentimen Negatif", negative_count)
    with col4:
        neutral_count = df[df["sentiment"] == "neutral"].shape[0]
        st.metric("Sentimen Netral", neutral_count)

    
    color_map = {
        'negative': '#e74c3c',  
        'neutral':  '#2b9dea',  
        'positive': '#52be80'  
    }

    category_order = ['negative', 'neutral', 'positive']


    
    sentiment_list = list(color_map.keys())
    df_filtered = df[df["sentiment"].isin(sentiment_list)].copy()

    
    sentiment_counts = df_filtered["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ['Sentimen', 'Jumlah']

    fig_bar = px.bar(sentiment_counts,
                    x="Sentimen",
                    y="Jumlah",
                    color="Sentimen",
                    color_discrete_map=color_map,
                    category_orders={"Sentimen": category_order},
                    labels={'Sentimen': 'Sentimen', 'Jumlah': 'Jumlah'},
                    title="Distribusi Sentimen")
    st.plotly_chart(fig_bar, use_container_width=True)

   
    fig_pie = px.pie(df_filtered,
                    names="sentiment",
                    color="sentiment",
                    color_discrete_map=color_map,
                    category_orders={"sentiment": category_order},
                    title="Proporsi Sentimen")
    st.plotly_chart(fig_pie, use_container_width=True)

    try:
        from wordcloud import WordCloud, STOPWORDS

        st.subheader("Word Cloud Sentimen")
        sentiment_type = st.radio("Pilih Sentimen untuk Word Cloud:", ["POSITIVE", "NEGATIVE"])

        if sentiment_type == "POSITIVE":
            positive_df = df[df["sentiment"] == "positive"]
            if not positive_df.empty:
                positive_words = " ".join(positive_df["clean_text"].astype(str))
                wordcloud_positive = WordCloud(width=800, height=400, background_color='white').generate(positive_words)
                st.image(wordcloud_positive.to_array())
            else:
                st.info("Tidak ada data dengan sentimen POSITIVE untuk membuat Word Cloud.")
        elif sentiment_type == "NEGATIVE":
            negative_df = df[df["sentiment"] == "negative"]
            if not negative_df.empty:
                negative_words = " ".join(negative_df["clean_text"].astype(str))
                wordcloud_negative = WordCloud(width=800, height=400, background_color='white').generate(negative_words)
                st.image(wordcloud_negative.to_array())
            else:
                st.info("Tidak ada data dengan sentimen NEGATIVE untuk membuat Word Cloud.")

    except ImportError:
        st.warning("Untuk menampilkan Word Cloud, instal library 'wordcloud' terlebih dahulu. (pip install wordcloud)")

    st.download_button("Download CSV Hasil", df.to_csv(index=False), file_name="tweets_sentiment.csv")

    # if st.button("Ulangi"):
    #     for key in ["submitted", "scraped", "user_input", "limit", "cleaned", "analyzed", "df_cleaned"]:
    #         if key in st.session_state:
    #             del st.session_state[key]
    #     st.rerun()

def insightbot():
    import streamlit as st
    st.title("InsightBot")
    apply_css()

    if "chatbot" not in st.session_state:
        st.session_state.chatbot = GeminiChatbot()

    chatbot = st.session_state.chatbot

    for msg in chatbot.conversation_history:
        if msg["role"] == "user":
            st.markdown(get_chat_message(msg["parts"][0], align="right"), unsafe_allow_html=True)
        elif msg["role"] == "model":
            st.markdown(get_chat_message(msg["parts"][0], align="left"), unsafe_allow_html=True)

    user_input = st.chat_input("Tulis pesan...")

    if user_input:
        response = chatbot.chat_completion(user_input)
        st.rerun()
