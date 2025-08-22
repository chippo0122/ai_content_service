# PromptBuilderService: 根據參數組合 prompt
import os

INSTRUCTION_PATH = os.path.join(os.path.dirname(__file__), "../prompt/instruction.json")

def load_instruction():
    with open(INSTRUCTION_PATH, "r", encoding="utf-8") as f:
        return f.read()

class PromptBuilderService:
    WRITING_STYLES = [
        "專業報導式",
        "第一人稱經驗分享",
        "輕鬆對話體",
        "條列式懶人包",
    ]
    EMOTIONS = [
        "客觀中立",
        "興奮期待",
        "溫暖療癒",
        "幽默風趣",
    ]
    AUDIENCES = [
        "大學生社團幹部",
        "企業福委會/人資",
        "有親子活動需求的家庭",
        "情侶/朋友",
        "遠端工作者",
        "一般大眾",
    ]

    def __init__(self):
        self.instruction = load_instruction()

    def build_prompt(self, keyword: str, parameters: dict, custom_prompt: str = None, is_highly_relevant: bool = False):
        import json
        # 將 instruction 讀成 dict
        instruction_dict = json.loads(self.instruction)
        style = self.WRITING_STYLES[parameters.get("writing_style", 0)]
        emotion = self.EMOTIONS[parameters.get("emotion", 0)]
        audience = self.AUDIENCES[parameters.get("audience", 0)]
        cta = "請在文中帶入業配。" if is_highly_relevant else ""
        if custom_prompt is None:
            custom_prompt = ""
        prompt_dict = {
            "撰寫輸入參數": {
                "關鍵字": keyword,
                "寫作風格": style,
                "情緒": emotion,
                "受眾": audience,
                "細部指引": custom_prompt,
                "商業連結": cta
            }
        }
        # 合併 instruction_dict 與 prompt_dict
        full_prompt = {**instruction_dict, **prompt_dict}
        return json.dumps(full_prompt, ensure_ascii=False)
