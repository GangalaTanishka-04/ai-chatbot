import os
import gradio as gr
from google import genai

# Get API key from Hugging Face Secrets
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

print("GEMINI_API_KEY loaded:", GEMINI_API_KEY is not None)

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Custom Gemini LLM wrapper
class GeminiLLM:
    def __init__(self):
        self.memory_history = []

    def predict(self, user_message):
        # System prompt
        prompt = (
            "Meet Riya, your youthful and witty personal assistant! "
            "She is energetic, friendly, and helpful.\n"
        )

        # Add last few turns for context
        for msg in self.memory_history[-6:]:
            prompt += msg + "\n"

        prompt += f"User: {user_message}\nChatbot:"

        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            answer = response.text
        except Exception as e:
            answer = "Sorry, something went wrong. Please try again."

        # Update memory
        self.memory_history.append(f"User: {user_message}")
        self.memory_history.append(f"Chatbot: {answer}")

        return answer


llm_chain = GeminiLLM()

def get_text_response(user_message, history):
    return llm_chain.predict(user_message)


demo = gr.ChatInterface(
    get_text_response,
    examples=[],  # IMPORTANT: prevents startup crash
)

if __name__ == "__main__":
    demo.launch()

