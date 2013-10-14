import hashlib
import hmac
import requests
import time

_API_URL = 'https://www.bitstamp.net/api/'


class APIError(Exception):
    pass


class APICall(object):
    url = None
    method = 'get'

    def __init__(self):
        self.parameters = {}
        self.response = None

    def _process_response(self):
        pass

    def call(self, params={}):
        # Load parameters
        self.parameters.update(params)
        # Form request
        r = None
        url = _API_URL + self.url
        if self.method == 'get':
            r = requests.get(url, params=self.parameters)
        elif self.method == 'post':
            r = requests.post(url, data=self.parameters)
        self.response = r.json()
        # API error?
        if isinstance(self.response, dict) and 'error' in self.response:
            raise APIError(self.response['error'])
        # Process fields
        self._process_response()
        return self.response


class APIPrivateCall(APICall):
    method = 'post'

    def _get_nonce(self):
        return str(int(time.time()))

    def auth(self, client_id, api_key, api_secret):
        nonce = self._get_nonce()
        message = nonce + client_id + api_key
        signature = hmac.new(api_secret, msg=message, digestmod=hashlib.sha256)
        signature = signature.hexdigest().upper()
        self.parameters['key'] = api_key
        self.parameters['signature'] = signature
        self.parameters['nonce'] = nonce
        return self


# Specific call classes
class APIAccountBalanceCall(APIPrivateCall):
    url = 'balance/'

    def _process_response(self):
        self.response['btc_reserved'] = float(self.response['btc_reserved'])
        self.response['btc_available'] = float(self.response['btc_available'])
        self.response['btc_balance'] = float(self.response['btc_balance'])
        self.response['usd_reserved'] = float(self.response['usd_reserved'])
        self.response['usd_available'] = float(self.response['usd_available'])
        self.response['usd_balance'] = float(self.response['usd_balance'])
        self.response['fee'] = float(self.response['fee'])


class APIBitcoinDepositAddressCall(APIPrivateCall):
    url = 'bitcoin_deposit_address/'


class APIBuyLimitOrderCall(APIPrivateCall):
    url = 'buy/'

    def _process_response(self):
        self.response['datetime'] = int(self.response['datetime'])
        self.response['price'] = float(self.response['price'])
        self.response['amount'] = float(self.response['amount'])


class APICancelOrderCall(APIPrivateCall):
    url = 'cancel_order/'

    def _process_response(self):
        self.response = (self.response == 'true')


class APICheckBitstampCodeCall(APIPrivateCall):
    url = 'check_code/'

    def _process_response(self):
        self.response['usd'] = float(self.response['usd'])
        self.response['btc'] = float(self.response['btc'])


class APIEURUSDConversionRateCall(APICall):
    url = 'eur_usd/'

    def _process_response(self):
        self.response['buy'] = float(self.response['buy'])
        self.response['sell'] = float(self.response['sell'])


class APIOrderBookCall(APICall):
    url = 'order_book/'

    def _process_response(self):
        self.response['timestamp'] = int(self.response['timestamp'])
        self.response['bids'] = [{
            'price': float(price),
            'amount': float(amount)
        } for (price, amount) in self.response['bids']]
        self.response['asks'] = [{
            'price': float(price),
            'amount': float(amount)
        } for (price, amount) in self.response['asks']]


class APIOpenOrdersCall(APIPrivateCall):
    url = 'open_orders/'

    def _process_response(self):
        for order in self.response:
            order['datetime'] = int(order['datetime'])
            order['price'] = float(order['price'])
            order['amount'] = float(order['amount'])


class APIRedeemBitstampCodeCall(APIPrivateCall):
    url = 'redeem_code/'

    def _process_response(self):
        self.response['usd'] = float(self.response['usd'])
        self.response['btc'] = float(self.response['btc'])


class APIRippleDepositAddressCall(APIPrivateCall):
    url = 'ripple_address/'


class APIRippleWithdrawalCall(APIPrivateCall):
    url = 'ripple_withdrawal/'

    def _process_response(self):
        self.response = (self.response == 'true')


class APISellLimitOrderCall(APIPrivateCall):
    url = 'sell/'

    def _process_response(self):
        self.response['datetime'] = int(self.response['datetime'])
        self.response['price'] = float(self.response['price'])
        self.response['amount'] = float(self.response['amount'])


class APITickerCall(APICall):
    url = 'ticker/'

    def _process_response(self):
        self.response['last'] = float(self.response['last'])
        self.response['high'] = float(self.response['high'])
        self.response['low'] = float(self.response['low'])
        self.response['volume'] = float(self.response['volume'])
        self.response['timestamp'] = int(self.response['timestamp'])
        self.response['bid'] = float(self.response['bid'])
        self.response['ask'] = float(self.response['ask'])


class APITransactionsCall(APICall):
    url = 'transactions/'

    def _process_response(self):
        for tx in self.response:
            tx['date'] = int(tx['date'])
            tx['price'] = float(tx['price'])
            tx['amount'] = float(tx['amount'])


class APIUnconfirmedBitcoinDepositsCall(APIPrivateCall):
    url = 'unconfirmed_btc/'

    def _process_response(self):
        self.response['amount'] = float(self.response['amount'])
        self.response['confirmations'] = int(self.response['confirmations'])


class APIUserTransactionsCall(APIPrivateCall):
    url = 'user_transactions/'

    def _process_response(self):
        for tx in self.response:
            tx['datetime'] = int(tx['datetime'])
            tx['usd'] = float(tx['usd'])
            tx['btc'] = float(tx['btc'])
            tx['fee'] = float(tx['fee'])


class APIWithdrawalCall(APIPrivateCall):
    url = 'bitcoin_withdrawal/'

    def _process_response(self):
        self.response = (self.response == 'true')


class APIWithdrawalRequestsCall(APIPrivateCall):
    url = 'withdrawal_requests/'

    def _process_response(self):
        for wr in self.response:
            wr['datetime'] = int(wr['datetime'])
            wr['amount'] = float(wr['amount'])
