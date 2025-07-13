import os
from openai import OpenAI
import logging


class AnalyzeService:
    def __init__(self):
        self.logger = logging.getLogger("Deepseek_service")
        self.endpoint = os.getenv("HF_INFERENCE_API_URL", "https://router.huggingface.co/novita/v3/openai")
        self.model_name = os.getenv("HF_INFERENCE_MODEL", "moonshotai/kimi-k2-instruct")
        self.token = os.getenv("HF_TOKEN")
        if not self.token:
            raise ValueError("HF_TOKEN is not set in environment")
        
        self.client = OpenAI(
            api_key=self.token,
            base_url=self.endpoint
        )

        
    async def classify_category(self, text: str) -> str:
        prompt = (
            f'Определи категорию жалобы: "{text}". '
            'Варианты: техническая, оплата, другое. '
            'Ответ должен быть одним словом на русском языке.'
        )

        return await self._call_moonshot(prompt)

    async def analyze_sentiment(self, text: str) -> str:
        prompt = (
            f'Проанализируй тональность текста: "{text}". '
            'Варианты: positive, negative, neutral. '
            'Если не уверен — ответь "unknown".'
        )

        return await self._call_moonshot(prompt)

    

    async def _call_moonshot(self, prompt: str) -> str:
        try:
            """response = self.client.complete(
                messages=[
                    SystemMessage("You are a helpful assistant."),
                    UserMessage(prompt)
                ],
                temperature=0.0,
                top_p=1.0,
                model=self.model_name
            )
            content = response.choices[0].message.content.strip().lower()"""
            completion = self.client.chat.completions.create(
                model = self.model_name,
                messages = [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            content = completion.choices[0].message.content

            
            self.logger.debug(f"GitHub Inference raw response: {content}")

            if content in ["техническая", "оплата"]:
                return content
            elif content in ["positive", "negative", "neutral"]:
                return content
            else:
                return "другое"

        except Exception as e:
            self.logger.error(f"GitHub Inference API error: {str(e)}", exc_info=True)
            return "другое"

