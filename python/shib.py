import streamlit as st
import pytesseract
from PIL import Image
import pyttsx3
from transformers import MarianMTModel, MarianTokenizer

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Set up MarianMT Translation Model
def load_translation_model(src_lang, tgt_lang):
    model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    return model, tokenizer

# Translation function
def translate_text(model, tokenizer, text):
    tokens = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**tokens)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# TTS function
def text_to_speech(text, lang="en"):
    engine.setProperty('voice', lang)
    engine.say(text)
    engine.runAndWait()

# OCR function
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Streamlit UI
st.title("Indian Language Translator with Speech Output")

# Language selection
src_lang = st.selectbox("Select Source Language", ["English"])
tgt_lang = st.selectbox("Select Target Language", ["Hindi", "Marathi", "Bengali", "Gujarati", "Tamil", "Telugu"])

# Load the correct model based on the target language
if tgt_lang == "Hindi":
    model, tokenizer = load_translation_model('en', 'hi')
elif tgt_lang == "Marathi":
    model, tokenizer = load_translation_model('en', 'mr')
elif tgt_lang == "Bengali":
    model, tokenizer = load_translation_model('en', 'bn')
elif tgt_lang == "Gujarati":
    model, tokenizer = load_translation_model('en', 'gu')
elif tgt_lang == "Tamil":
    model, tokenizer = load_translation_model('en', 'ta')
elif tgt_lang == "Telugu":
    model, tokenizer = load_translation_model('en', 'te')

# Text or Image input
option = st.radio("Select input type", ("Text", "Image"))

if option == "Text":
    text_input = st.text_area("Enter English Text")
    if st.button("Translate"):
        if text_input:
            translated_text = translate_text(model, tokenizer, text_input)
            st.success(f"Translated Text in {tgt_lang}: {translated_text}")
            if st.button("Speak Translation"):
                text_to_speech(translated_text, tgt_lang)
        else:
            st.warning("Please enter some text for translation.")

elif option == "Image":
    uploaded_image = st.file_uploader("Upload an image with text", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        if st.button("Extract and Translate Text"):
            extracted_text = extract_text_from_image(image)
            st.info(f"Extracted Text: {extracted_text}")
            translated_text = translate_text(model, tokenizer, extracted_text)
            st.success(f"Translated Text in {tgt_lang}: {translated_text}")
            if st.button("Speak Translation"):
                text_to_speech(translated_text, tgt_lang)