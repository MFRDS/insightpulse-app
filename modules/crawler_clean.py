import re

def clean_text(text, is_reply=False, reply_to_username=None):
    chars_to_replace = ["\n", ",", '"', "U+2066", "U+2069", "’", "‘", "“", "”", "…", "—", "–", "•"]
    pattern = "|".join(map(re.escape, chars_to_replace))
    cleaned_text = re.sub(pattern, " ", text)
    
    if is_reply and reply_to_username:
        first_word = cleaned_text.split(" ")[0]
        if first_word == f"@{reply_to_username}":
            cleaned_text = cleaned_text.replace(f"@{reply_to_username} ", "", 1).strip()
        elif first_word.startswith("@"): 
            cleaned_text = cleaned_text.replace(first_word, "", 1).strip()
    return cleaned_text