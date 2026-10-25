
import requests

# Our locally installed language model
MODEL = "qwen2:1.5b"
OLLAMA_URL = "http://localhost:11434/api/generate"

# Ask the model a question
question = "Explain how AI agents can help logistics companies."

print("Asking our local AI model...\n")

response = requests.post(
    OLLAMA_URL,
    json={
        "model": MODEL,
        "prompt": question,
        "stream": False
    },
    timeout=180
)

response.raise_for_status()

answer = response.json()["response"]

print("Question:", question)
print("\nAI Response:\n")
print(answer)
