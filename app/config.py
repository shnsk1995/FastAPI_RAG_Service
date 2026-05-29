"""Application configuration.

Use pydantic-settings (BaseSettings) so all config is sourced from environment
variables. In Lambda, env vars come from the function configuration and from
Secrets Manager / Parameter Store references. Never hard-code secrets.

Settings should be cached with functools.lru_cache so the object is built once
per Lambda container.
"""

# Suggested env vars (define as fields on a Settings class):
#   APP_ENV: "local" | "dev" | "staging" | "prod"
#   LOG_LEVEL: "INFO" | "DEBUG" | "WARNING"
#   AWS_REGION
#
#   # Auth
#   COGNITO_USER_POOL_ID
#   COGNITO_APP_CLIENT_ID
#   JWT_ISSUER
#   JWT_AUDIENCE
#   JWKS_URL                # cached JWKS for token verification
#
#   # LLM
#   ANTHROPIC_API_KEY_SECRET_ARN   # fetched at cold start from Secrets Manager
#   ANTHROPIC_MODEL                # e.g. "claude-opus-4-7"
#   ANTHROPIC_MAX_TOKENS
#   ANTHROPIC_TEMPERATURE
#   PROMPT_CACHE_TTL_SECONDS       # informational; Anthropic cache TTL is fixed
#
#   # Embeddings
#   EMBEDDING_MODEL                # e.g. "voyage-3" or "text-embedding-3-large"
#   EMBEDDING_DIM
#
#   # Vector store
#   VECTOR_STORE_PROVIDER          # "opensearch" | "pinecone" | "pgvector"
#   VECTOR_STORE_ENDPOINT
#   VECTOR_INDEX_NAME
#
#   # Metadata / conversation store
#   DDB_DOCUMENTS_TABLE
#   DDB_CONVERSATIONS_TABLE
#
#   # Semantic cache
#   SEMANTIC_CACHE_ENABLED: bool
#   SEMANTIC_CACHE_REDIS_URL       # ElastiCache (Redis) endpoint
#   SEMANTIC_CACHE_SIMILARITY_THRESHOLD: float    # e.g. 0.95
#   SEMANTIC_CACHE_TTL_SECONDS
#
#   # Ingestion
#   S3_INGESTION_BUCKET
#   S3_PRESIGNED_URL_TTL_SECONDS
#   S3_MAX_UPLOAD_BYTES
#   ALLOWED_MIME_TYPES             # csv list
#   INGESTION_WEBHOOK_URL          # downstream processor
#   INGESTION_WEBHOOK_SECRET_ARN   # HMAC signing key
#
#   # Rate limiting
#   RATE_LIMIT_PER_MINUTE
#
#   # Guardrails
#   GUARDRAILS_PROVIDER            # "bedrock-guardrails" | "presidio" | "custom"
#   GUARDRAILS_POLICY_ID
#
#   # Observability
#   OTEL_EXPORTER_OTLP_ENDPOINT
#   ENABLE_XRAY: bool


# class Settings(BaseSettings): ...
# @lru_cache
# def get_settings() -> "Settings": ...

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    APP_NAME: str = "Chat and Ingestion Service"
    APP_ENV: Literal["local","dev","staging","prod"] = "local"
    #LOG_LEVEL: Literal["INFO","DEBUG","WARNING"] = "INFO"
    AWS_PROFILE: str
    AWS_REGION: str = "us-east-2"
#
    #Auth
    #COGNITO_USER_POOL_ID : str
    #COGNITO_APP_CLIENT_ID : str
    #JWT_ISSUER : str
    #JWT_AUDIENCE : str
    #JWKS_URL : str                # cached JWKS for token verification
#
#   #LLM
    ANTHROPIC_API_KEY : str
    #ANTHROPIC_API_KEY_SECRET_ARN : str   # fetched at cold start from Secrets Manager
    ANTHROPIC_MODEL : str                # e.g. "claude-opus-4-7"
    ANTHROPIC_MAX_TOKENS : int = 1000
    ANTHROPIC_TEMPERATURE : float = 0.5
    #PROMPT_CACHE_TTL_SECONDS  : int = 300     # informational; Anthropic cache TTL is fixed
#
#   # Embeddings
    #EMBEDDING_MODEL : str                # e.g. "voyage-3" or "text-embedding-3-large"
    #EMBEDDING_DIM : int
#
#   # Vector store
    #VECTOR_STORE_PROVIDER : str          # "opensearch" | "pinecone" | "pgvector"
    #VECTOR_STORE_ENDPOINT : str
    #VECTOR_INDEX_NAME : str
#
#   # Metadata / conversation store
    #DDB_DOCUMENTS_TABLE : str
    DDB_CONVERSATIONS_TABLE : str | None = None
    CHAT_HISTORY_LIMIT: int = 20
#
#   # Semantic cache
    #SEMANTIC_CACHE_ENABLED: bool = False
    #SEMANTIC_CACHE_REDIS_URL : str       # ElastiCache (Redis) endpoint
    #SEMANTIC_CACHE_SIMILARITY_THRESHOLD: float    # e.g. 0.95
    #SEMANTIC_CACHE_TTL_SECONDS : int = 3600 * 48
#
#   # Ingestion
    #S3_INGESTION_BUCKET : str
    #S3_PRESIGNED_URL_TTL_SECONDS : int = 300
    #S3_MAX_UPLOAD_BYTES : int = 5 * 1024 * 1024
    #ALLOWED_MIME_TYPES : str             # csv list
    #INGESTION_WEBHOOK_URL : str       # downstream processor
    #INGESTION_WEBHOOK_SECRET_ARN : str   # HMAC signing key
#
#   # Rate limiting
    #RATE_LIMIT_PER_MINUTE : int = 100
#
#   # Guardrails
    #GUARDRAILS_PROVIDER : str = "bedrock-guardrails"            # "bedrock-guardrails" | "presidio" | "custom"
    #GUARDRAILS_POLICY_ID : str
#
#   # Observability
    #OTEL_EXPORTER_OTLP_ENDPOINT : str
    #ENABLE_XRAY: bool

    #Prompts
    ANTHROPIC_SYSTEM_PROMPT: str = (
    "You are a helpful AI assistant for a chat and document ingestion application. "
    "Answer clearly, briefly, and accurately. "
    "If you do not know the answer, say that you do not know."
    )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()