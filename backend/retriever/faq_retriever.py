from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DataFrameLoader
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

from pathlib import Path
from backend.db.db_connector import get_faq_data

# Project Root
BASE_DIR = Path(__file__).resolve().parent      # Örn: backend/db
PROJECT_DIR = BASE_DIR.parent.parent 

load_dotenv(dotenv_path=PROJECT_DIR / ".env")
db_path = PROJECT_DIR / "database" / "insurance.db"

def create_retriever():
    # Load environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Prepare the data
    df = get_faq_data(db_path=str(db_path))
    df["content"] = df["question"] + "\n" + df["answer"]
    loader = DataFrameLoader(df, page_content_column="content")
    documents = loader.load()

    # Embedding ve retriever
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(documents, embeddings)

    # LLM ve memory
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Create QA chain (with memory support)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=False,
        output_key="answer"
    )

    return qa_chain
