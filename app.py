import os
import gradio as gr
import google.generativeai as genai

"""**How to get Google Gemini API Key?**

- Go to https://aistudio.google.com/app/api-keys
- Click "Create API Key"
- Copy the API Key for your use
"""

GEMINI_API_KEY="AIzaSyBg1CYTTOfWBrOzgxBhBLqHjujx7qVurrM"
genai.configure(api_key=GEMINI_API_KEY)

"""
- Similar to Gemini Model we can also use HuggingFace Transformer Models.
- Reference links: https://python.langchain.com/docs/integrations/providers/huggingface , https://python.langchain.com/docs/integrations/llms/huggingface_hub.html

"""

# from langchain.llms import HuggingFacePipeline
# hf = HuggingFacePipeline.from_model_id(
#     model_id="gpt2",
#     task="text-generation",)

# Initialize Gemini model
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Custom LLM wrapper for Gemini
class GeminiLLM:
    def __init__(self, model):
        self.model = model
        self.memory_history = []

    def predict(self, user_message):
        # Build conversation context
        full_prompt = "You are a helpful assistant to answer user queries.\n"
        for msg in self.memory_history:
            full_prompt += f"{msg}\n"
        full_prompt += f"User: {user_message}\nChatbot:"

        # Generate response
        response = self.model.generate_content(full_prompt)
        answer = response.text

        # Update memory
        self.memory_history.append(f"User: {user_message}")
        self.memory_history.append(f"Chatbot: {answer}")

        # Keep only last 10 exchanges
        if len(self.memory_history) > 20:
            self.memory_history = self.memory_history[-20:]

        return answer

llm_chain = GeminiLLM(gemini_model)

def get_text_response(user_message,history):
    response = llm_chain.predict(user_message = user_message)
    return response

demo = gr.ChatInterface(get_text_response, examples=["How are you doing?","What are your interests?","Which places do you like to visit?"])

if __name__ == "__main__":
    demo.launch(debug=True) #To create a public link, set `share=True` in `launch()`. To enable errors and logs, set `debug=True` in `launch()`.
