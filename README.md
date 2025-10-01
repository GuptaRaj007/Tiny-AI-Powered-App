🌟 Features
1. Q&A Bot

Chat with AI using natural language.

Follow-up questions supported — the bot remembers conversation context.

Uses Groq API with LLaMA-3.1 model.

2. Text Summarizer

Summarizes any news article or blog post in 3 sentences.

Supports copy-paste of text for instant summarization.

3. Personal Expense Tracker

Track expenses by category: Food, Rent, Travel, etc.

Shows weekly/monthly summaries.

Generates interactive pie charts to visualize expenses.

4. Document Q&A

Upload PDF, TXT, or image files.

Extracts text using:

PyPDFLoader for PDFs

TextLoader for text files

pytesseract OCR for images

Ask multi-turn questions about uploaded documents — follow-up supported.

⚙️ Setup Instructions
1. Clone the Repository
git clone https://github.com/your-username/tiny-ai-app.git
cd tiny-ai-app

2. Install Python & Dependencies

Ensure Python 3.12+ is installed. Then install required packages:

pip install -r requirements.txt

3. Set Up API Key

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here


Make sure your API key is valid and active.

4. Run the App
streamlit run app.py


Open the URL printed in your terminal ( Example http://localhost:8501).

Use the sidebar to select Q&A Bot, Summarizer, Expense Tracker, or Document Q&A.

📝 CLI Version

cli_app.py provides a command-line interface for the same features (except file upload and OCR).

Run:

python cli_app.py

⚡ Future Improvements I can Work On:- 

Add semantic search with LangChain embeddings for large documents.

Enhance Expense Tracker with monthly reports and charts.

Deploy a more polished ChatGPT-like UI with Streamlit Components.
