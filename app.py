import os
import gradio as gr
import requests

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not found")


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
            "HTTP-Referer": "https://huggingface.co",
            "X-Title": "Riya Chatbot"
        }

        payload = {
            "model": "google/gemma-4-26b-a4b-it:free",
            "messages": [
                {
                    "role": "system",
                    "content": "You are Riya, a friendly, witty and helpful AI assistant."
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

        except Exception:
            if 'response' in locals():
                answer = f"{response.status_code}\n{response.text}"
            else:
                answer = "Unknown Error"

        self.memory.append(f"User: {user_message}")
        self.memory.append(f"Chatbot: {answer}")

        return answer


llm = ChatbotLLM()


def get_text_response(message, history):
    return llm.predict(message)


demo = gr.ChatInterface(
    fn=get_text_response,
    title="🤖 Riya AI Assistant",
    description="A friendly conversational AI assistant powered by an open-source LLM.",
    examples=[
        "Tell me about yourself",
        "Plan a Hyderabad trip",
        "Write a Python function to reverse a linked list"
    ]
)

if __name__ == "__main__":
    demo.launch()
