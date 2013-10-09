# Standard dependencies
import hashlib, hmac, time
# 3rd party dependencies
import requests

# Constants
API_URL = 'https://www.bitstamp.net/api/'
API_TICKER_URL = API_URL + 'ticker/'
API_ORDER_BOOK_URL = API_URL + 'order_book/'
API_TRANSACTIONS_URL = API_URL + 'transactions/'
API_EUR_USD_CONVERSION_RATE_URL = API_URL + 'eur_usd/'

# Auth info
CLIENT_ID = '643388'
API_KEY = 'APIKEY'
API_SECRET = 'APISECRET'

def _get_auth(client_id, api_key, api_secret):
	print('_get_auth ::: Getting authentication credentials')
	nonce = _get_nonce()
	print('_get_auth ::: Nonce %s' % nonce)
	print('_get_auth ::: Client ID %s' % client_id)
	print('_get_auth ::: API key %s' % api_key)
	message = nonce + client_id + api_key
	signature = hmac.new(api_secret, msg=message, digestmod=hashlib.sha256)
	signature = signature.hexdigest().upper()
	print('_get_auth ::: Signature %s' % signature)
	return {
		'key': api_key,
		'signature': signature,
		'nonce': nonce
	}

def _get_nonce(): return str(int(time.time()))

def eur_usd_conversion_rate():
	resp = requests.get(API_EUR_USD_CONVERSION_RATE_URL).json()
	for field in ['buy', 'sell']:
		resp[field] = float(resp[field])
	return resp

def order_book(group = True):
	params = {'group': '1' if group else '0'}
	resp = requests.get(API_ORDER_BOOK_URL, params = params).json()
	for field in ['bids', 'asks']:
		resp[field] = [[float(pr), float(amnt)] for (pr, amnt) in resp[field]]
	for field in ['timestamp']:
		resp[field] = int(resp[field])
	return resp

def ticker():
	resp = requests.get(API_TICKER_URL).json()
	for field in ['volume', 'last', 'bid', 'ask', 'high', 'low']:
		resp[field] = float(resp[field])
	for field in ['timestamp']:
		resp[field] = int(resp[field])
	return resp

def transactions(offset = 0, limit = 100, sort_descending = True):
	params = {
		'offset': str(offset),
		'limit': str(limit),
		'sort': 'desc' if sort_descending else 'asc'
	}
	resp = requests.get(API_TRANSACTIONS_URL, params = params).json()
	for tx in resp:
		for field in ['price', 'amount']:
			tx[field] = float(tx[field])
		for field in ['date', 'tid']:
			tx[field] = int(tx[field])
	return resp

print(eur_usd_conversion_rate())
