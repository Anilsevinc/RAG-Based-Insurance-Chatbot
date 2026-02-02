from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=PROJECT_DIR / ".env")

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY not set in .env")


llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)


intent_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are an intelligent assistant for an insurance company. 
Classify the user's intent based on the meaning of their question.

Use the following categories ONLY:

- Policy Inquiry → Questions about insurance policies, such as start/end date, type, coverage, premium, status, or cancellation.
- Claim Inquiry → Questions about insurance claims, such as how to file, current status, amount, claim history, or description.
- Payment Inquiry → Questions about payments, such as amount paid, date, method, or payment status.
- FAQ Inquiry → General questions that do not depend on the user's personal data, such as definitions (e.g. deductible, policy), process questions (e.g. how to cancel), or common insurance knowledge. These answers come from an FAQ database.
- General Inquiry → Greetings, small talk, or unclear intent.

Respond with only the intent category name. Do not explain or elaborate.

Question: {question}
Intent:
"""
)


intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

def extract_intent(user_question):
    result = intent_chain.run(user_question)
    return result.strip()
