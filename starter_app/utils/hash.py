import base64
import hashlib
import hmac
import time
import uuid


def gen_uuid():
    return str(uuid.uuid4())


def hmac_sha256(key: bytes, message: bytes) -> bytes:
    return hmac.new(key, message, hashlib.sha256).digest()


def generate_api_key(client_id, client_secret) -> str:
    timestamp = int(time.time())
    message = f'{client_id}.{client_secret}.{timestamp}'
    signature = hmac_sha256(client_secret.encode(), message.encode())
    # remove special characters and trailing `=`: https://gist.github.com/cameronmaske/f520903ade824e4c30ab
    return base64.urlsafe_b64encode(signature).rstrip(b'=').decode()
