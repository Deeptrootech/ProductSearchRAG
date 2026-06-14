import requests
from config import LLM_MODEL, LLM_URL, OPENROUTER_API_KEY
from services.prompt import INTENT_PROMPT


class IntentService:

    def extract_intent(self, query):
        messages = [
            {
                "role": "system",
                "content": INTENT_PROMPT
            },
            {
                "role": "user",
                "content": query
            }
        ]

        payload = {
            "model": LLM_MODEL,
            "messages": messages,
            "temperature": 0,
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
            }
        )

        return response.json()["choices"][0]["message"]["content"]
