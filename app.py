#rebuild
import os
import gradio as gr
from google import genai

# Load API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found")

client = genai.Client(api_key=GEMINI_API_KEY)

class GeminiLLM:
    def __init__(self):
        self.memory = []

    def predict(self, user_message):
        prompt = (
            "Meet Riya, your youthful and witty personal assistant. "
            "She is friendly, energetic, and helpful.\n"
        )

        for msg in self.memory[-6:]:
            prompt += msg + "\n"

        prompt += f"User: {user_message}\nChatbot:"

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )
            answer = response.text

        except Exception as e:
            answer = f"Gemini error: {str(e)}"

        self.memory.append(f"User: {user_message}")
        self.memory.append(f"Chatbot: {answer}")

        return answer


llm = GeminiLLM()

def get_text_response(message, history):
    return llm.predict(message)


demo = gr.ChatInterface(
    get_text_response,
    examples=[],
)

if __name__ == "__main__":
    demo.launch()

