import base64
import uuid

def get_random_id(prefix=""):
    encoded = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return prefix + encoded.rstrip(b"=").decode("ascii")
