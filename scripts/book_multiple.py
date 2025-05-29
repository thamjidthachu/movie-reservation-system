import requests

LOGIN_URL = "http://127.0.0.1:5000/auth/login"
CHECKOUT_URL = "http://127.0.0.1:5000/checkout"

users = [
    {"username": "thachu_one", "password": "thachu#01"},
    {"username": "thachu_two", "password": "thachu#01"},
    {"username": "thachu_three", "password": "thachu#01"},
    {"username": "thachu_four", "password": "thachu#01"},
    {"username": "thachu_five", "password": "thachu#01"},
]

tokens = []

for creds in users:
    session = requests.Session()
    response = session.post(LOGIN_URL, json=creds)
    if response.ok:
        tokens.append({'bearer': response.json().get('access_token')})

    else:
        print(f"[!] Failed to log in as {creds['username']}, cause: {response.__dict__}")

seats = [
    {"seat_ids": [1, 2]},
    {"seat_ids": [1, 2]},
    {"seat_ids": [3, 4]},
    {"seat_ids": [4, 5]},
    {"seat_ids": [1, 2]},
]

data = []

for token, seat in zip(tokens, seats):
    combined = token.copy()
    combined.update(seat)
    data.append(combined)

responses = []
count = 0
for item in data:
    count+=1
    bearer_token = item['bearer']
    seat_payload = {'seat_ids': item['seat_ids']}

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    session = requests.Session()
    response = session.post(CHECKOUT_URL, json=seat_payload, headers=headers)

    if response.ok:
        print(f"Try: {count} → Checkout successful with seats {item['seat_ids']}")
    else:
        print(f"Try: {count} → Failed checkout with seats {item['seat_ids']} because: {response.json().get('error')}")
