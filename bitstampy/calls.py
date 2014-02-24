import datetime
import hashlib
import hmac
import requests
import time
from decimal import Decimal

_API_URL = 'https://www.bitstamp.net/api/'


def dt(timestamp):
    """
    Convert a unix timestamp or ISO 8601 date string to a datetime object.
    """
    if not timestamp:
        return None
    try:
        timestamp = int(timestamp)
    except ValueError:
        try:
            timestamp = time.mktime(
                time.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f'))
        except ValueError:
            timestamp = time.mktime(
                time.strptime(timestamp, '%Y-%m-%d %H:%M:%S'))
    return datetime.datetime.fromtimestamp(timestamp)


class APIError(Exception):
    pass


class APICall(object):
    url = None
    method = 'get'

    def _process_response(self, response):
        """
        Process the response dictionary.

        If the dictionary is just being altered, then no return is necessary.
        Alternatively, a totally different response can be returned.
        """
        return

    def call(self, **params):
        # Form request
        r = None
        url = _API_URL + self.url
        if self.method == 'get':
            r = requests.get(url, params=params)
        elif self.method == 'post':
            r = requests.post(url, data=params)
        response = r.json()
        # API error?
        if isinstance(response, dict) and 'error' in response:
            raise APIError(response['error'])
        # Process fields
        new_response = self._process_response(response)
        if new_response is not None:
            response = new_response
        return response


class APIPrivateCall(APICall):
    method = 'post'

    def __init__(self, client_id, api_key, api_secret, *args, **kwargs):
        super(APIPrivateCall, self).__init__(*args, **kwargs)
        self.client_id = client_id
        self.api_key = api_key
        self.api_secret = api_secret

    def _get_nonce(self):
        return str(int(time.time() * 1e6))

    def call(self, **params):
        nonce = self._get_nonce()
        message = nonce + self.client_id + self.api_key
        signature = hmac.new(
            self.api_secret, msg=message, digestmod=hashlib.sha256)
        signature = signature.hexdigest().upper()
        params.update({
            'key': self.api_key, 'signature': signature, 'nonce': nonce
        })
        return super(APIPrivateCall, self).call(**params)


# Specific call classes
class APIAccountBalanceCall(APIPrivateCall):
    url = 'balance/'

    def _process_response(self, response):
        response['btc_reserved'] = Decimal(response['btc_reserved'])
        response['btc_available'] = Decimal(response['btc_available'])
        response['btc_balance'] = Decimal(response['btc_balance'])
        response['usd_reserved'] = Decimal(response['usd_reserved'])
        response['usd_available'] = Decimal(response['usd_available'])
        response['usd_balance'] = Decimal(response['usd_balance'])
        response['fee'] = Decimal(response['fee'])


class APIBitcoinDepositAddressCall(APIPrivateCall):
    url = 'bitcoin_deposit_address/'


class APIBitcoinWithdrawalCall(APIPrivateCall):
    url = 'bitcoin_withdrawal/'


class APIBuyLimitOrderCall(APIPrivateCall):
    url = 'buy/'

    def _process_response(self, response):
        response['datetime'] = dt(response['datetime'])
        response['price'] = Decimal(response['price'])
        response['amount'] = Decimal(response['amount'])


class APICancelOrderCall(APIPrivateCall):
    url = 'cancel_order/'


class APICheckBitstampCodeCall(APIPrivateCall):
    url = 'check_code/'

    def _process_response(self, response):
        response['usd'] = Decimal(response['usd'])
        response['btc'] = Decimal(response['btc'])


class APIEURUSDConversionRateCall(APICall):
    url = 'eur_usd/'

    def _process_response(self, response):
        response['buy'] = Decimal(response['buy'])
        response['sell'] = Decimal(response['sell'])


class APIOrderBookCall(APICall):
    url = 'order_book/'

    def _process_response(self, response):
        response['timestamp'] = dt(response['timestamp'])
        response['bids'] = [{
            'price': Decimal(price),
            'amount': Decimal(amount)
        } for (price, amount) in response['bids']]
        response['asks'] = [{
            'price': Decimal(price),
            'amount': Decimal(amount)
        } for (price, amount) in response['asks']]


class APIOpenOrdersCall(APIPrivateCall):
    url = 'open_orders/'

    def _process_response(self, response):
        for order in response:
            order['datetime'] = dt(order['datetime'])
            order['price'] = Decimal(order['price'])
            order['amount'] = Decimal(order['amount'])


class APIRedeemBitstampCodeCall(APIPrivateCall):
    url = 'redeem_code/'

    def _process_response(self, response):
        response['usd'] = Decimal(response['usd'])
        response['btc'] = Decimal(response['btc'])


class APIRippleDepositAddressCall(APIPrivateCall):
    url = 'ripple_address/'


class APIRippleWithdrawalCall(APIPrivateCall):
    url = 'ripple_withdrawal/'


class APISellLimitOrderCall(APIPrivateCall):
    url = 'sell/'

    def _process_response(self, response):
        response['datetime'] = dt(response['datetime'])
        response['price'] = Decimal(response['price'])
        response['amount'] = Decimal(response['amount'])


class APITickerCall(APICall):
    url = 'ticker/'

    def _process_response(self, response):
        response['last'] = Decimal(response['last'])
        response['high'] = Decimal(response['high'])
        response['low'] = Decimal(response['low'])
        response['volume'] = Decimal(response['volume'])
        response['timestamp'] = dt(response['timestamp'])
        response['bid'] = Decimal(response['bid'])
        response['ask'] = Decimal(response['ask'])


class APITransactionsCall(APICall):
    url = 'transactions/'

    def _process_response(self, response):
        for tx in response:
            tx['date'] = dt(tx['date'])
            tx['price'] = Decimal(tx['price'])
            tx['amount'] = Decimal(tx['amount'])


class APIUnconfirmedBitcoinDepositsCall(APIPrivateCall):
    url = 'unconfirmed_btc/'

    def _process_response(self, response):
        response['amount'] = Decimal(response['amount'])
        response['confirmations'] = int(response['confirmations'])


class APIUserTransactionsCall(APIPrivateCall):
    url = 'user_transactions/'

    def _process_response(self, response):
        for tx in response:
            tx['datetime'] = dt(tx['datetime'])
            tx['usd'] = Decimal(tx['usd'])
            tx['btc'] = Decimal(tx['btc'])
            tx['fee'] = Decimal(tx['fee'])


class APIWithdrawalRequestsCall(APIPrivateCall):
    url = 'withdrawal_requests/'

    def _process_response(self, response):
        for wr in response:
            wr['datetime'] = dt(wr['datetime'])
            wr['amount'] = Decimal(wr['amount'])
