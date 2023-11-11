import os
from unittest.mock import Mock, patch
from main import button_press


def test_button_press_no_auth_header():
    request = Mock()
    request.headers.get.return_value = None
    response, status_code = button_press(request)
    assert status_code == 401
    assert response == {"message": "Authorization header is missing"}


def test_button_press_invalid_token():
    request = Mock()
    request.headers.get.return_value = "Bearer invalid_token"
    os.environ["secret_key"] = "valid_token"
    response, status_code = button_press(request)
    assert status_code == 401
    assert response == {"message": "Invalid token"}


def test_button_press_valid_token():
    request = Mock()
    request.headers.get.return_value = "Bearer valid_token"
    os.environ["secret_key"] = "valid_token"
    # Mock the alpaca_interfacer instance and its methods
    with patch("main.alpaca_interfacer") as mock_alpaca_interfacer:
        mock_alpaca_interfacer.return_value.execute_random_action.return_value = (
            "buy_response"
        )
        response, status_code = button_press(request)
    assert status_code == 200
    assert response == {"message": "buy_response"}
