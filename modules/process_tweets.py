import pandas as pd
from modules.preprocessing import clean_text

def load_and_clean_tweets(filepath):
    try:
        df = pd.read_csv(filepath)

        # Cek kolom yang dibutuhkan
        required_columns = {'created_at', 'username', 'full_text'}
        if not required_columns.issubset(df.columns):
            return None, f"Kolom wajib tidak ditemukan: {required_columns - set(df.columns)}"

        df1 = df[['created_at', 'username', 'full_text']].copy()
        df1['clean_text'] = df1['full_text'].astype(str).apply(clean_text)
        return df1, None

    except Exception as e:
        return None, str(e)
