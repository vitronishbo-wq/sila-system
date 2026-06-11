import jwt
import time
SECRET = "Trumanmarcelo_1983_SILA_SECRET_KEY_2026"
now = int(time.time())
payload = {"sub": "citizen_demo", "type": "access", "iat": now, "exp": now + 3600, "realm_access": {"roles": ["CITIZEN"]}, "email": "citizen@example.com"}
token = jwt.encode(payload, SECRET, algorithm="HS256")
print('TOKEN:', token)
print('DECODED:', jwt.decode(token, SECRET, algorithms=['HS256']))
