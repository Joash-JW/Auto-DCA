config = {
  # Dollar-Cost Averaging config
  'SYMBOL': 'AAPL',        # Stock symbol, string type
  'ALLOCATION': 200,       # Amount of money to allocate for each DCA in USD, int type
  
  # config for TD
  'TD_ID': '',             # TD Ameritrade Account ID, string type
  'TD_ACCESS_TOKEN': '',   # Access Token, string type
  'TD_CONSUMER_KEY': '',   # Consumer key, string type
  'TD_CALLBACK_URL': 'http://localhost',
  'TD_REFRESH_URL': 'https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={callback_url}&client_id={consumer_key}%40AMER.OAUTHAP',
  'TD_REFRESH_TOKEN': '',  # Refresh token, string type
  'TD_CODE': '',           # TD Ameritrade Code, string type

  # config for MooMoo
  'MOOMOO_IP': '127.0.0.1',  # Default IP used
  'MOOMOO_PORT': 11111,      # Default Port used

  # config for IBKR
  'IBKR_URL': '127.0.0.1',  # Default IP used
  'IBKR_PORT': 4002,        # Default Port used, 4001 for IB Gateway live trading, 4002 for IB Gateway paper trading
  'IBKR_ID': 0,             # IBKR Master API client ID, int type

  # config for tiger
  'PRIVATE_KEY_PATH': '',   # Path to your private key, string type
  'TIGER_ID': 0,            # Tiger_ID, int type
  'TIGER_ACCOUNT': 0,       # Tiger Account (Live/Paper), int type
}
