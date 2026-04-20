from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[4]
DATASET_DIR = ROOT_DIR / "datasets" / "sample_corpus"
EVALS_DIR = ROOT_DIR / "datasets" / "evals"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_cors_origins: str = "http://localhost:3000"

    database_url: str = "sqlite:///./citadel.db"
    redis_url: str = "redis://localhost:6379/0"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "citadel_chunks"
    opensearch_url: str = "http://localhost:9200"
    opensearch_index: str = "citadel-documents"
    opensearch_username: str = ""
    opensearch_password: str = ""
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = "password"

    storage_mode: str = Field(default="local", alias="CITADEL_STORAGE_MODE")
    public_app_name: str = Field(default="CITADEL", alias="CITADEL_PUBLIC_APP_NAME")
    public_domain: str = Field(default="Platform Engineering Knowledge", alias="CITADEL_PUBLIC_DOMAIN")
    disable_generation: bool = Field(default=False, alias="CITADEL_DISABLE_GENERATION")
    allow_extractive_fallback: bool = Field(default=True, alias="CITADEL_ALLOW_EXTRACTIVE_FALLBACK")
    query_top_k: int = Field(default=8, alias="CITADEL_QUERY_TOP_K")
    context_max_chunks: int = Field(default=10, alias="CITADEL_CONTEXT_MAX_CHUNKS")
    graph_hops: int = Field(default=1, alias="CITADEL_GRAPH_HOPS")
    retrieval_timeout_seconds: int = Field(default=12, alias="CITADEL_RETRIEVAL_TIMEOUT_SECONDS")
    rerank_top_k: int = Field(default=12, alias="CITADEL_RERANK_TOP_K")
    eval_recall_threshold: float = Field(default=0.8, alias="CITADEL_EVAL_RECALL_THRESHOLD")
    eval_unsupported_claim_threshold: float = Field(
        default=0.05, alias="CITADEL_EVAL_UNSUPPORTED_CLAIM_THRESHOLD"
    )

    generator_provider: str = "extractive"
    openai_base_url: str = ""
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b-instruct-q4_K_M"

    api_auth_mode: str = "disabled"
    api_jwt_audience: str = "citadel"
    api_jwt_issuer: str = "local-dev"

    dataset_dir: Path = DATASET_DIR
    evals_dir: Path = EVALS_DIR

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.api_cors_origins.split(",") if origin.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

