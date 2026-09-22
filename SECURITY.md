# Security Policy

SecureLearn Cyber Lab is designed for education and authorized security practice.

## Safe use

- Run labs only against systems you own or have explicit permission to test.
- Never store real credentials, tokens, private keys, or personal data in examples.
- Use isolated virtual machines or lab networks for security exercises.
- Sanitize screenshots, logs, packet captures, and challenge data before sharing them.
- Treat submitted URLs, email samples, and generated analysis results as potentially sensitive.

## Reporting

If you discover a security issue in the project itself, avoid posting secrets or sensitive reproduction data publicly. Report the affected component, impact, reproduction context, and suggested remediation through an appropriate private channel when available.

For useful reports, include:

1. The affected file, endpoint, or feature.
2. Minimal reproduction steps.
3. Expected versus observed behavior.
4. Security impact and realistic attack prerequisites.
5. A proposed fix or mitigation when practical.

Remove passwords, API keys, session tokens, personal information, and real customer data from logs before sharing them.

## Deployment checklist

Before exposing the application outside a local lab:

- Configure a strong `SECRET_KEY` through the environment and never rely on the development default.
- Keep `DEBUG` disabled in production.
- Restrict CORS to trusted frontend origins.
- Protect database files and analysis artifacts with appropriate filesystem permissions.
- Review dependency updates and run the automated tests before deployment.
- Do not treat the phishing classifier's prediction as proof that a URL or message is malicious.

## Disclosure

This project is primarily for academic and authorized defensive-security learning. Security findings should contain enough evidence to reproduce the issue without publishing credentials, private data, or unnecessarily weaponized payloads.