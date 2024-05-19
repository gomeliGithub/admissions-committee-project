import time
from datetime import datetime
from typing import Dict

import jwt

from ..config.config import settings

JWT_SECRET: str = settings['JWT_SECRET']
JWT_ALGORITHM: str = settings['JWT_ALGORITHM']


def sign_jwt (jwt_payload: Dict[ str, str | int | datetime | None ]) -> str:
    payload = {
        **jwt_payload,
        "expires": time.time() + 600
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)

    return token


def decode_jwt (token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms = [JWT_ALGORITHM])

        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None # return { }