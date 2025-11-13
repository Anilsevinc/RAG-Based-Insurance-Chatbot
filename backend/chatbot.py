from backend.retriever.faq_retriever import create_retriever
from backend.query_understanding.intent_recognition import extract_intent
from backend.query_understanding.intent_router import route_intent_to_table
from pathlib import Path
from dotenv import load_dotenv
import os
import re

# LangChain SQL Agent imports
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import initialize_agent, AgentType
from langchain.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI

# Load environment variables
PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=PROJECT_DIR / ".env")

# Database path
db_path = PROJECT_DIR / "database" / "insurance.db"

# QA chain for FAQ retrieval
qa = create_retriever()

def is_farewell_message(text):
    text = text.strip().lower()
    pattern = r"^(thanks|thank you|that's all|bye|goodbye)$"
    return re.match(pattern, text) is not None

def get_sql_response(user_query):
    """Create a fresh SQL Agent for each query to avoid memory retention."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not set in .env")

    db = SQLDatabase.from_uri(f"sqlite:///{str(db_path)}")
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        openai_api_key=openai_api_key,
    )
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=4,
        early_stopping_method="generate",
        agent_kwargs={
            "extra_prompt_messages": [
                {"role": "system", "content": """
You are a helpful SQL assistant.
Always inspect the schema before writing a query.
Do NOT assume any column exists unless it's shown in the schema.
If you cannot find what the user asks for, politely say the data is unavailable and STOP.
Do not keep trying invalid queries.
Always answer in English.
"""}
            ]
        },
    )

    return agent_executor.run(user_query)

def handle_user_query(user_query, chat_history=None):
    """Main function to handle user queries, route to FAQ or SQL Agent."""
    
    # 1️⃣ Farewell check
    if is_farewell_message(user_query):
        return "You're very welcome! If you have any more questions, feel free to ask. Have a great day!"
    
    # 2️⃣ Intent extraction
    intent = extract_intent(user_query)
    print(f"Detected intent: {intent}")

    # 3️⃣ Determine table based on keywords or intent
    faq_keywords = ["what is", "how can i", "how do i", "definition", "meaning", "how to", "what can i do"]
    lowered = user_query.strip().lower()
    if any(kw in lowered for kw in faq_keywords):
        selected_table = "FAQ"
        print("🔁 Overridden to FAQ based on keywords.")
    else:
        selected_table = route_intent_to_table(intent)

    print(f"Routing to table: {selected_table}")

    # 4️⃣ FAQ query
    if selected_table == "FAQ":
        try:
            result = qa.run(user_query)
            print("Final response from retriever:", result)
            return result or "Sorry, I couldn't find an answer."
        except Exception as e:
            return f"Retriever failed: {str(e)}"
    
    # 5️⃣ SQL query
    else:
        try:
            result = get_sql_response(user_query)
            print("SQL Agent Response:", result)
            return result
        except Exception as e:
            return f"SQL Agent failed: {str(e)}"
