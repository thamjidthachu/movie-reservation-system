import requests

LOGIN_URL = "http://127.0.0.1:5000/auth/login"

users = [
    {"username": "thachu_one", "email": "thachuthamjid+1@gmail.com", "password": "thachu#01"},
    {"username": "thachu_two", "email": "thachuthamjid+2@gmail.com", "password": "thachu#01"},
    {"username": "thachu_three", "email": "thachuthamjid+3@gmail.com", "password": "thachu#01"},
    {"username": "thachu_four", "email": "thachuthamjid+4@gmail.com", "password": "thachu#01"},
    {"username": "thachu_five", "email": "thachuthamjid+5@gmail.com", "password": "thachu#01"},
]

sessions = {}

for creds in users:
    session = requests.Session()
    response = session.post(LOGIN_URL, json=creds)
    if response.ok:
        print(f"[+] Logged in as {creds['username']}, session: {session}")
        sessions[creds['username']]= response.json().get('access_token')
    else:
        print(f"[!] Failed to log in as {creds['username']}, cause: {response.__dict__}")

    print(sessions)
