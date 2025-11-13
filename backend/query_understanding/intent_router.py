def route_intent_to_table(intent):
    """
    Intent'e göre hangi tabloya yönlendirme yapılacağını belirler.
    """
    intent_table_map = {
        "Policy Inquiry": "Policies",
        "Claim Inquiry": "Claims",
        "Payment Inquiry": "Payments",
        "FAQ Inquiry": "FAQ",
        "General Inquiry": "FAQ",
        "Farewell Inquiry": "Farewell"
    }
    return intent_table_map.get(intent, "FAQ")
