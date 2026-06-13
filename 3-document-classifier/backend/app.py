from flask import Flask, request, jsonify
from flask_cors import CORS
from classifier import classify_document
import os

app = Flask(__name__)
CORS(app)

@app.route("/classify", methods=["POST"])
def classify():
    """
    Endpoint: POST /classify
    Body: {"description": "I have a passport with..."}
    Response: {"success": true, "data": {...}}
    """
    try:
        data = request.get_json()
        
        if not data or "description" not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'description' field"
            }), 400
        
        description = data["description"].strip()
        if len(description) < 10:
            return jsonify({
                "success": False,
                "error": "Description too short (min 10 characters)"
            }), 400
        
        # Call classifier
        result = classify_document(description)
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Server error",
            "details": str(e)
        }), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)