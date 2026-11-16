import requests
from core.config import *

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    res = requests.get(url, auth=(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET))
    return res.json()['access_token']

def stk_push(phone, amount):
    token = get_access_token()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "BusinessShortCode": MPESA_SHORTCODE,
        "Password": MPESA_PASSKEY,
        "Timestamp": "20260101010101",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": MPESA_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": MPESA_CALLBACK_URL,
        "AccountReference": "Musician",
        "TransactionDesc": "Premium"
    }

    return requests.post(url, json=payload, headers=headers).json()
