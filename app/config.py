"""Configuration via variables d'environnement (.env en local, dashboard Render en prod)."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "dev"                                  # dev | prod
    database_url: str = "sqlite:///./dev.db"          # Postgres sur Render (injecté par render.yaml)
    secret_key: str = "dev-secret-change-me"          # signe le cookie de la porte
    access_code: str = "fes2026"                      # code commun invités (changer en prod !)
    gate_cookie_name: str = "kj_gate"
    gate_max_age: int = 90 * 24 * 3600                # 90 jours

    class Config:
        env_file = ".env"


settings = Settings()
