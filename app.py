```python
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- Simple Tax Calculation Function ---
def calculate_tax(income):
    """
    Example Indian Income Tax Slabs:
    - Up to 2.5L: 0%
    - 2.5L – 5L: 5%
    - 5L – 10L: 20%
    - Above 10L: 30%
    """
    tax = 0
    if income <= 250000:
        tax = 0
    elif income <= 500000:
        tax = (income - 250000) * 0.05
    elif income <= 1000000:
        tax = (250000 * 0.05) + (income - 500000) * 0.20
    else:
        tax = (250000 * 0.05) + (500000 * 0.20) + (income - 1000000) * 0.30
    return tax

# --- Azure Bot Framework Endpoint ---
@app.route("/api/messages", methods=["POST"])
def messages():
    data = request.json
    user_text = data.get("text", "").lower()

    # Very simple intent handling
    response = "I can calculate your tax. Please enter your income."
    
    if "income" in user_text:
        try:
            income_val = int(user_text.replace("income", "").strip())
            tax = calculate_tax(income_val)
            response = f"✅ For an income of ₹{income_val}, your estimated tax is ₹{tax:.2f}"
        except:
            response = "❌ Please enter a valid income like: income 600000"

    return jsonify({"type": "message", "text": response})

@app.route("/", methods=["GET"])
def index():
    return "Tax Bot is running! " + str(datetime.now())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```
