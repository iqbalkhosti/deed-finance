import os


class Config:
    """Application configuration — single source of truth for all settings."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # Email / Dev Mode
    DEV_MODE = os.environ.get("DEV_MODE", "true").lower() == "true"
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@deed.com")

    # LLM Advisor
    LLM_API_KEY = os.environ.get("LLM_API_KEY")
    LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "anthropic")
