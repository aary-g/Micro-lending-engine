import os
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

AVAILABLE_POOL = 50000.0


def get_commit_sha():
    sha = os.getenv("RENDER_GIT_COMMIT")
    if sha:
        return sha[:7]
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("utf-8")
            .strip()
        )
    except Exception:
        return "902ef5d"


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html", pool=AVAILABLE_POOL, decision=None, commit_sha=get_commit_sha()
    )


@app.route("/apply", methods=["POST"])
def apply():
    global AVAILABLE_POOL
    name = request.form.get("name", "Applicant")
    income = float(request.form.get("income", 0))
    debt = float(request.form.get("debt", 0))
    amount = float(request.form.get("amount", 0))

    if income <= 0:
        decision = {
            "status": "Rejected",
            "reason": "Monthly income must be greater than zero.",
            "dti": 0,
        }
        return render_template(
            "index.html",
            pool=AVAILABLE_POOL,
            decision=decision,
            commit_sha=get_commit_sha(),
        )

    dti = debt / income
    if dti > 0.40:
        decision = {
            "status": "Rejected",
            "reason": f"DTI ratio ({dti * 100:.1f}%) exceeds maximum underwriting tolerance (40.0%).",
            "dti": dti,
        }
    elif amount > AVAILABLE_POOL:
        decision = {
            "status": "Rejected",
            "reason": f"Requested amount (${amount:,.2f}) exceeds currently available liquidity pool.",
            "dti": dti,
        }
    else:
        AVAILABLE_POOL -= amount
        decision = {
            "status": "Approved",
            "name": name,
            "amount": amount,
            "dti": dti,
        }

    return render_template(
        "index.html",
        pool=AVAILABLE_POOL,
        decision=decision,
        commit_sha=get_commit_sha(),
    )


@app.route('/api/pool', methods=['GET'])
def api_pool():
    return {
        'available_pool': AVAILABLE_POOL,
        'currency': 'USD',
        'status': 'operational',
    }


@app.route("/health", methods=["GET"])
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
