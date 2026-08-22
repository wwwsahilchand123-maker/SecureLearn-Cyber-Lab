# AI-Powered Phishing Detection & Awareness Simulator

Educational B.Tech Cyber Security project.

## Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python + Flask
- ML: scikit-learn Random Forest
- Database: SQLite

## Setup
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python ml/train_model.py
python -m backend.app
```

Open http://127.0.0.1:5000/

## Safety
This is an educational simulator. It must not collect or transmit real passwords, OTPs, tokens, payment information, or other secrets.
