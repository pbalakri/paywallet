import requests
import json


url = "https://sandboxapi.upayments.com/api/v1/charge"


def create_top_up_request(guardian, student, amount):
    payload = json.dumps({
        "products": [
            {
                "name": "Top Up",
                "description": "Top Up",
                "price": amount,
                "quantity": 1
            }
        ],
        "order": {
            "id": "202210101255255144669",
            "reference": "11111991",
            "description": "Purchase order received for Top Up",
            "currency": "KWD",
            "amount": amount
        },
        "language": "en",
        "reference": {
            "id": "202210101202210101"
        },
        "customer": {
            "uniqueId": student.bracelet_id,
            "name": guardian.user.first_name + " " + guardian.user.last_name,
            "email": guardian.user.email,
            "mobile": guardian.phone_number
        },
        "returnUrl": "https://upayments.com/en/",
        "cancelUrl": "https://error.com",
        "notificationUrl": "https://webhook.site/d7c6e1c8-b98b-4f77-8b51-b487540df336",
        "customerExtraData": "User define data"
    })
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': 'Bearer jtest123'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)


def create_buy_request(guardian, student, product, quantity):
    payload = json.dumps({
        "products": [
            {
                "name": product.name,
                "description": product.name,
                "price": product.price,
                "quantity": quantity
            }
        ],
        "order": {
            "id": "202210101255255144669",
            "reference": "11111991",
            "description": "Purchase order received for " + product.name,
            "currency": "KWD",
            "amount": product.price * quantity
        },
        "language": "en",
        "reference": {
            "id": "202210101202210101"
        },
        "customer": {
            "uniqueId": student.bracelet_id,
            "name": guardian.user.first_name + " " + guardian.user.last_name,
            "email": guardian.user.email,
            "mobile": guardian.phone_number
        },
        "returnUrl": "https://upayments.com/en/",
        "cancelUrl": "https://error.com",
        "notificationUrl": "https://webhook.site/d7c6e1c8-b98b-4f77-8b51-b487540df336",
        "customerExtraData": "User define data"
    })
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': 'Bearer jtest123'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)
