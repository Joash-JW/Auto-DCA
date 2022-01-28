from config import config
from broker import Broker
from requests import post
from requests.models import Response


class TD(Broker):
    def __init__(self):
        self._place_order_url = 'https://api.tdameritrade.com/v1/accounts/{}/orders'.format(config['TD_ID'])
        self._refresh_token_url = 'https://api.tdameritrade.com/v1/oauth2/token'

    def print_response(self, response: Response):
        print('{name} Broker - HTTP_CODE={status_code}&MESSAGE={message}'.format(
            name=self.name, status_code=response.status_code, message=response.json()
        ))

    def refresh_token(self):
        # refer to TD API - https://developer.tdameritrade.com/authentication/apis/post/token-0
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

    def place_order(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + config['TD_ACCESS_TOKEN']
        }
        response = post(self._place_order_url, headers=headers)
        self.print_response(response)
        if response.status_code == 401:
            self.refresh_token()
        data = {
            'orderType': 'LIMIT',
            'session': 'NORMAL',
            'duration': 'DAY',
            'orderStrategyType': 'SINGLE',
            'price': 1.00,
            'orderLegCollection': [
                {
                    'instruction': 'Buy',
                    'quantity': 1,
                    'instrument': {
                        'symbol': 'AAPL',
                        'assetType': 'EQUITY'
                    }
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + config['TD_ACCESS_TOKEN']
        }
        response = post(self._place_order_url, headers=headers, json=data)
        self.print_response(response)
