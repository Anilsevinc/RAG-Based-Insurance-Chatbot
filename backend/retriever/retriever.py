from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DataFrameLoader
from langchain.chains import RetrievalQA  # <-- Önemli
from dotenv import load_dotenv
import os
from pathlib import Path
from backend.db.db_connector import get_faq_data


BASE_DIR = Path(__file__).resolve().parent     
PROJECT_DIR = BASE_DIR.parent.parent 

load_dotenv(dotenv_path=PROJECT_DIR / ".env")
db_path = PROJECT_DIR / "database" / "insurance.db"

def create_retriever():
    openai_api_key = os.getenv("OPENAI_API_KEY")
 
    # Prepare the data
    df = get_faq_data(db_path=str(db_path))
    df["content"] = df["question"] + "\n" + df["answer"]
    loader = DataFrameLoader(df, page_content_column="content")
    documents = loader.load()

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(documents, embeddings)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)
    
    # Classic RetrievalQA chain without memory
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",              
        retriever=vectorstore.as_retriever(),
        return_source_documents=False
    )

    return qa_chain
