from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def request_completion(messages, model="gpt-3.5-turbo", max_tokens=500):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )

    completion = response.choices[0].message.content.strip()
    return completion
