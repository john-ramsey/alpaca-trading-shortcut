# Alpaca Trading Cloud Function

This project is a Google Cloud Function that interacts with an [Alpaca](https://alpaca.markets/) trading profile to buy or sell random stocks. It is designed to be used with the Apple Shortcuts app.


## LICENSE

Disclaimer: This code is shared for academic purposes under the MIT education license. **Nothing herein is financial advice, and NOT a recommendation to trade real money. Please use common sense and always first consult a professional before trading or investing.**


**Note that Alpaca has the ability to trade with ["paper" accounts](https://docs.alpaca.markets/docs/paper-trading) (i.e. fake money)**. The developer strongly advises against using this code as a trading strategy with actual funds.

This code has only been tested on Python 3.11 - no guarantees are made regarding its functionality.

## Overview

The main functionality of this project is encapsulated in the `alpaca_interfacer` class, which is defined in `alpacaInterfacer/__init__.py`. This class provides methods to buy or sell random stocks, and to execute a random action (either buying or selling).

The `alpaca_interfacer` class uses several helper classes to interact with the Alpaca API:

- `alpaca_base` in `alpacaInterfacer/alpacaBase.py`
- `account_handler` in `alpacaInterfacer/accountHandler.py`
- `asset_handler` in `alpacaInterfacer/assetHandler.py`
- `order_handler` in `alpacaInterfacer/orderHandler.py`
- `position_handler` in `alpacaInterfacer/positionHandler.py`

The project also includes a logger that uses Google Cloud's logging service, defined in `alpacaLogger/gcpLogger.py`.

The main entry point of the cloud function is defined in `main.py`.

## Setup

1. Clone this repository.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Set up your Alpaca API keys and other configuration variables in a `.env` file. You can use the provided `sample.env` as a template.
4. Deploy the cloud function to Google Cloud using the provided script in `scripts/deploy.sh`. Note that you will need to have [GCP CLI](https://cloud.google.com/sdk/docs/install) installed with the proper APIs exposed in your project.

## Usage

Once the cloud function is deployed, you can trigger it by making a HTTP request to the function's URL. If you're using the Apple Shortcuts app (the original intention for the repo), you can set up a shortcut to make this request. Note that the application uses bearer authentication.

The function will randomly choose to either buy or sell a stock from your Alpaca profile. The decision is logged to Google Cloud's logging service.

## Environmental Variables
The `sample.env` file contains a template for the environmental variables needed for the project. Rename this file to `.env` and replace the placeholders with your actual values. Here's what each variable is used for:

- `alpaca_key`: Your Alpaca API key. This is used to authenticate with the Alpaca API.
- `alpaca_secret`: Your Alpaca secret key. This is used to authenticate with the Alpaca API.
- `secret_key`: A secret key for your application. This is used for secure operations within your application.
- `max_percent_to_spend`: The maximum percentage of your buying power that you're willing to spend on a single stock purchase. This should be a decimal number between 0 and 1 (e.g., 0.1 for 10%).
- `truncated_asset_name_length`: The number of words to use from the asset name when logging or displaying asset names. For example, if this is set to 3, "Standard BioTools Inc. Common Stock" would be truncated to "Standard BioTools Inc.".

## Testing/Notebooks

Unit tests for the `alpaca_interfacer` class are provided in `tests/test_alpaceInterfacer.py`. You can run these tests using pytest.

The `notebooks` directory contains Jupyter notebooks that you can use to interactively test and explore the functionality of the `alpaca_interfacer` class.
