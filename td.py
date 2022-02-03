from config import config
from broker import Broker
from requests import post, get
from requests.models import Response


class TD(Broker):
    # TD Ameritrade Implementation. Paper trading is only available via thinkorswim.

    def __init__(self):
        self._place_order_url = 'https://api.tdameritrade.com/v1/accounts/{}/orders'.format(config['TD_ID'])
        self._refresh_token_url = 'https://api.tdameritrade.com/v1/oauth2/token'

    def print_response(self, response: Response):
        print('{name} Broker - HTTP_CODE={status_code}&MESSAGE={message}'.format(
            name=self.name, status_code=response.status_code, message=response.text
        ))

    def get_price(self):
        # Refer to TD API - https://developer.tdameritrade.com/quotes/apis/get/marketdata/%7Bsymbol%7D/quotes
        query_url = 'https://api.tdameritrade.com/v1/marketdata/{}/quotes'
        params = {'apikey': config['TD_CONSUMER_KEY'] + '@AMER.OAUTHAP'}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + config['TD_ACCESS_TOKEN']
        }

        # Attempt 1 to see response status code.
        response = get(query_url.format(config['SYMBOL']), params=params, headers=headers)

        # Refresh token if status code 401.
        # From TD - indicating the caller must pass a valid Authorization in the HTTP authorization request header.
        if response.status_code == 401:
            self.refresh_token()

            # Resend request using the new access token.
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + config['TD_ACCESS_TOKEN']
            }
            response = get(query_url.format(config['SYMBOL']), params=params, headers=headers)

        assert response.status_code == 200  # only status code 200 is able to pass this step

        return float(response.json()[config['SYMBOL']]['askPrice'])  # return ask price

    def refresh_token(self):
        # Refer to TD API - https://developer.tdameritrade.com/authentication/apis/post/token-0
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': config['TD_REFRESH_TOKEN'],
            'access_type': '',
            'code': config['TD_CODE'],
            'client_id': config['TD_CONSUMER_KEY'] + '@AMER.OAUTHAP',
            'redirect_uri': config['TD_CALLBACK_URL']
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = post(self._refresh_token_url, headers=headers, data=data)
        self.print_response(response)
        if response.status_code == 200:
            # New access token
            config['TD_ACCESS_TOKEN'] = response.json()['access_token']

    def place_order(self, quantity):
        # Refer to TD API - https://developer.tdameritrade.com/account-access/apis/post/accounts/%7BaccountId%7D/orders-0
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + config['TD_ACCESS_TOKEN']
        }

        # This request does not actually place the order.
        # Test request to ensure status code 200.
        response = post(self._place_order_url, headers=headers)

        # Refresh token if status code 401.
        if response.status_code == 401:
            self.refresh_token()

            # Update with new access token after refresh.
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + config['TD_ACCESS_TOKEN']
            }

        # This specifies the order that will be placed.
        data = {
            'orderType': 'MARKET',
            'session': 'NORMAL',
            'duration': 'DAY',
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'Buy',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': config['SYMBOL'],
                        'assetType': 'EQUITY'
                    }
                }
            ]
        }

        response = post(self._place_order_url, headers=headers, json=data)
        self.print_response(response)

    def do_dca(self):
        ask_price = self.get_price()
        quantity = self.calculate_qty(ask_price)
        self.place_order(quantity)
        message = "{broker} Broker - Placed order for {symbol}, {quantity}@{price}".format(
            broker=self.name, symbol=config['SYMBOL'], quantity=quantity, price=ask_price
        )
        self.log_order(message)
        print(message)
