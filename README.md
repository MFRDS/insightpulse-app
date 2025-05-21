# InsightPulse <img align="center" src="https://raw.githubusercontent.com/MFRDS/insightpulse-app/refs/heads/main/assets/ai_icon.png" height="30" width="30" />

Welcome to the InsightPulse repository!  

<img src="https://raw.githubusercontent.com/MFRDS/insightpulse-app/refs/heads/main/assets/insightpulse.png" width="70%" height="70%" />

## Overview

**InsightPulse** is a real-time sentiment analysis web application that leverages the **IndoBERT** model to analyze public opinions on various technology brands through Twitter. This system allows users to enter a keyword (brand name), collect related tweets, process and classify them into sentiment categories, and visualize the results in an interactive dashboard. Additionally, users can explore deeper insights using the integrated chatbot powered by Gemini LLM.


## Features

- **Keyword-based tweet scraping** using Playwright.
- **Text preprocessing** pipeline: cleansing, case folding, and stopword removal.
- **Fine-tuned IndoBERT model** for sentiment classification (positive, negative, neutral).
- **Interactive data visualization** (bar chart, pie chart, word cloud).
- **InsightBot** (LLM-based chatbot) to explain results interactively.
- **Downloadable results** in CSV format.



## Installation

To get started with the project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/MFRDS/insightpulse-app
    ```
    
2. **Download the Sentiment Model (Required)**
   - **Download the model [here](https://drive.google.com/file/d/1TkzBhryHjkUN6i-V5wMK4ydGzB7wNnio/view?usp=sharing)**
   - After downloading, extract it to the following path: models/sentiment_model
     
4. **Install the required libraries**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Streamlit app**:
    ```bash
    streamlit run run.py
    ```

## Technologies Used

- Streamlit
- HuggingFace Transformers
- PyTorch
- Plotly
- Playwright (for scraping)
- Gemini API (via LangChain)
- WordCloud

## License

This project is licensed for academic and non-commercial use.
