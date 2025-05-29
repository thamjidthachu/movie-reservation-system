import requests

REGISTER_URL = "http://127.0.0.1:5000/auth/register"

users = [
    {"username": "thachu_one", "email": "thachuthamjid+1@gmail.com", "password": "thachu#01"},
    {"username": "thachu_two", "email": "thachuthamjid+2@gmail.com", "password": "thachu#01"},
    {"username": "thachu_three", "email": "thachuthamjid+3@gmail.com", "password": "thachu#01"},
    {"username": "thachu_four", "email": "thachuthamjid+4@gmail.com", "password": "thachu#01"},
    {"username": "thachu_five", "email": "thachuthamjid+5@gmail.com", "password": "thachu#01"},
]

sessions = []

for creds in users:
    session = requests.Session()
    response = session.post(REGISTER_URL, json=creds)
    if response.ok:
        print(f"[+] Registered as {creds['username']}")
        sessions.append(session)
    else:
        print(f"[!] Failed to register as {creds['username']}")
        print(response.status_code, response.text)
