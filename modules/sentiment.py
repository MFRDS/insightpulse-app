import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F


def load_model(model_path="models/sentiment_model"):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    return tokenizer, model


def predict_sentiment(texts, tokenizer, model):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=-1)
        preds = torch.argmax(probs, dim=-1)

   
    label_map = model.config.id2label
    sentiments = [label_map[p.item()] for p in preds]
    confidences = [p.max().item() for p in probs]
    return sentiments, confidences