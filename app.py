import os
import gradio as gr
from google import genai

# Load API key from Hugging Face Secrets
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

class GeminiLLM:
    def __init__(self):
        self.memory = []

    def predict(self, user_message):
        # System prompt
        prompt = (
            "Meet Riya, your youthful and witty personal assistant. "
            "She is friendly, energetic, and helpful.\n"
        )

        # Add limited memory
        for msg in self.memory[-6:]:
            prompt += msg + "\n"

        prompt += f"User: {user_message}\nChatbot:"

        try:
            response = client.generate_content(
                model="gemini-1.0-pro",
                contents=prompt
            )

            if not response or not response.text:
                raise ValueError("Empty response from Gemini")

            answer = response.text

        except Exception as e:
            answer = f"Gemini error: {str(e)}"

        # Update memory
        self.memory.append(f"User: {user_message}")
        self.memory.append(f"Chatbot: {answer}")

        return answer


llm = GeminiLLM()

def get_text_response(message, history):
    return llm.predict(message)


demo = gr.ChatInterface(
    get_text_response,
    examples=[],  # IMPORTANT: avoids HF startup crash
)

if __name__ == "__main__":
    demo.launch()

