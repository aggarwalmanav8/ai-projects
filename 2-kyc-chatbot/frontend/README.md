# KYC Chatbot Frontend

HTML/JS frontend for the KYC FAQ chatbot. Single-page application with conversation state management.

## Features

- **Chat Interface** — Clean, responsive UI
- **Conversation Memory** — Stores messages in browser (multi-turn)
- **Real-time Formatting** — Markdown formatting support
- **Token Tracking** — Shows tokens used and estimated cost
- **Error Handling** — Graceful error messages

## Setup

### 1. Update Backend URL (if needed)
In `app.js`, change:
```javascript
const API_URL = 'http://localhost:5001';  // Local
// or
const API_URL = 'https://your-railway-url.com';  // Production
```

### 2. Open Locally
Simply open `index.html` in a browser:
```bash
open index.html
```

Or serve with a local HTTP server:
```bash
python3 -m http.server 8000
```
Then visit: http://localhost:8000

## Deployment to Vercel

1. Push code to GitHub
2. Go to https://vercel.com
3. Import your GitHub repo
4. No build step needed (static files)
5. Deploy

## File Structure

- `index.html` — Chat UI markup
- `app.js` — Conversation state and API calls
- `styles.css` — Responsive styling

## How It Works

1. User types a question
2. Frontend adds to `conversationHistory` array
3. Sends entire history to backend API
4. Backend validates and calls Claude
5. Frontend receives response
6. Adds to conversation and displays

## Technologies

- Vanilla JavaScript (no frameworks)
- Fetch API for HTTP requests
- CSS Grid & Flexbox for layout
- Local browser storage (in-memory)

## Cost Awareness

Frontend displays estimated token cost per message. With Claude 3 Haiku:
- ~$0.001 per typical KYC question
- $5 budget = ~5,000 questions