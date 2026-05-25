"""
OpenRouter exposes cloud-hosted LLMs via an API,
so you don’t run the model locally.

How it works:
    1. You Send : user query + top-K products to this OpenRouter API
    2. Get a text response from model. like... — this is your recommendation / explanation

Benefits of using OpenRouter API: No local GPU/CPU usage for LLMs
"""

import requests

from config import llm_model, API_KEY, url
from prompt import LLM_PROMPT

payload = {
    "model": llm_model,
    "messages": [
        {"role": "system", "content": LLM_PROMPT},
        {"role": "user",
         "content": str(input())}
    ]
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
recommendation = response.json()['choices'][0]['message']['content']
print(recommendation)
