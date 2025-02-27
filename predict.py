from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Load the model and tokenizer (ensure this matches your model choice)
model_name = "bert-base-uncased"  # Example model
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def predict(input_text):
    # Tokenize input text
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=-1)
    return prediction.item()

# Example input for prediction
input_text = "The weather today is sunny."
prediction = predict(input_text)
print(f"Prediction: {prediction}")
