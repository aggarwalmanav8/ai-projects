# Document Classifier Backend

Flask API for KYC document classification using OpenAI function calling and Pydantic validation.

## Quick Start

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env
echo "OPENAI_API_KEY=sk-..." > .env

# Test locally
python3 test_classifier.py

# Run server
python3 app.py
# http://localhost:5000/health
```

## API Endpoints

### POST /classify

Classify a KYC document from free-text description.

**Request:**
```json
{
  "description": "Passport with name John Doe, DOB 15-05-1990, expiry 2030"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "doc_type": "passport",
    "doc_type_confidence": 0.95,
    "name": "John Doe",
    "name_confidence": 0.95,
    "dob": "15-05-1990",
    "dob_confidence": 0.95,
    "action": "approve"
  }
}
```

**Errors:**
- `400` — Missing/invalid input
- `500` — Server error

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## How It Works

### 1. Input Validation

```python
if not data or "description" not in data:
    return error 400

if len(description) < 10:
    return error 400
```

### 2. OpenAI Function Calling

LLM is constrained by strict schema:

```python
{
  "doc_type": enum ["pan", "aadhaar", "passport", "voterid", "dl"],
  "doc_type_confidence": float 0-1,
  "name": string or null,
  "name_confidence": float 0-1,
  "dob": string (DD-MM-YYYY) or null,
  "dob_confidence": float 0-1
}
```

### 3. Pydantic Validation

LLM output validated against schema:

```python
classification = DocumentClassification(**arguments)
# Raises ValidationError if invalid
```

### 4. Backend Action Logic

**Critical:** Backend computes action, not LLM.

```python
min_confidence = min(doc_type_conf, name_conf, dob_conf)

if min_confidence >= 0.75:
    action = "approve"      # All scores high
elif min_confidence >= 0.5:
    action = "needs_review" # Some scores low
else:
    action = "decline"      # Any score very low
```

**Why?** Regulatory compliance. LLMs hallucinate. This is auditable.

## Architecture

Request → Validation → OpenAI Function Call → Pydantic Validation → Action Logic → JSON Response

## Configuration

**Environment Variables:**

| Variable | Required | Default |
|----------|----------|---------|
| `OPENAI_API_KEY` | Yes | — |
| `FLASK_ENV` | No | development |
| `PORT` | No | 5000 |

## Files

- **`app.py`** — Flask app, endpoints, error handling
- **`classifier.py`** — Core logic (schema, OpenAI call, validation)
- **`test_classifier.py`** — 5 test scenarios
- **`requirements.txt`** — Dependencies

## Testing

```bash
python3 test_classifier.py
```

Expected output:
Test 1: Valid passport → approve ✅
Test 2: Blurry PAN → decline ❌
Test 3: Clear Aadhaar → approve ✅
Test 4: Torn VoterID → decline ❌
Test 5: Fake DL → decline ❌

## Deployment (Railway)

1. Push to GitHub
2. railway.app → New Project → Deploy from Git
3. Root directory: `3-document-classifier/backend`
4. Environment: `OPENAI_API_KEY=sk-...`
5. Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

## Dependencies

- **Flask 3.0.0** — Web framework
- **OpenAI 0.27.8** — GPT-4o API (legacy SDK, Zscaler compatible)
- **Pydantic 2.11.0** — Schema validation
- **python-dotenv 1.0.0** — `.env` loading
- **Gunicorn 21.2.0** — Production server
- **flask-cors 4.0.0** — Cross-origin requests

**Why 0.27.8?** Newer versions (1.x+) use httpx which has Zscaler proxy issues. Older SDK uses requests library (works fine with Zscaler certs).

## Error Handling

**Validation Error:**
```json
{
  "success": false,
  "error": "Classification validation failed",
  "details": "value is not a valid number"
}
```

**Missing Field:**
```json
{
  "success": false,
  "error": "Missing 'description' field"
}
```

**Server Error:**
```json
{
  "success": false,
  "error": "Server error",
  "details": "..."
}
```

## Performance

- **Latency:** 2-3 seconds (OpenAI API call)
- **Throughput:** ~10 classifications/second (single instance)
- **Cost:** ~$0.003 per classification

## Design Decisions

### Why Pydantic?

Type safety before touching your code. Catches LLM mistakes early.

### Why Decouple Action Logic?

LLM scores confidence. Backend decides approval. Clean separation of concerns.

### Why Strict Confidence Thresholds?

Deterministic, auditable, tweakable. Change 0.75 → 0.80 without retraining.

### Why DD-MM-YYYY Format?

Consistent format for downstream systems. Validation catches format errors.

## Future Work

- Add OCR integration (image → text)
- Add face matching (identity verification)
- Add fraud detection signals
- Store audit trail in database
- Multi-provider fallback (Gemini if OpenAI unavailable)

## Support

Check Railway logs:
```bash
railway logs --service 3-document-classifier
```

Or test locally:
```bash
python3 app.py  # Debug mode
```
