import os
import base64
import streamlit as st
import google.generativeai as genai
from app.config import GEMINI_API_KEY



genai.configure(api_key=GEMINI_API_KEY)


class GeminiChatbot:
    def __init__(self):
        self.model_name = 'gemini-2.0-flash'
        self.model = genai.GenerativeModel(self.model_name)
        self.temperature = 0.7
        self.max_tokens = 1000
        self.conversation_history = []
        self.system_message = "Halo! Saya InsightBot, siap membantumu memahami opini publik tentang brand teknologi favoritmu."
        self.conversation_history.append({"role": "model", "parts": [self.system_message]})

    def chat_completion(self, prompt, temperature=None, max_tokens=None):
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens

        analysis_context = ""
        import streamlit as st
        if "df_cleaned" in st.session_state and "sentiment" in st.session_state.df_cleaned.columns:
            analysis_context = generate_analysis_summary(st.session_state.df_cleaned)

        full_prompt = f"{analysis_context}\n\nPertanyaan pengguna:\n{prompt}"
        self.conversation_history.append({"role": "user", "parts": [full_prompt]})

        try:
            response = self.model.generate_content(
                self.conversation_history,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )
            ai_response = response.text
            self.conversation_history.append({"role": "model", "parts": [ai_response]})
            return ai_response
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Maaf, terjadi kesalahan."

    def reset_conversation_history(self):
        self.conversation_history = [{"role": "user", "parts": [self.system_message]}]


def apply_css():
    with open("src/style.css", "r") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_local_img(file_path: str) -> str:
    full_path = os.path.join(BASE_DIR, "..", file_path)  
    try:
        with open(full_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: File not found at {full_path}")
        return ""

def get_chat_message(contents: str, align: str = "left") -> str:
    div_class = "AI-chat"
    color = "#f1f0f0"
    file_path = os.path.join("assets","ai_icon.png")

    if align == "right":
        div_class = "user-chat"
        color = "#aed6f1"
        file_path = os.path.join("assets","user_icon.png")

    src = f"data:image/png;base64,{get_local_img(file_path)}"

    icon_code = f"<img class='chat-icon' src='{src}' style='width: 30px; height: 30px; border-radius: 50%;' alt='avatar'>"
    formatted_contents = f"""
    <div class="{div_class}" style="display: flex; align-items: flex-start; margin-bottom: 10px;">{icon_code}
    <div class="chat-bubble" style="background-color: {color}; padding: 10px; border-radius: 10px; margin-left: 10px; max-width: 80%;">{contents}</div>
    </div>
    """
    return formatted_contents

def generate_analysis_summary(df):
    from collections import Counter

    total = len(df)
    counts = dict(Counter(df["sentiment"]))
    summary = f"Total tweet yang dianalisis: {total}.\n"
    for sent, count in counts.items():
        summary += f"- {sent.title()}: {count} tweet.\n"

    example = df[["full_text", "sentiment"]].head(3).to_dict(orient="records")
    example_text = "\n".join([f"{i+1}. [{row['sentiment']}] {row['full_text']}" for i, row in enumerate(example)])
    return summary + "\nContoh tweet:\n" + example_text


def main():
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

if __name__ == "__main__":
    main()
