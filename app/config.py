from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # storage
    database_url: str = "sqlite+aiosqlite:///./chatting_bot.db"

    # auth
    jwt_secret: str = "change-me-in-prod"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # llm
    llm_provider: str = "echo"          # "echo" (offline) or "openai"
    openai_api_key: str = ""
    model_name: str = "gpt-4o-mini"     # pick whatever's current/cheap when you build
    max_context_tokens: int = 4000      # the budget a memory strategy must fit inside

    class Config:
        env_file = ".env"


settings = Settings()
