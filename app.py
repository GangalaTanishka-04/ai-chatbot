import os
import gradio as gr
import google.generativeai as genai

# Configure Gemini using HF Secrets
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Stable model
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

class GeminiLLM:
    def __init__(self, model):
        self.model = model
        self.memory_history = []

    def predict(self, user_message):
        full_prompt = (
            "Meet Riya, your youthful and witty personal assistant! "
            "At 21 years old, she's energetic and eager to help.\n"
        )

        for msg in self.memory_history:
            full_prompt += f"{msg}\n"

        full_prompt += f"User: {user_message}\nChatbot:"

        response = self.model.generate_content(full_prompt)
        answer = response.text

        self.memory_history.append(f"User: {user_message}")
        self.memory_history.append(f"Chatbot: {answer}")

        if len(self.memory_history) > 20:
            self.memory_history = self.memory_history[-20:]

        return answer

llm_chain = GeminiLLM(gemini_model)

def get_text_response(message, history):
    return llm_chain.predict(message)

demo = gr.ChatInterface(
    get_text_response,
    examples=[
        "How are you doing?",
        "What are your interests?",
        "Which places do you like to visit?"
    ]
)

if __name__ == "__main__":
    demo.launch()
