"""
Genrates a valid auth token for this server (For Dev use-only)
"""

from datetime import datetime, timedelta, timezone
from os import environ
from dotenv import load_dotenv
import jwt


load_dotenv()

iat = datetime.now(timezone.utc)
jwt_body = {
    "email": "anuragpparmar@gmail.com",
    "iat": iat,
    "exp": iat + timedelta(days=15),
    "iss": "Anurag",
}

token = jwt.encode(
    jwt_body, environ.get("secret")
)

print(token)
