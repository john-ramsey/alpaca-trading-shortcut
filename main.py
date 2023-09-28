import functions_framework
import os

from alpacaInterfacer import alpaca_interfacer


@functions_framework.http
def button_press(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return {"message": "Authorization header is missing"}, 401
    auth_token = auth_header.split(" ")[1]
    if auth_token != os.getenv("secret_key"):
        return {"message": "Invalid token"}, 401
    ai = alpaca_interfacer()
    action_response = ai.execute_random_action()
    if action_response is None:
        return {"message": "No actions available"}, 400
    else:
        return {"message": action_response}
