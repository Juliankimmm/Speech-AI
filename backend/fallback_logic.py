import random

def route_intent(intent: str, confidence: float) -> str:
    """
    Route intent to appropriate response with fallback logic
    """
    
    # Low confidence fallback
    if confidence < 0.7:
        fallback_responses = [
            "I'm not sure I understood that correctly. Could you please repeat?",
            "I didn't catch that. Could you say it again?",
            "I'm having trouble understanding. Can you rephrase that?",
            "Sorry, I didn't quite get that. Could you try again?"
        ]
        return random.choice(fallback_responses)
    
    # High confidence intent routing
    responses = {
        "track_package": [
            "I can help you track your package. Let me look up your order details.",
            "Sure! I'll check the status of your delivery right away.",
            "Let me find your tracking information for you."
        ],
        "cancel_order": [
            "I can help you cancel your order. Let me process that for you.",
            "No problem! I'll take care of canceling your order.",
            "I'll help you cancel that order right away."
        ],
        "customer_service": [
            "I'm here to help! What can I assist you with today?",
            "How can I help you with your concern?",
            "I'm ready to assist you. What's the issue?"
        ],
        "greeting": [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Good day! How may I assist you?"
        ],
        "goodbye": [
            "Goodbye! Have a great day!",
            "Thank you for calling. Take care!",
            "Bye! Feel free to reach out anytime."
        ],
        "unknown": [
            "I'm not sure how to help with that. Could you please clarify?",
            "I don't recognize that request. Can you provide more details?",
            "I'm sorry, I don't understand. Could you rephrase your question?"
        ]
    }
    
    # Get responses for the intent
    intent_responses = responses.get(intent, responses["unknown"])
    
    # Return a random response from the appropriate category
    return random.choice(intent_responses)