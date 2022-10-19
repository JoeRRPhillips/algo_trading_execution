import hashlib
import hmac
import json
import requests
import time
from typing import Dict, Tuple
from _config import API_KEY, SECRET_KEY


def post_request(method: str, req_id: int, params: Dict, debug: bool) -> Tuple[int, Dict]:
    url = "https://uat-api.3ona.co/v2/" if debug else "https://api.crypto.com/v2/"
    request = {
        "id": req_id,
        "method": method,
        "api_key": API_KEY,
        "params": params,
        "nonce": time_now()
    }
    response = requests.post(
        f"{url}{method}",
        headers={"Content-type": "application/json"},
        data=json.dumps(sign_private_request(request))
    )
    return response.status_code, json.loads(response.content)


def sign_private_request(req: Dict) -> Dict:
    # Params need to be alphabetically sorted by key
    param_str = ""
    if "params" in req:
        for key in sorted(req["params"]):
            param_str += key
            param_str += str(req["params"][key])

    # method + id + api_key + parameter string + nonce
    sig_payload = req["method"] + str(req["id"]) + req["api_key"] + param_str + str(req["nonce"])

    # hash req using api secret as the cryptographic key -> Digital Signature as hex string
    req["sig"] = hmac.new(
        bytes(str(SECRET_KEY), "UTF-8"),
        msg=bytes(sig_payload, "UTF-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()

    return req


def time_now():
    return int(time.time() * 1000)
