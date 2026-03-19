🤖 EVEREST – College Chatbot

EVEREST is an AI-powered chatbot built for Padmashree Institute of Management & Sciences (PIMS).
It provides accurate and context-based answers about admissions, courses, facilities, and campus information using a RAG (Retrieval-Augmented Generation) system.

🚀 Features

AI chatbot powered by OpenAI

Context-aware answers using college data

Semantic search with Pinecone

Clean and interactive UI

Easy integration into websites

🛠️ Tech Stack

Backend: Flask

LLM: OpenAI

Embeddings: HuggingFace (MiniLM)

Vector Database: Pinecone

Framework: LangChain

Frontend: HTML, CSS, JavaScript

⚙️ Setup Instructions


1. Clone the repository
git clone https://github.com/your-username/college-chatbot.git
cd college-chatbot



2. Install dependencies
pip install -r requirements.txt


3. Create .env file
PINECONE_API_KEY=your_pinecone_api_key
OPENAI_API_KEY=your_openai_api_key


4. Upload data to Pinecone
python store_index.py


5. Run the application
python app.py


Open in browser:

http://127.0.0.1:8080
💡 Example Queries

What is the admission process?

Does PIMS provide hostel facilities?

Where is the college located?

📌 Notes

First response may take a few seconds due to model initialization

Use gpt-4o-mini for faster responses


👨‍💻 Author

Bimlesh Sah
GitHub: @sahbimlesh9