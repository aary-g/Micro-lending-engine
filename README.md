# Micro-Lending Capital Pool & Risk Assessment Engine

Automated fintech microservice that manages a community lending capital pool and evaluates credit risk using Debt-to-Income (DTI) bounds.

## CI/CD Pipeline
- **CI**: Runs on every push and PR. Lints code via `flake8` and runs 5 unit/integration tests with `pytest`.
- **CD Gate**: Deploys to Render via webhook only if all tests on `main` pass (`needs: test`).

## Local Execution
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
flake8 --max-line-length=120 --exclude=venv .
pytest -v
python app.py