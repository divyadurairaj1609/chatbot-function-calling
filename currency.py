import requests

def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another using live rates"""
    try:
        url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
        response = requests.get(url)
        data = response.json()

        if data.get("result") != "success":
            return f"Could not fetch exchange rates. Please try again."

        rates = data.get("rates", {})
        to_upper = to_currency.upper()

        if to_upper not in rates:
            return f"Currency '{to_currency}' not found. Try: USD, INR, EUR, GBP, JPY"

        rate = rates[to_upper]
        converted = float(amount) * rate

        return f"""
Currency Conversion:
- Amount: {amount} {from_currency.upper()}
- Converted: {converted:,.2f} {to_upper}
- Exchange Rate: 1 {from_currency.upper()} = {rate:,.4f} {to_upper}
"""
    except Exception as e:
        return f"Could not convert currency. Please try again."

def get_dollar_rate():
    """Get current USD to INR rate"""
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url)
        data = response.json()

        if data.get("result") != "success":
            return "Could not fetch dollar rate. Please try again."

        rates = data.get("rates", {})
        inr_rate = rates.get("INR", "N/A")
        eur_rate = rates.get("EUR", "N/A")
        gbp_rate = rates.get("GBP", "N/A")
        jpy_rate = rates.get("JPY", "N/A")
        aed_rate = rates.get("AED", "N/A")

        return f"""
Live Dollar Rates (1 USD =):
- INR (Indian Rupee): ₹{inr_rate:,.2f}
- EUR (Euro): €{eur_rate:,.4f}
- GBP (British Pound): £{gbp_rate:,.4f}
- JPY (Japanese Yen): ¥{jpy_rate:,.2f}
- AED (UAE Dirham): {aed_rate:,.4f}
"""
    except Exception as e:
        return "Could not fetch dollar rate. Please try again."