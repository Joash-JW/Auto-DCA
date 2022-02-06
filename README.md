# Auto-DCA
A tutorial to automate your monthly Dollar-Cost Averaging.

## Description
This application is mainly a tutorial to automate your **MONTHLY** [Dollar-Cost Averaging](https://www.investopedia.com/terms/d/dollarcostaveraging.asp) tasks. This program is written in `Python`.
I have included the basic code to showcase how to place order with mainly these 4 brokers: **TD Ameritrade**, **Interactive Brokers**, **Tiger Brokers** and **MooMoo**.

> Dollar-cost averaging (DCA) is an investment strategy in which an investor divides up the total amount to be invested across periodic purchases of a target asset in an effort to reduce the impact of volatility on the overall purchase. The purchases occur regardless of the asset's price and at regular intervals. (*From Investopedia*)

:white_check_mark: Do: Recommended to first try this out with a paper trading account and modify this application to suit your needs.

## Getting Started
### Directory Structure
    Auto-DCA
    ├── logs/                    # Orders placed will be logged in this folder
    ├── .gitignore               # Specify private files to not push onto GitHub
    ├── app.py                   # Main entry point of the application
    ├── broker.py                # Abstract Class Broker
    ├── config.py                # Private configurations used to control the application 
    ├── config_template.py       # Template for config.py
    ├── ibkr.py                  # Subclass of Broker - Implementation for interacting with Interactive Brokers
    ├── moomoo.py                # Subclass of Broker - Implementation for interacting with MooMoo
    ├── td.py                    # Subclass of Broker - Implementation for interacting with TD Ameritrade
    ├── tiger.py                 # Subclass of Broker - Implementation for interacting with Tiger Brokers
    ├── requirements.txt         # Specify libraries that the application uses
    ├── rsa_private_key.pem      # Private Key for Tiger Brokers
    ├── rsa_public_key.pem       # Public Key for Tiger Brokers
    ├── LICENSE
    └── README.md

### Dependencies
This is written and tested with `Python3`.

### Installation
1. Set-up your respective broker, refer below [Broker Specifc Set-Up](https://github.com/Joash-JW/Auto-DCA#broker-specific-set-up).
2. Clone the repo
    ```commandline
    git clone https://github.com/Joash-JW/Auto-DCA.git
    ```
3. Install the necessary python libraries, but feel free to leave out libraries that you do not need.
    ```commandline
    pip install -r requirements.txt
    ```
   Optional libraries:
    ```text
    futu-api               # for MooMoo
    tigeropen              # for Tiger brokers
    ```

### Running the Program
First ensure that you have filled in your configurations in `config.py`, then run the following:
```commandline
python app.py
```

## Broker Specific Set-Up
### TD Ameritrade
:heavy_exclamation_mark: Note: TD Ameritrade does not allow paper trading via their API, paper trading is only allowed in thinkorswim.

Most of the steps are similar to https://www.reddit.com/r/algotrading/comments/c81vzq/td_ameritrade_api_access_2019_guide/ as I referenced it when developing this application.

1. Register an account here https://developer.tdameritrade.com/
2. Create an application in My Apps page ![td_add_app_edit](https://user-images.githubusercontent.com/32333304/152682940-0bfbe52c-5c6a-4eae-9dd8-0f3195c69482.png)
3. Fill in the app details, but use http://localhost for the Callback URL
4. Once completed, note down the Consumer Key of your app as it goes into `config['TD_CONSUMER_KEY']`
5. The next few steps are to obtain your Authorization Code as shown in https://developer.tdameritrade.com/content/simple-auth-local-apps
6. Replace the following part of the URL in { brackets } with your Consumer Key

   https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=http%3A%2F%2Flocalhost&client_id={CONSUMER_KEY}%40AMER.OAUTHAP
7. Hit Enter after placing in your Consumer Key in the URL shown in Step 6 and it will redirect you to this page ![td_redirect](https://user-images.githubusercontent.com/32333304/152683802-dc5df236-aa35-4500-8b96-04943de004c5.JPG)
8. Log In to your TD Ameritrade Account (**NOT** your TD Ameritrade Developer Account) and click Allow
9. After the above step, you will see a "This site can’t be reached" and this is **EXPECTED**
10. Copy the code parameter of the URL on this page, `https://localhost/?code=<COPY THIS>` ![TD code](https://preview.redd.it/uhuxz95f0s731.png?width=578&format=png&auto=webp&s=03d7d73869c0ab41021e93acf11e7dc192035ad8)
11. Do a URL Decode of the above step, and this will be your `config['TD_CODE`] 
12. Go to this site https://developer.tdameritrade.com/authentication/apis/post/token-0, fill in the Body Parameters and hit Send.
    ```text
    grant_type: authorization_code (type in exactly authorization_code)
    refresh_token: (leave this blank)
    access_type: offline (type in exactly offline)
    code: (fill in your decoded code from Step 11)
    client_id: {CONSUMER_KEY}@AMER.OAUTHAP (replace {CONSUMER_KEY} with your Consumer Key)
    redirect_uri: http://localhost
    ```
13. You will see "HTTP/1.1 200 OK" response if successful, and it will contain access_token and refresh_token. These goes into `config['TD_ACCESS_TOKEN']` and `config['TD_REFRESH_TOKEN']` respectively
14. Set-up complete!

### Interactive Brokers
:white_check_mark: Do: Recommended to first try this out with a paper trading account.

Refer to their official guide on creating a paper account https://www.interactivebrokers.com/en/software/ptgstl/topics/papertrader.htm

1. Download TWS API from here https://interactivebrokers.github.io/
2. You will also need to download TWS or IB Gateway which can be found here https://www.interactivebrokers.com/en/trading/ib-api.php
3. Configure the settings as follows (from Interactive Brokers official documentation) ![ibkr_settings](https://interactivebrokers.github.io/tws-api/enable_socket.png)
4. Note down the Port number, default is 7496 for live (TWS), 7497 for paper (TWS), 4001 for live (IB Gateway) and 4002 for paper (IB Gateway). This number also goes into `config['IBKR_PORT']`
5. Fill in your choice of Master API client ID. This number goes into `config[IBKR_ID]`
6. Navigate to your TWS API (for me, it is `C:\TWS API\source\pythonclient`) and run `python setup.py install`
7. Set-up complete! Make sure TWS or IB Gateway is running **before** running the application.

### Tiger Brokers
:white_check_mark: Do: Recommended to first try this out on your paper trading account.

1. Generate your private and public key. :heavy_exclamation_mark: Note: generated key needs to be in **1024 bits**
   
   Command to generate private key:
   ```commandline
   openssl genrsa -out rsa_private_key.pem 1024
   ```
   Command to generate public key:
   ```commandline
   openssl rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem
   ```
   To install OpenSSL, for MacOS users: `brew install openssl`, Linux users: `sudo apt-get install openssl`, and for Windows users, the least hassle way I found is to use git bash.
2. Go to https://quant.tigerfintech.com/?locale=en-us#developer
   ```text
   Verification code: (enter the code being sent to you after clicking 'Get verification code')
   IP whitelist: (leave this blank)
   Public key: (Paste your public key here, you can open the public key file using Notepad)
   Callback URL: (leave this blank)
   ```
   ![tiger_page2_en_edit](https://user-images.githubusercontent.com/32333304/152687783-8fa3195c-bd83-4795-b977-3d28e12eaf33.png)
3. Once completed you should see the page below. tiger_ID goes to `config['TIGER_ID']`, and Account ID/Paper account goes to `config['TIGER_ACCOUNT']`
   
   ![tiger_page_en_edit](https://user-images.githubusercontent.com/32333304/152688212-59880a27-db72-4a27-9545-4e2de8380432.png)
4. Set-up complete!

### MooMoo
:white_check_mark: Do: Recommended to first try this out on your paper trading account.

1. Download FutuOpenD from https://www.moomoo.com/download/ > OpenAPI > FutuOpenD
2. Install FutuOpenD, you can choose between the command line or the GUI version but for this tutorial I chose the GUI version
3. Launch FutuOpenD and you will see the page below. Ensure the IP and Port corresponds to `config['MOOMOO_IP']` and `config['MOOMOO_PORT']` respectively.

   ![moomoo](https://openapi.moomoo.com/futu-api-doc/assets/img/ui-config.1e824b8f.png)
4. Log In to your moomoo account.
5. Set-up complete! Make sure FutuOpenD is running **before** running the application.

### References
- https://developer.tdameritrade.com/content/getting-started
- https://www.reddit.com/r/algotrading/comments/c81vzq/td_ameritrade_api_access_2019_guide/
- https://medium.com/@fotiosdotcom/interactive-brokers-api-setup-ba87c73e7b6c
- https://interactivebrokers.github.io/tws-api/
- https://quant.itiger.com/openapi/zh/python/quickStart/prepare.html
- https://openapi.moomoo.com/futu-api-doc/en/quick/opend-base.html
