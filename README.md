# AI Chatbot

A conversational AI chatbot built using Python and Gradio, powered by OpenRouter's API. The chatbot maintains short-term conversation context to provide more natural and coherent responses.

## Live Demo

Hugging Face Space:
https://huggingface.co/spaces/Tanishka-1004/myChatbot

## Features

- Conversational AI interface
- Context-aware responses using conversation history
- Clean Gradio web interface
- API integration through OpenRouter
- Secure API key management using environment variables
- Deployable on Hugging Face Spaces

## Tech Stack

- Python
- Gradio
- OpenRouter API
- Requests

## Project Structure

```
ai-chatbot/
│── app.py
│── requirements.txt
│── README.md
│── images/
│   ├── home.png
│   └── chat.png
```

## Installation

Clone the repository

```bash
git clone https://github.com/GangalaTanishka-04/ai-chatbot.git
```

Go to the project directory

```bash
cd ai-chatbot
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create an environment variable

```
OPENROUTER_API_KEY=your_api_key
```

Run

```bash
python app.py
```

## Future Improvements

- Streaming responses
- Multiple AI model selection
- Chat history export
- Dark mode
- Voice input/output

## Author

Gangala Tanishka

GitHub:
https://github.com/GangalaTanishka-04
