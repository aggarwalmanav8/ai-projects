# CLI Streaming Chatbot

A minimal, production-ready CLI chatbot that streams GPT-4o responses in real-time.

## Quick Start

### Prerequisites
- Python 3.10 or higher
- OpenAI API key (get one at [platform.openai.com](https://platform.openai.com/api/keys))

### Setup

1. **Clone and enter the repo**
```bash
   git clone https://github.com/YOUR-USERNAME/week1-cli-chatbot.git
   cd week1-cli-chatbot
```

2. **Set up environment**
```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
```

3. **Add your API key**
```bash
   # Create .env file
   cat > .env << 'EOF'
   OPENAI_API_KEY=sk-your-actual-key-here
   EOF
```

4. **Run the chatbot**
```bash
   python3 chatbot.py
```

## Usage
🤖 CLI Chatbot (Ctrl+C to exit)
You: What is artificial intelligence?
Bot: Artificial intelligence (AI) is the simulation of human intelligence...
[streams response in real-time]
You: Explain machine learning
Bot: Machine learning is a subset of AI...

## Architecture & Key Concepts

### Streaming vs. Batch

**Why Streaming?**
- User sees responses immediately (better UX)
- Lower perceived latency
- Can interrupt mid-response
- Natural for chatbots

**How it works:**
```python
with client.chat.completions.create(
    model="gpt-4o",
    stream=True,  # Enable streaming
    messages=[...]
) as stream:
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)
```

Each token arrives individually and is printed immediately instead of waiting for the complete response.

### Tokens

**What are tokens?**
- How OpenAI measures text for billing and rate-limiting
- ~4 characters = 1 token
- Example: "Hello world" = 2 tokens

**Cost implication:**
- Input tokens: $0.005 per 1K tokens
- Output tokens: $0.015 per 1K tokens
- A typical question costs less than $0.01

### Temperature

Temperature controls creativity (0.0 - 2.0):
- **0.0** = Deterministic (always same answer)
- **1.0** = Balanced (default, good for Q&A)
- **2.0** = Creative (highly unpredictable)

This chatbot uses temperature 1.0 for conversational responses.

## Code Structure

**`chatbot.py`**
- `stream_response(user_message)` → Calls OpenAI API and streams response
- `main()` → Main loop that accepts user input and handles errors
- Error handling for KeyboardInterrupt and API failures

**Key design decisions:**
- Uses `.env` file for API key (never hardcode secrets)
- `flush=True` ensures real-time token printing
- `end=""` prevents newlines between tokens
- Graceful error handling with `sys.exit()`

## What You Learned

✅ How to call OpenAI API from Python  
✅ Streaming vs. batch API calls  
✅ Real-time token handling  
✅ Error handling and graceful interrupts  
✅ Environment variable management (API keys)  
✅ Git and GitHub workflow  

## Extending This Chatbot

### Add conversation memory
```python
messages = []  # Accumulate all user/bot exchanges
messages.append({"role": "user", "content": user_input})
response = client.chat.completions.create(model="gpt-4o", messages=messages)
messages.append({"role": "assistant", "content": response.choices[0].message.content})
```

### Add system prompt for custom behavior
```python
messages = [
    {"role": "system", "content": "You are a KYC compliance expert."},
    {"role": "user", "content": user_input}
]
```

### Add temperature control
```python
with client.chat.completions.create(
    model="gpt-4o",
    temperature=0.5,  # More focused
    messages=[...]
) as stream:
    ...
```

## Resources

- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Messages API Documentation](https://platform.openai.com/docs/api-reference/messages)
- [Token counting guide](https://platform.openai.com/docs/guides/tokens)

---