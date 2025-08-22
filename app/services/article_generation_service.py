from app.repositories import KeywordRepository, ArticleRepository, LogRepository
from app.services.prompt_builder import PromptBuilderService
from app.services.ai_provider import AIProviderService

class ArticleGenerationService:
    def __init__(self, db):
        self.db = db
        self.keyword_repo = KeywordRepository(db)
        self.article_repo = ArticleRepository(db)
        self.log_repo = LogRepository(db)
        self.prompt_builder = PromptBuilderService()
        self.ai_provider = AIProviderService()

    def generate_article(self, keyword_id, parameters, custom_prompt=None, is_highly_relevant=False):
        # 1. 將 keyword 狀態設為 processing
        self.keyword_repo.update_status(keyword_id, "processing")
        keyword = self.keyword_repo.get_by_id(keyword_id)
        if not keyword:
            return None
        # 2. 組合 prompt
        prompt = self.prompt_builder.build_prompt(keyword.title, parameters, custom_prompt, is_highly_relevant)
        # 3. 呼叫 AI 生成
        try:
            ai_result = self.ai_provider.generate_article(prompt)
            # 4. 寫入 articles
            article = self.article_repo.create(
                keyword_id=keyword_id,
                status="pending_review",
                title=ai_result["title"],
                content=ai_result["content"],
                parameters=parameters,
                ai_model_used=ai_result["ai_model_used"],
                final_prompt=ai_result["final_prompt"]
            )
            # 5. 寫入 logs
            self.log_repo.create(
                keyword_id=keyword_id,
                article_id=article.id,
                status="success",
                ai_model_used=ai_result["ai_model_used"],
                final_prompt=ai_result["final_prompt"]
            )
            # 6. 更新 keyword 狀態
            self.keyword_repo.update_status(keyword_id, "completed")
            print("文章生成成功:", ai_result)
            return ai_result
        except Exception as e:
            # 失敗流程
            self.log_repo.create(
                keyword_id=keyword_id,
                status="failed",
                error_message=str(e),
                ai_model_used="gemini-1.5-flash",
                final_prompt=prompt
            )
            self.keyword_repo.update_status(keyword_id, "generation_failed")
            return None
