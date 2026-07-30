#rebuild
import os
import gradio as gr
import requests
# Load API key
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not found")

client = genai.Client(api_key=OPENROUTER_API_KEY)

class ChatbotLLM:
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

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": "meta-llama/llama-3.1-8b-instruct:free",
            "messages": [
                {
                    "role": "system",
                    "content": "Meet Riya, your youthful and witty personal assistant. She is friendly, energetic and helpful."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
        
            response.raise_for_status()
        
            answer = response.json()["choices"][0]["message"]["content"]
        
        except Exception as e:
            answer = f"Error: {e}"

        self.memory.append(f"User: {user_message}")
        self.memory.append(f"Chatbot: {answer}")

        return answer


llm = ChatbotLLM()

def get_text_response(message, history):
    return llm.predict(message)


demo = gr.ChatInterface(
    get_text_response,
    examples=[],
)

if __name__ == "__main__":
    demo.launch()

