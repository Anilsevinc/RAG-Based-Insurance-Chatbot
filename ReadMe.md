

# RAG-based Insurance Chatbot Assistant

A **Retrieval-Augmented Generation (RAG)** based insurance assistant chatbot built with **Python**, **LangChain**, **OpenAI GPT**, and **Gradio**.  
This assistant helps users with insurance queries including policies, claims, payments, and FAQs.

---

## Features

- **Natural Language Understanding**: Classifies user queries into intents such as Policy, Claim, Payment, FAQ, or General inquiries.
- **RAG Architecture**: Combines FAQ retrieval using embeddings with SQL queries for structured data.
- **Context-Aware Responses**: Memory-enabled chatbot remembers previous conversation context (via `faq_retriever`).
- **Interactive Web UI**: Modern dark gradient theme with sample questions and responsive design.
- **Easy Deployment**: Run locally using Python and Gradio.

---

## Project Structure

```text
INSURANCE_CHATBOT_RAG/
├─ backend/
│  ├─ __init__.py
│  ├─ chatbot.py
│  ├─ db/
│  │  ├─ __init__.py
│  │  ├─ db_connector.py
│  │  ├─ db_test.py
│  │  └─ sql_agent.py
│  ├─ query_understanding/
│  │  ├─ __init__.py
│  │  ├─ intent_recognition.py
│  │  └─ intent_router.py
│  └─ retriever/
│     ├─ __init__.py
│     ├─ faq_retriever.py
│     └─ retriever.py
├─ database/
│  └─ insurance.db
├─ frontend/
│  ├─ __init__.py
│  └─ app_chatbot_ui.py
├─ .env
├─ Requirements.txt
├─ Readme.md
└─ venv/
````

---

## Backend Overview

### Intent Recognition (`query_understanding`)

* **`intent_recognition.py`**: Classifies user questions into intents using OpenAI GPT-3.5-turbo.
* **`intent_router.py`**: Routes recognized intent to the correct data source or table.

**Intent categories**:

* Policy Inquiry
* Claim Inquiry
* Payment Inquiry
* FAQ Inquiry
* General Inquiry
* Farewell Inquiry

### Database Handling (`db`)

* **`db_connector.py`**:

  * Connects to SQLite database (`insurance.db`) and fetches FAQ data.
  * Implements SQL queries via LangChain SQL Agent.
  * Requires `.env` with `OPENAI_API_KEY`.

### Retrievers (`retriever`)

* **`faq_retriever.py`**: Memory-enabled retrieval from FAQ using embeddings (FAISS) and conversational context.
* **`retriever.py`**: Standard retrieval QA chain without memory.

### Chatbot Logic (`chatbot.py`)

* Detects user intent and routes query to either:

  * **FAQ retriever** (for general questions), or
  * **SQL Agent** (for structured queries like policy, claims, payments)
* Handles farewell messages and keyword overrides for FAQs.
* Returns response with error handling.

---

## Frontend Overview (`frontend/app_chatbot_ui.py`)

* **Interactive web UI using Gradio**
* Dark gradient theme (purple & navy)
* Chat interface with:

  * Chat history
  * Sample question buttons
  * Send button & Enter key submission
* Responsive layout for desktop and mobile

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Anilsevinc/RAG-Based-Insurance-Chatbot.git
cd INSURANCE_CHATBOT_RAG
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r Requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the Gradio app

```bash
python frontend/app_chatbot_ui.py
```

* The app will launch and provide a shareable link in the console.
* Ask questions about insurance policies, claims, payments, or FAQs.

---

## Usage Example

* Ask: `What is a deductible?` → Returns FAQ-based answer.
* Ask: `When does my car policy expire?` → Returns structured SQL data.
* Ask: `How can I file a claim?` → Returns claim instructions.

---

## License & Credits

* **Author:** Anıl Sevinç
* **License:** MIT (or your preferred license)
* **Note:** Do not commit `.env` or `venv` to GitHub.

---

## Notes

* Ensure your `.env` file contains a valid OpenAI API key.
* The SQLite database `insurance.db` contains all FAQ, policy, claim, and payment data.
* You can customize sample questions in `frontend/app_chatbot_ui.py`.

---

