# AIProviderService: 封裝 Google Gemini API 互動
# 實際串接前先以 mock 回傳為主，方便後續單元測試

from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

# CACHE_NAME = ""


class AIProviderService:
    def __init__(self, model_name=None, api_key=None):
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(
            api_key=self.api_key,
            http_options=types.HttpOptions(api_version='v1alpha')
        )
        # self.cache = self._ensure_cache()

    # def _ensure_cache(self):
    #     # 檢查快取是否已存在，若無則建立
    #     caches = list(self.client.caches.list())
    #     for c in caches:
    #         if c.display_name == CACHE_NAME:
    #             return c
    #     # 建立快取
    #     instruction = load_instruction()
    #     print("建立快取內容：", instruction)
    #     cache = self.client.caches.create(
    #         model=self.model_name,
    #         config=types.CreateCachedContentConfig(
    #             display_name=CACHE_NAME,
    #             system_instruction="請嚴格遵守以下角色設定與品牌規範：",
    #             contents=[instruction],
    #             ttl="604800s",  # 7天
    #         )
    #     )
    #     return cache

    # def check_cache(self):
    #     # 詢問AI他的角色，並印出回答
    #     prompt = "請簡述你的角色設定"
    #     response = self.client.models.generate_content(
    #         model=self.model_name,
    #         contents=prompt,
    #         config=types.GenerateContentConfig(cached_content=self.cache.name)
    #     )
    #     answer = response.candidates[0].content.parts[0].text
    #     print("AI角色自述：", answer)
    #     return answer

    @staticmethod
    def extract_h1_title(text: str) -> str:
        import re
        # 支援 markdown H1（# 標記）或 HTML <h1> 標籤
        match = re.search(r'^\s*#\s*(.+)$', text, re.MULTILINE)
        if match:
            return match.group(1).strip()
        match = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    def generate_article(self, prompt: str):
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[prompt]
        )
        return {
            "title": self.extract_h1_title(response.text),
            "content": response.text,
            "ai_model_used": self.model_name,
            "final_prompt": prompt
        }
