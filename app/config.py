import os
from dotenv import load_dotenv

load_dotenv()

FOLDER = "data"
FILENAME = "tweets_sentiment.csv"
STORED_PATH = os.path.join(FOLDER, FILENAME)
TWITTER_TOKEN = os.getenv("TWITTER_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")