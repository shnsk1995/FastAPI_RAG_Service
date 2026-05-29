# Backend — Full-Stack Gen AI RAG App

Production-grade RAG backend designed to run on AWS Lambda behind API Gateway.
Two logical services share one codebase:

- **Chat service** — `/api/v1/chat/*` — retrieves grounded context and answers
  with Claude. Pipeline: input guardrails → semantic cache → RBAC-filtered
  retrieval → prompt caching → LLM → output guardrails.
- **Ingestion service** — `/api/v1/ingestion/*` — issues S3 presigned upload
  URLs; receives an S3-event webhook on upload completion; parses, chunks,
  embeds, and indexes the document into the vector store.

## Layout

    app/
      main.py               FastAPI factory
      config.py             pydantic-settings (env-driven)
      dependencies.py       shared DI providers
      exceptions.py         domain errors + handlers
      api/
        deps.py             service-level providers
        v1/
          router.py         aggregates v1 sub-routers
          chat.py           chat endpoints
          ingestion.py      presigned URL + webhook
          health.py         liveness / readiness
      core/
        logging.py          structlog config
        security.py         JWT verification
        rbac.py             scope + document ACL
        guardrails.py       input / output checks
        middleware.py       request context, auth, rate limit
      services/
        chat_service.py     chat orchestration
        retriever.py        hybrid retrieval + rerank
        prompt_builder.py   Anthropic prompt caching layout
        llm_client.py       Anthropic wrapper + retries
        semantic_cache.py   embedding-keyed response cache
        ingestion_service.py  upload-url + process pipeline
        parser.py           per-mime document parsers
        chunker.py          semantic chunking
        embedder.py         batched embeddings
        indexer.py          vector upsert / delete
      schemas/              Pydantic request / response
      repositories/         vector store, DDB, Redis
      integrations/         S3, webhook, Secrets Manager
    lambda_handler.py       Mangum entry for API Gateway
    tests/                  (to be populated)

## Deployment shape

    Client
      │
      ▼
    API Gateway (HTTP API) ── Cognito authorizer ──┐
      │                                            │
      ▼                                            ▼
    Lambda: chat-service (this app)        Lambda: ingestion-api (this app)
      │                                            │
      ├─► Anthropic API                            └─► S3 (presigned PUT)
      ├─► OpenSearch / Pinecone                            │
      ├─► ElastiCache Redis (semantic cache)               ▼
      └─► DynamoDB (conversations)                  S3 ObjectCreated
                                                          │
                                                          ▼
                                          EventBridge ──► Webhook (HMAC)
                                                          │
                                                          ▼
                                              Lambda: ingestion-worker
                                              (calls IngestionService.process_upload)

## Local dev

    uv sync
    uv run uvicorn app.main:app --reload

## Status

Skeleton only — every module is commented-but-empty. See each file for
implementation notes.
