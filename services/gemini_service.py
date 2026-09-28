import os

def get_financial_advice(income, expense, categories):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "Gemini API key is not configured. Basic analysis: "
            f"Income = ₹{income:.2f}, Expenses = ₹{expense:.2f}, "
            f"Current savings = ₹{income-expense:.2f}. "
            "Review high-spending categories and set a realistic savings target."
        )

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""
You are a personal finance education assistant.
Give general budgeting guidance, not regulated investment or tax advice.
Income: ₹{income:.2f}
Expenses: ₹{expense:.2f}
Category spending: {categories}
Provide:
1. Spending summary
2. Possible overspending areas
3. Practical budget suggestions
4. Saving suggestions
Keep the answer concise and easy to understand.
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as exc:
        return f"AI service unavailable. Basic recommendation: review spending and save a fixed amount each month. ({exc})"
