"""
OpenRouter exposes cloud-hosted LLMs via an API,
so you don’t run the model locally.

How it works:
    1. You Send : user query + top-K products to this OpenRouter API
    2. Get a text response from model. like... — this is your recommendation / explanation

Benefits of using OpenRouter API: No local GPU/CPU usage for LLMs
"""
import requests
import json
from config import (
    LLM_URL,
    LLM_MODEL,
    OPENROUTER_API_KEY
)
from services.prompt import SYSTEM_PROMPT, RECOMMENDATION_PROMPT


class LLMService:

    def get_response(self, user_asked_input, context=""):
        try:
            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": RECOMMENDATION_PROMPT.format(
                        query=user_asked_input,
                        retrieved_context=context
                    )
                }
            ]

            payload = {
                "model": LLM_MODEL,
                "messages": messages,
                "temperature": 0.3,
                "response_format": {
                    "type": "json_object"
                }
            }

            response = requests.post(
                LLM_URL,
                json=payload,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=60
            )

            response.raise_for_status()
            llm_content = response.json()['choices'][0]['message']['content']
            return json.loads(llm_content)
        except json.JSONDecodeError:
            print("LLM returned invalid JSON")
            return {
                "answer": "Unable to generate recommendations.",
                "products": []
            }
        except Exception as e:
            print(f"LLM Error: {e}")

            return {
                "answer": "Something went wrong while generating recommendations.",
                "products": []
            }
