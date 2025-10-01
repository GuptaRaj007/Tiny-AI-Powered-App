import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.docstore.document import Document
import pytesseract
from PIL import Image

# Load .env file
load_dotenv()

# Get API Key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("❌ GROQ_API_KEY not found. Add it to your .env file.")
else:
    client = Groq(api_key=api_key)

# ---------------- Helper Functions ----------------

def ask_ai(question, history=None):
    """Ask Groq AI with optional conversation history"""
    messages = history.copy() if history else []
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )
    return response.choices[0].message.content

def summarize(text):
    return ask_ai(f"Summarize this in 3 sentences:\n{text}")

def render_expenses(expenses):
    if not expenses:
        st.write("No expenses yet.")
        return
    df = {}
    for cat, amt in expenses:
        df[cat] = df.get(cat, 0) + amt
    
    st.write("### Expense Summary")
    st.write(df)
    
    # Pie chart
    fig, ax = plt.subplots()
    ax.pie(df.values(), labels=df.keys(), autopct="%1.1f%%")
    st.pyplot(fig)

def process_uploaded_file(uploaded_file):
    """Extract text from uploaded PDFs, TXT, or images"""
    text_content = ""
    if uploaded_file.type == "application/pdf":
        loader = PyPDFLoader(uploaded_file.name)
        docs = loader.load()
        text_content = "\n".join([d.page_content for d in docs])
    elif uploaded_file.type.startswith("text/"):
        loader = TextLoader(uploaded_file.name)
        docs = loader.load()
        text_content = "\n".join([d.page_content for d in docs])
    elif uploaded_file.type.startswith("image/"):
        image = Image.open(uploaded_file)
        text_content = pytesseract.image_to_string(image)
    else:
        st.warning("Unsupported file type.")
    return text_content

# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="Tiny AI App", page_icon="🤖", layout="wide")
st.sidebar.title("Tiny AI App")
mode = st.sidebar.radio("Choose Mode:", ["Q&A Bot", "Summarizer", "Expense Tracker", "Document Q&A"])
st.title("🤖 Tiny AI App")

# ---------------- Q&A BOT ----------------
if mode == "Q&A Bot":
    st.subheader("Chat with AI (Follow-ups supported)")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Type your question...")
    if user_input:
        answer = ask_ai(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    for msg in st.session_state.chat_history:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.write(msg["content"])

# ---------------- SUMMARIZER ----------------
elif mode == "Summarizer":
    st.subheader("Summarize any text")
    text = st.text_area("Paste article/blog here")
    if st.button("Summarize"):
        if text.strip():
            summary = summarize(text)
            st.success(summary)

# ---------------- EXPENSE TRACKER ----------------
elif mode == "Expense Tracker":
    st.subheader("Track your expenses")
    if "expenses" not in st.session_state:
        st.session_state.expenses = []
    
    cat = st.text_input("Category (food, rent, travel)")
    amt = st.number_input("Amount", min_value=0.0, step=10.0)
    
    if st.button("Add Expense"):
        if cat and amt > 0:
            st.session_state.expenses.append((cat, amt))
            st.success("Expense added!")
    
    render_expenses(st.session_state.expenses)

# ---------------- DOCUMENT Q&A ----------------
elif mode == "Document Q&A":
    st.subheader("Upload a document or image to query it")

    if "doc_text" not in st.session_state:
        st.session_state.doc_text = ""
    if "doc_chat_history" not in st.session_state:
        st.session_state.doc_chat_history = []

    uploaded_file = st.file_uploader("Upload PDF, TXT, or Image", type=["pdf", "txt", "png", "jpg", "jpeg"])
    
    if uploaded_file:
        st.session_state.doc_text = process_uploaded_file(uploaded_file)
        if st.session_state.doc_text:
            st.text_area("Extracted Text", st.session_state.doc_text[:2000], height=200)
    
    query = st.text_input("Ask a question about this document:")
    if st.button("Ask Document Question") and query.strip() and st.session_state.doc_text:
        answer = ask_ai(
            f"Answer based on this document:\n{st.session_state.doc_text}\n\nQuestion: {query}",
            st.session_state.doc_chat_history
        )
        st.session_state.doc_chat_history.append({"role": "user", "content": query})
        st.session_state.doc_chat_history.append({"role": "assistant", "content": answer})
        st.success(answer)

    # Display chat history for document Q&A
    for msg in st.session_state.doc_chat_history:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.write(msg["content"])
