import os
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

INITIAL_POOL = 50000.0
loans = []
COMMIT = os.getenv("RENDER_GIT_COMMIT", os.getenv("GIT_SHA", "local"))[:7]


def get_current_pool():
    disbursed = sum(loan["amount"] for loan in loans)
    return round(INITIAL_POOL - disbursed, 2)


@app.route("/")
def home():
    current_pool = get_current_pool()
    total_disbursed = round(sum(loan["amount"] for loan in loans), 2)
    avg_dti = (
        round(sum(loan["dti"] for loan in loans) / len(loans), 1)
        if loans
        else 0.0
    )
    return render_template(
        "index.html",
        loans=loans,
        current_pool=current_pool,
        total_disbursed=total_disbursed,
        avg_dti=avg_dti,
        commit=COMMIT,
    )


@app.route("/apply", methods=["POST"])
def apply_loan():
    borrower = request.form.get("borrower", "").strip()
    amount_str = request.form.get("amount", "").strip()
    income_str = request.form.get("income", "").strip()
    debt_str = request.form.get("debt", "").strip()

    if not borrower or not amount_str or not income_str or not debt_str:
        return "All form fields are required.", 400

    try:
        amount = float(amount_str)
        income = float(income_str)
        debt = float(debt_str)
    except ValueError:
        return "Values must be valid numbers.", 400

    if amount <= 0 or income <= 0 or debt < 0:
        return "Values must be strictly positive.", 400

    if amount > get_current_pool():
        return "Loan rejected: Requested amount exceeds available capital pool.", 400

    dti = round((debt / income) * 100, 2)
    if dti > 40.0:
        return f"Loan rejected: High risk. DTI ratio of {dti}% exceeds the 40% threshold.", 400

    loans.append({
        "id": len(loans) + 1,
        "borrower": borrower,
        "amount": amount,
        "income": income,
        "dti": dti,
    })
    return redirect("/")


@app.route("/api/loans")
def api_loans():
    return jsonify({
        "current_pool": get_current_pool(),
        "total_disbursed": sum(loan["amount"] for loan in loans),
        "loans": loans,
    })


@app.route("/health")
def health():
    return {"status": "ok", "commit": COMMIT}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
