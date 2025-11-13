from backend.retriever.faq_retriever import create_retriever
from backend.query_understanding.intent_recognition import extract_intent
from backend.query_understanding.intent_router import route_intent_to_table
from backend.db.sql_agent import get_sql_response


#  QA chain is created at the beginning, memory is preserved in each call
qa = create_retriever()


def handle_user_query(user_query, chat_history=None):
    intent = extract_intent(user_query)
    print(f"Detected intent: {intent}")

    # If intent is Farewell, directly return a farewell message
    if intent == "Farewell Inquiry":
        return "You're very welcome! If you have any more questions, feel free to ask. Have a great day!"

    # Remaining intent processing
    lowered_query = user_query.strip().lower()

    faq_keywords = ["what is", "how can i", "how do i", "definition", "meaning"]
    if any(kw in lowered_query for kw in faq_keywords):
        selected_table = "FAQ"
        print("🔁 Overridden to FAQ based on keywords.")
    else:
        selected_table = route_intent_to_table(intent)

    print(f"Routing to table: {selected_table}")

    if selected_table == "FAQ":
        try:
            result = qa({"question": user_query})
            print("Final response from retriever:", result)
            return (
                result.get("answer")
                or result.get("result")
                or "Sorry, I couldn't find an answer."
            )
        except Exception as e:
            return f"Retriever failed: {str(e)}"
    else:
        try:
            result = get_sql_response(user_query)
            print("SQL Agent Response:", result)
            return result
        except Exception as e:
            return f"SQL Agent failed: {str(e)}"
