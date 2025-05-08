import random
import streamlit as st

def tokenize(text):
    return text.lower().split()

def build_trigram_model(words):
    model = {}
    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        if key not in model:
            model[key] = []
        model[key].append(words[i + 2])
    return model

def generate_text(model, start_words, length=10):
    words = start_words.lower().split()
    if len(words) < 2:
        return "Please enter at least two start words."
    
    key = (words[-2], words[-1])
    output = list(key)

    for _ in range(length):
        next_words = model.get(key)
        if not next_words:
            break
        next_word = random.choice(next_words)
        output.append(next_word)
        key = (key[1], next_word)
        if next_word.endswith(('.', '!', '?')):
            break

    return ' '.join(output).capitalize()

# Load corpus once
@st.cache_data
def load_model():
    try:
        with open('D:\\mini LLM chatbot\\bigram_app\\corpus.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        words = tokenize(text)
        return build_trigram_model(words)
    except FileNotFoundError:
        st.error("Missing 'corpus.txt'. Please place it in the app folder.")
        st.stop()

# Streamlit UI
st.title("Trigram Text Generator")

model = load_model()

start_words = st.text_input("Enter two start words:")
length = st.slider("Max number of words to generate", min_value=5, max_value=50, value=10)

if st.button("Generate"):
    if len(start_words.strip().split()) < 2:
        st.warning("Please enter at least two start words.")
    elif tuple(start_words.strip().split()) not in model:
        st.warning("word not found")  
    else:
        result = generate_text(model, start_words, length)
        st.text_area("Generated Text", result, height=150)
