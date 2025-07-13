from transformers import pipeline
import torch

# Initialize the intent classification pipeline
# Using a pre-trained sentiment model as a base - you can fine-tune this for your specific intents
classifier = pipeline(
    "text-classification", 
    model="distilbert-base-uncased-finetuned-sst-2-english",
    return_all_scores=True
)

# Custom intent mapping based on keywords and patterns
INTENT_PATTERNS = {
    "track_package": ["track", "package", "order", "delivery", "shipment", "where is", "status"],
    "cancel_order": ["cancel", "stop", "refund", "return", "don't want"],
    "customer_service": ["help", "support", "problem", "issue", "complaint"],
    "greeting": ["hello", "hi", "hey", "good morning", "good afternoon"],
    "goodbye": ["bye", "goodbye", "see you", "talk later"],
    "unknown": []
}

def get_intent(text: str) -> tuple[str, float]:
    """
    Classify intent from text using hybrid approach:
    1. Pattern matching for specific intents
    2. Sentiment analysis for confidence
    """
    try:
        text_lower = text.lower()
        
        # Pattern-based intent detection
        detected_intent = "unknown"
        max_matches = 0
        
        for intent, patterns in INTENT_PATTERNS.items():
            matches = sum(1 for pattern in patterns if pattern in text_lower)
            if matches > max_matches:
                max_matches = matches
                detected_intent = intent
        
        # Use sentiment analysis for confidence scoring
        sentiment_result = classifier(text)[0]
        
        # Calculate confidence based on pattern matches and sentiment confidence
        if max_matches > 0:
            base_confidence = min(0.6 + (max_matches * 0.1), 0.95)
            sentiment_confidence = max([score['score'] for score in sentiment_result])
            confidence = (base_confidence + sentiment_confidence) / 2
        else:
            # Low confidence for unknown intents
            confidence = max([score['score'] for score in sentiment_result]) * 0.5
        
        return detected_intent, confidence
    
    except Exception as e:
        print(f"Error in intent classification: {e}")
        return "unknown", 0.0