import requests, json
from config import LLM_MODEL, LLM_URL, OPENROUTER_API_KEY
from services.prompt import INTENT_PROMPT


class IntentService:

    def extract_intent(self, query):
        messages = [{"role": "system", "content": INTENT_PROMPT}, {"role": "user", "content": query}]
        payload = {
            "model": LLM_MODEL,
            "messages": messages,
            "temperature": 0,
            "response_format": {"type": "json_object"}
        }
        print(f"=================== Extracting Intent...")
        response = requests.post(
            LLM_URL,
            json=payload,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        print(f"=================== Intent Extracted.... {response.json()}")
        if error_message := response.json().get("error"):
            return error_message.get("message", "Unknown error"), False
        intent_text = response.json()["choices"][0]["message"]["content"]
        print(f"++++++++++++++++++++++++++++++++++= {intent_text}")

        try:
            intent = json.loads(intent_text)
        except json.JSONDecodeError:
            print("Invalid intent:", intent_text)

            intent = {
                "search_text": query,
                "product_type": "",
                "category": "",
                "brand": "",
                "required_features": [],
                "filters": [],
                "sort": {
                    "field": "",
                    "order": ""
                }
            }

        return intent, True
