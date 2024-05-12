from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY,
)

def request_completion(messages, model="llama3-8b-8192", max_tokens=500):
    chat_completion = client.chat.completions.create(model=model, messages=messages, max_tokens=max_tokens)
    completion = chat_completion.choices[0].message.content
    return completion
