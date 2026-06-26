import requests

def get_gold_rate():
    """Get current gold rates in USD and INR"""
    try:
        # Get gold price in USD using metals.live
        url = "https://api.metals.live/v1/spot/gold"
        response = requests.get(url)
        data = response.json()

        # Gold price per troy ounce in USD
        gold_usd_per_ounce = float(data[0].get("price", 0))

        # Convert to grams (1 troy ounce = 31.1035 grams)
        gold_usd_per_gram = gold_usd_per_ounce / 31.1035

        # Get USD to INR rate
        inr_url = "https://open.er-api.com/v6/latest/USD"
        inr_response = requests.get(inr_url)
        inr_data = inr_response.json()
        usd_to_inr = inr_data["rates"]["INR"]

        # Calculate INR prices
        gold_inr_per_gram = gold_usd_per_gram * usd_to_inr

        # Calculate different quantities
        gold_inr_per_sovereign = gold_inr_per_gram * 8  # 1 sovereign = 8 grams
        gold_inr_22k_per_gram = gold_inr_per_gram * 0.916  # 22 carat = 91.6% pure
        gold_inr_24k_per_gram = gold_inr_per_gram  # 24 carat = 100% pure

        gold_usd_22k_per_gram = gold_usd_per_gram * 0.916
        gold_usd_24k_per_gram = gold_usd_per_gram

        return f"""
Live Gold Rates Today:

In Indian Rupees (INR):
- 24 Carat per gram: ₹{gold_inr_24k_per_gram:,.2f}
- 22 Carat per gram: ₹{gold_inr_22k_per_gram:,.2f}
- 24 Carat per sovereign (8g): ₹{gold_inr_per_sovereign:,.2f}

In US Dollars (USD):
- 24 Carat per gram: ${gold_usd_24k_per_gram:,.2f}
- 22 Carat per gram: ${gold_usd_22k_per_gram:,.2f}
- Per troy ounce: ${gold_usd_per_ounce:,.2f}

Exchange Rate Used: 1 USD = ₹{usd_to_inr:,.2f}
"""
    except Exception as e:
        return f"Could not fetch gold rate. Please try again."