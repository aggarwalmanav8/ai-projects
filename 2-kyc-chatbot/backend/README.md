# KYC Chatbot Backend

Flask API for the KYC FAQ chatbot. Handles Claude API calls and conversation validation.

## Setup

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env` File
```bash
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

Get your API key from: https://console.anthropic.com

### 4. Run Locally
```bash
python3 app.py
```

Server runs on `http://localhost:5001`

## API Endpoints

### `POST /api/ask`
Ask a KYC question.

**Request:**
```json
{
  "conversation": [
    {"role": "user", "content": "What is KYC?"}
  ]
}
```

**Response:**
```json
{
  "answer": "KYC is...",
  "tokens_used": 145,
  "stop_reason": "end_turn"
}
```

### `GET /api/health`
Health check.

**Response:**
```json
{
  "status": "ok",
  "service": "kyc-chatbot-backend"
}
```

### `GET /api/config`
Get backend configuration.

**Response:**
```json
{
  "max_tokens": 1024,
  "model": "claude-3-haiku-20240307"
}
```

## Deployment to Railway

1. Push code to GitHub
2. Go to https://railway.app
3. Connect GitHub repo
4. Set environment variable: `ANTHROPIC_API_KEY`
5. Deploy

## Technologies

- Flask 3.0.0
- Anthropic Claude API
- Python 3.10+