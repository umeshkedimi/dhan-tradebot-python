import requests
import credentials
import datetime

BASE_URL = "https://api.dhan.co"
HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "access-token": credentials.ACCESS_TOKEN,
    "client-id": credentials.CLIENT_ID,
}


def get_quote(symbol: str):
    """
    Get the LTP for an instrument.
    symbol: NSE/BSE/BANKNIFTY options like 'BANKNIFTY24613APR45800PE'
    """
    url = f"{BASE_URL}/market/feed/quote"
    params = {
        "securityId": symbol,
        "exchangeSegment": "NFO",  # Change if not NFO
        "instrumentType": "OPTIDX"
    }
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        res.raise_for_status()
        return res.json()["lastTradedPrice"]
    except Exception as e:
        print(f"Error getting quote for {symbol}: {e}")
        return None


def place_order(symbol: str, qty: int, txn_type: str):
    """
    Place an order.
    txn_type: 'BUY' or 'SELL'
    """
    url = f"{BASE_URL}/orders"
    order_data = {
        "transactionType": txn_type,
        "securityId": symbol,
        "quantity": qty,
        "orderType": "MARKET",
        "productType": "INTRADAY",
        "price": 0.0,
        "exchangeSegment": "NFO",
        "validity": "DAY",
        "afterMarketOrderFlag": False,
        "amoTimeSlot": "SLOT1"
    }

    try:
        res = requests.post(url, headers=HEADERS, json=order_data)
        res.raise_for_status()
        return res.json().get("orderId")
    except Exception as e:
        print(f"Error placing order: {e}")
        return None


def get_positions():
    url = f"{BASE_URL}/positions"
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error fetching positions: {e}")
        return []


def cancel_all_open_orders():
    url = f"{BASE_URL}/orders"
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        orders = res.json()

        for order in orders:
            if order["status"] in ["OPEN", "TRIGGER_PENDING"]:
                cancel_url = f"{BASE_URL}/orders/{order['orderId']}/cancel"
                cancel_res = requests.post(cancel_url, headers=HEADERS)
                print(f"Cancelled order {order['orderId']}: {cancel_res.status_code}")
    except Exception as e:
        print(f"Error cancelling orders: {e}")


def square_off_all_positions():
    positions = get_positions()
    for pos in positions:
        if pos["netQty"] != 0:
            try:
                txn_type = "SELL" if pos["netQty"] > 0 else "BUY"
                place_order(pos["securityId"], abs(pos["netQty"]), txn_type)
                print(f"Squared off {pos['securityId']} with {txn_type}")
            except Exception as e:
                print(f"Error squaring off {pos['securityId']}: {e}")
