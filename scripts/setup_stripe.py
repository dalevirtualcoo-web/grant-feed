import urllib.request
import urllib.parse
import json
import os

def load_env():
    env_path = "/data/automation-arbitrage/.env"
    if not os.path.exists(env_path):
        print(f"Env file not found at {env_path}")
        return {}
    env = {}
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

def make_stripe_request(endpoint, params, secret_key):
    url = f"https://api.stripe.com/v1/{endpoint}"
    data = urllib.parse.urlencode(params).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res = response.read()
        return json.loads(res.decode("utf-8"))
    except Exception as e:
        print(f"Stripe API Error for /{endpoint}: {e}")
        return None

def setup_stripe():
    env = load_env()
    secret_key = env.get("STRIPE_SECRET_KEY") or os.environ.get("STRIPE_SECRET_KEY")
    
    if not secret_key:
        print("Error: STRIPE_SECRET_KEY not found in .env or environment.")
        return
        
    print("Initiating Stripe programmatic onboarding...")
    
    # 1. Create a Product
    print("Creating Product 'Premium Grant Intelligence Feed'...")
    product_params = {
        "name": "Premium Grant Intelligence Feed",
        "description": "Unlock unlimited real-time non-profit grant opportunities and digests."
    }
    product = make_stripe_request("products", product_params, secret_key)
    if not product:
        return
    product_id = product.get("id")
    print(f"Product created successfully. ID: {product_id}")
    
    # 2. Create a Price for the Product ($29/month)
    print("Creating Price '$29.00/month'...")
    price_params = {
        "product": product_id,
        "unit_amount": 2900,
        "currency": "usd",
        "recurring[interval]": "month"
    }
    price = make_stripe_request("prices", price_params, secret_key)
    if not price:
        return
    price_id = price.get("id")
    print(f"Price created successfully. ID: {price_id}")
    
    # 3. Create a Payment Link for the Price
    print("Generating hosted Payment Link...")
    link_params = {
        "line_items[0][price]": price_id,
        "line_items[0][quantity]": 1
    }
    payment_link = make_stripe_request("payment_links", link_params, secret_key)
    if not payment_link:
        return
    payment_url = payment_link.get("url")
    print(f"Payment Link generated successfully! URL: {payment_url}")
    
    # 4. Save details to stripe_config.json
    config_path = "/data/automation-arbitrage/data/stripe_config.json"
    config_data = {
        "product_id": product_id,
        "price_id": price_id,
        "payment_url": payment_url,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if 'datetime' in globals() else "2026-06-28"
    }
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)
        
    print(f"Stripe configuration saved to {config_path}")
    return payment_url

if __name__ == "__main__":
    setup_stripe()
