# Micro-Lending Capital Pool & Risk Assessment Engine

Automated cloud-native fintech web service that manages a communal micro-financing capital pool ($50,000 baseline) and evaluates credit risk using Debt-to-Income (DTI) underwriting bounds.

- **Live Application:** https://micro-lending-engine.onrender.com

---

## Features

- **Dynamic Reserve Management:** Tracks an in-memory capital pool starting at $50,000.00; approved loans reduce available liquidity in real time.
- **Underwriting Risk Gate:** Rejects applications where Debt-to-Income exceeds 40.0% (`debt / income > 0.40`).
- **Real-Time Dynamic UI:** Interactive loan calculator with live payment projections (12 months @ 8.5% APR) and risk grading.
- **Version Traceability:** Displays deployed Git commit SHA in the footer via `RENDER_GIT_COMMIT`.

---

## API Endpoints

| Method | Route | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Web underwriting dashboard |
| `POST` | `/apply` | Evaluates borrower credit and updates pool |
| `GET` | `/api/pool` | Returns JSON status of liquidity pool |
| `GET` | `/health` | Health check endpoint returning status and commit SHA |

---

## CI/CD Pipeline

git push (main)
│
▼
[Job 1: test] ──> flake8 Lint ──> pytest -v
│
├─► (Pass) ──► [Job 2: deploy (needs: test)] ──► Render Webhook ──► Live Site
│
└─► (Fail) ──► Pipeline Blocked (Deployment Skipped)

- **Continuous Integration:** Every push and pull request runs `flake8` linting and `pytest` test suites.
- **Continuous Deployment:** On passing `main` branch builds, GitHub Actions calls the Render Deploy Hook. Render native auto-deploy is disabled to guarantee no untested code reaches production.

---

## Local Setup

```bash
# 1. Clone repo
git clone <your-repository-url>
cd Micro-lending-engine

# 2. Virtual environment setup
python -m venv venv
.\venv\Scripts\Activate.ps1    # macOS/Linux: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Lint and test
flake8 --max-line-length=120 --exclude=venv .
pytest -v

# 5. Run application
python app.py
