"""
OpenRouter exposes cloud-hosted LLMs via an API,
so you don’t run the model locally.

How it works:
    1. You Send : user query + top-K products to this OpenRouter API
    2. Get a text response from model. like... — this is your recommendation / explanation

Benefits of using OpenRouter API: No local GPU/CPU usage for LLMs
"""
import requests

from config import (
    LLM_URL,
    LLM_MODEL,
    OPENROUTER_API_KEY
)
from services.prompt import llm_prompt


class LLMService:

    def get_response(self, user_asked_input, context=""):
        try:
            messages = [{"role": "system", "content": llm_prompt}]
            if context:
                messages.append({"role": "system", "content": context})
            messages.append({"role": "user", "content": user_asked_input})

            response = requests.post(
                LLM_URL,
                json={"model": LLM_MODEL, "messages": messages},
                headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
            )
            print(response.json())
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error getting LLM response: {e}")
            return None
