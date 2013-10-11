# Standard dependencies
import hashlib, hmac, time
# 3rd party dependencies
import requests

# Constants
_API_URL = 'https://www.bitstamp.net/api/'
_API_TICKER = {
	'url': _API_URL + 'ticker/',
	'method': 'get'
}
_API_ORDER_BOOK = {
	'url': _API_URL + 'order_book/',
	'method': 'get'
}
_API_TRANSACTIONS = {
	'url': _API_URL + 'transactions/',
	'method': 'get'
}
_API_EUR_USD_CONVERSION_RATE = {
	'url': _API_URL + 'eur_usd/',
	'method': 'get'
}
_API_ACCOUNT_BALANCE = {
	'url': _API_URL + 'balance/',
	'method': 'post'
}
_API_USER_TRANSACTIONS = {
	'url': _API_URL + 'user_transactions/',
	'method': 'post'
}

# Class definitions
class APIError(Exception): pass

class _APICall:
	def __init__(self, api_endpoint, parameters = {}):
		self.url = api_endpoint['url']
		self.method = api_endpoint['method']
		self.parameters = parameters
	def authorise(self, client_id, api_key, api_secret):
		auth = _get_auth(client_id, api_key, api_secret)
		for key in auth.keys(): self.parameters[key] = auth[key]
		return self
	def call(self):
		r = None
		if self.method == 'get':
			r = requests.get(self.url, params = self.parameters)
		elif self.method == 'post':
			r = requests.post(self.url, data = self.parameters)
		jsn = r.json()
		if type(jsn) is dict and 'error' in jsn.keys():
			raise APIError(jsn['error'])
		return jsn

def _get_auth(client_id, api_key, api_secret):
	nonce = _get_nonce()
	message = nonce + client_id + api_key
	signature = hmac.new(api_secret, msg = message, digestmod = hashlib.sha256)
	signature = signature.hexdigest().upper()
	return {
		'key': api_key,
		'signature': signature,
		'nonce': nonce
	}

def _get_nonce(): return str(int(time.time()))

def account_balance(client_id, api_key, api_secret):
	call = _APICall(_API_ACCOUNT_BALANCE).authorise(client_id, api_key, api_secret)
	resp = call.call()
	for field in ['btc_reserved', 'fee', 'btc_available', 'usd_reserved',
		'btc_balance', 'usd_balance', 'usd_available']:
		resp[field] = float(resp[field])
	return resp

def eur_usd_conversion_rate():
	call = _APICall(_API_EUR_USD_CONVERSION_RATE)
	resp = call.call()
	for field in ['buy', 'sell']:
		resp[field] = float(resp[field])
	return resp

def order_book(group = True):
	params = {'group': '1' if group else '0'}
	call = _APICall(_API_ORDER_BOOK, params)
	resp = call.call()
	for field in ['bids', 'asks']:
		resp[field] = [[float(pr), float(amnt)] for (pr, amnt) in resp[field]]
	for field in ['timestamp']:
		resp[field] = int(resp[field])
	return resp

def ticker():
	call = _APICall(_API_TICKER)
	resp = call.call()
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
	call = _APICall(_API_TRANSACTIONS, params)
	resp = call.call()
	for tx in resp:
		for field in ['price', 'amount']:
			tx[field] = float(tx[field])
		for field in ['date', 'tid']:
			tx[field] = int(tx[field])
	return resp

def user_transactions(client_id, api_key, api_secret, 
	offset = 0, limit = 100, sort_descending = True):
	params = {
		'offset': str(offset), 
		'limit': str(limit), 
		'sort': 'desc' if sort_descending else 'asc'}
	call = _APICall(_API_USER_TRANSACTIONS, params).authorise(client_id, api_key, api_secret)
	resp = call.call()
	for tx in resp:
		for field in ['usd', 'btc', 'fee']:
			tx[field] = float(tx[field])
		for field in ['datetime', 'id', 'type', 'order_id']:
			tx[field] = int(tx[field])
	return resp
