# SecureLearn Deployment Checklist

## Before deployment
- Set production secrets through environment variables or a secret manager.
- Keep DEBUG disabled in production.
- Restrict CORS to trusted origins instead of using a wildcard.
- Confirm model and uploaded-file paths are writable only where required.
- Run the Python test suite before publishing.

## Security verification
- Verify secret validation fails closed when required values are missing.
- Test malformed and non-finite model inputs.
- Confirm uploaded files are size/type constrained.
- Review logs to ensure passwords, tokens, and sensitive request data are not emitted.

## Operational checks
- Record the deployed commit SHA.
- Confirm health checks return the expected status.
- Keep a rollback commit or release reference available.
