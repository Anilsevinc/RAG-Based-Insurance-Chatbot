from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import initialize_agent, AgentType
from langchain.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent.parent

env_path = PROJECT_DIR / ".env"
load_dotenv(dotenv_path=env_path)


db_path = PROJECT_DIR / "database" / "insurance.db"

def get_sql_response(user_query):

    # Use LangChain SQL Agent to send natural language query to SQL table.
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OPENAI_API_KEY not set in .env")

    db = SQLDatabase.from_uri(f"sqlite:///{str(db_path)}")

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=4,  # maximum step limit (prevents infinite loops)
        early_stopping_method="generate",  # stop on error
        agent_kwargs={
            "system_message": """
You are a helpful SQL assistant.
Always inspect the schema before writing a query.
Do NOT assume any column exists unless it's shown in the schema.
If you cannot find what the user asks for, politely say the data is unavailable and STOP.
Do not keep trying invalid queries.
"""
        },
    )

    try:
        return agent_executor.run(user_query)
    except Exception as e:
        return f"Sorry, I couldn't answer due to: {str(e)}"
