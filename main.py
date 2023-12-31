import functions_framework
import os
from typing import Dict, Tuple

from alpacaInterfacer import alpaca_interfacer


@functions_framework.http
def button_press(request) -> Tuple[Dict[str, str], int]:
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return {"message": "Authorization header is missing"}, 401
    auth_token = auth_header.split(" ")[1]
    if auth_token != os.getenv("secret_key"):
        return {"message": "Invalid token"}, 401
    ai = alpaca_interfacer()
    action_response = ai.execute_random_action()
    if action_response is None:
        return {"message": "Not able to buy or sell at this time"}, 400
    else:
        return {"message": action_response}, 200
