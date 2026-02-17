from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
import pickle

# Load model
model = tf.keras.models.load_model("next_word_model.h5")

# Load tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# For padding sequences
from tensorflow.keras.preprocessing.sequence import pad_sequences
max_sequence_len = 5  # Same as used in training

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/predict")
def predict_next_word(input: TextInput):
    text = input.text
    token_list = tokenizer.texts_to_sequences([text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
    predicted_index = model.predict(token_list, verbose=0).argmax(axis=1)[0]

    for word, index in tokenizer.word_index.items():
        if index == predicted_index:
            return {"next_word": word}
    
    return {"next_word": "N/A"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import gradio as gr

def dummy(x):
    return "API Running"

iface = gr.Interface(fn=dummy, inputs="text", outputs="text")

if __name__ == "__main__":
    iface.launch()


