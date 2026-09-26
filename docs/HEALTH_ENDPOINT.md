# Health Endpoint Contract

The Flask service exposes `GET /health` as a lightweight liveness check.

## Contract

- HTTP status: `200`
- Response JSON:

```json
{
  "status": "healthy",
  "app": "Phishing Detection Simulator"
}
```

## Operational use

Use this endpoint for local smoke checks and container/orchestrator liveness probes. It intentionally avoids model inference and database queries so a health check does not depend on the phishing model being loaded.
