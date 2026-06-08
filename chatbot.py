#!/usr/bin/env python3
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

def stream_response(user_message: str) -> None:
    """
    Stream a response from GPT-4o for the given user message.
    
    Args:
        user_message: The user's question/prompt
    """
    try:
        # Create streaming message
        # Key insight: stream=True enables real-time token delivery
        with client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            stream=True
        ) as stream:
            # Iterate through tokens as they arrive from the API
            for chunk in stream:
                # Extract text from chunk
                delta = chunk.choices[0].delta
                if delta.content:
                    print(delta.content, end="", flush=True)
        
        print()  # Newline after response completes
    
    except KeyboardInterrupt:
        print("\n[Chat interrupted by user]")
        sys.exit(0)
    except Exception as e:
        print(f"\n[Error: {e}]", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main loop: accept input and stream responses."""
    print("🤖 CLI Chatbot (Ctrl+C to exit)")
    print("-" * 40)

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            print("Bot: ", end="", flush=True)
            stream_response(user_input)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            # Handle pipe input (non-interactive)
            break


if __name__ == "__main__":
    main()