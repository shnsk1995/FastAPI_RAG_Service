"""AWS Lambda entry point.

Wraps the FastAPI ASGI app with Mangum so API Gateway (HTTP API or REST API)
events are translated into ASGI scope. One Lambda function per service is
recommended in production:

    - chat-service-lambda     -> routes /api/v1/chat/*
    - ingestion-api-lambda    -> routes /api/v1/ingestion/upload-url, /webhook
    - ingestion-worker-lambda -> triggered by S3 ObjectCreated, not via API GW

For now this single handler serves all routes; split by setting `LAMBDA_ROLE`
env var and mounting only the matching router in app.main.create_app().
"""

# from mangum import Mangum
# from app.main import app
#
# handler = Mangum(app, lifespan="off")  # API Gateway -> FastAPI
#
# Notes:
# - lifespan="off" because Lambda has no long-lived startup; do init at import.
# - For S3-event-triggered ingestion worker, define a separate handler that
#   does NOT use Mangum:
#
#       def s3_event_handler(event, context):
#           # parse S3 records -> dispatch webhook -> ingestion_service.process()
#           ...
