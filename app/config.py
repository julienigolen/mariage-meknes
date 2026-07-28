"""Configuration via variables d'environnement (.env en local, dashboard Render en prod)."""
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "dev"                                  # dev | prod
    database_url: str = "sqlite:///./dev.db"          # Postgres sur Render (injecté par render.yaml)
    secret_key: str = "dev-secret-change-me"          # signe le cookie de la porte
    access_code: str = "meknes2026"                   # code commun invités (changer en prod !)
    gate_cookie_name: str = "kj_gate"
    gate_max_age: int = 90 * 24 * 3600                # 90 jours
    household_cookie_name: str = "kj_household"       # foyer reconnu (entrée par tel ou RSVP) — feedback 2026-07-29

    @field_validator("database_url")
    @classmethod
    def _use_psycopg3(cls, url: str) -> str:
        """Render injecte `postgres://…` → SQLAlchemy choisirait psycopg2 (absent).
        On force le driver psycopg v3, le seul installé."""
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+psycopg://", 1)
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url

    class Config:
        env_file = ".env"


settings = Settings()
