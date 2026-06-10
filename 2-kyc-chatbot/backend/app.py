"""
KYC FAQ Chatbot Backend
Stateless Flask API that calls Claude and returns answers.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables (.env file)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to call this backend from different domain

# Initialize Claude client
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in .env")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Configuration
MAX_TOKENS = 1024
SYSTEM_PROMPT = """You are a helpful KYC (Know Your Customer) expert assistant.
Your role is to answer common questions about onboarding, document requirements, and verification.
Keep answers concise (under 150 words) and clear."""

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_conversation_format(conversation):
    """
    Validate that conversation is a list of properly formatted messages.
    
    Returns: (is_valid, error_message)
    """
    # Check if conversation is a list
    if not isinstance(conversation, list):
        return False, "conversation must be a list"
    
    # Check each message in the conversation
    for i, msg in enumerate(conversation):
        # Each message must be a dictionary
        if not isinstance(msg, dict):
            return False, f"message {i} is not a dictionary"
        
        # Each message must have 'role' and 'content'
        if "role" not in msg or "content" not in msg:
            return False, f"message {i} missing 'role' or 'content' field"
        
        # Role must be either 'user' or 'assistant'
        if msg["role"] not in ["user", "assistant"]:
            return False, f"message {i} has invalid role '{msg['role']}'"
        
        # Content must be a string
        if not isinstance(msg["content"], str):
            return False, f"message {i} content must be a string"
        
        # Content cannot be empty
        if not msg["content"].strip():
            return False, f"message {i} content cannot be empty"
    
    return True, None


def validate_request_payload(data):
    """
    Validate the entire request payload.
    
    Returns: (is_valid, error_message)
    """
    # Check if data exists
    if not data:
        return False, "request body cannot be empty"
    
    # Check if 'conversation' field exists
    if "conversation" not in data:
        return False, "request must contain 'conversation' field"
    
    # Validate the conversation format
    return validate_conversation_format(data["conversation"])

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """
    Main endpoint: Receive conversation history, call Claude, return answer.
    
    Request body:
    {
        "conversation": [
            {"role": "user", "content": "What documents do I need?"},
            {"role": "assistant", "content": "..."}
        ]
    }
    
    Response:
    {
        "answer": "You need...",
        "tokens_used": 234,
        "stop_reason": "end_turn"
    }
    """
    try:
        # Step 1: Get JSON data from request
        data = request.get_json()
        
        # Step 2: Validate the request
        is_valid, error_msg = validate_request_payload(data)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        conversation = data["conversation"]
        
        # Step 3: Call Claude API
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=conversation
        )
        
        # Step 4: Extract answer and token count
        answer = response.content[0].text
        tokens_used = response.usage.output_tokens + response.usage.input_tokens
        
        # Step 5: Return success response
        return jsonify({
            "answer": answer,
            "tokens_used": tokens_used,
            "stop_reason": response.stop_reason
        }), 200
    
    except Exception as e:
        # Catch unexpected errors
        print(f"Error in /api/ask: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    

@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint for monitoring.
    Returns: {"status": "ok"}
    """
    return jsonify({"status": "ok", "service": "kyc-chatbot-backend"}), 200


@app.route('/api/config', methods=['GET'])
def get_config():
    """
    Return frontend configuration (limits, model info, etc.)
    Frontend uses this to know the constraints.
    
    Returns: {
        "max_tokens": 1024,
        "model": "claude-3-haiku-20241022"
    }
    """
    return jsonify({
        "max_tokens": MAX_TOKENS,
        "model": "claude-haiku-4-5-20251001"
    }), 200

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle requests to non-existent endpoints."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle wrong HTTP method (e.g., GET to POST endpoint)."""
    return jsonify({"error": "Method not allowed"}), 405


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == '__main__':
    print("Starting KYC Chatbot Backend...")
    print("Flask server running on http://localhost:5000")
    print("Available endpoints:")
    print("  POST /api/ask - Ask a KYC question")
    print("  GET /api/health - Health check")
    print("  GET /api/config - Get configuration")
    
    # Start Flask server
    app.run(debug=True, host='0.0.0.0', port=5001)