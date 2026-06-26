import os
import httpx

class AIService:
    def __init__(self):
        self.url = os.getenv("ASCLOUD_API_URL")

    async def get_hub_status(self) -> list:
        try:
            async with httpx.AsyncClient(timeout = 4.0) as client:
                response = await client.get(self.url)
                return response.json()
        except Exception as e:
            return []