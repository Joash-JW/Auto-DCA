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
1. Set-up your respective broker, refer below
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
### Interactive Brokers
### Tiger Brokers
### MooMoo
 