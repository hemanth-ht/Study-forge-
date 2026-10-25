import os
import json
import fitz  # PyMuPDF
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.title("StudyForge")
st.write("Turn your notes into flashcards.")

pdf = st.file_uploader("Upload a PDF", type="pdf")
notes = st.text_area("Or paste your notes")

text = ""
if pdf:
    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    text = "".join(page.get_text() for page in doc)
elif notes:
    text = notes

if st.button("Generate flashcards") and text:
    with st.spinner("Generating..."):
        msg = client.messages.create(
            model="claude-fable-5-1",
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": "Create 10 flashcards from this text. Reply ONLY with a JSON list "
                           'like [{"q": "...", "a": "..."}].\n\n' + text[:8000],
            }],
        )
    cards = json.loads(msg.content[0].text)
    for i, c in enumerate(cards, 1):
        with st.expander(f"Card {i}: {c['q']}"):
            st.write(c["a"])
