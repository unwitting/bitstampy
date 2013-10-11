from bitstampy import api
import getpass, sys, time

client_id = sys.argv[1]
api_key = sys.argv[2]
api_secret = sys.argv[3]

user_transactions = api.user_transactions(client_id, api_key, api_secret)
print('User transactions %s' % user_transactions)
time.sleep(1.1)

account_balance = api.account_balance(client_id, api_key, api_secret)
print('Account balance %s' % account_balance)
time.sleep(1.1)

rate = api.eur_usd_conversion_rate()
print('EUR/USD conversion rate %s' % rate)
time.sleep(1.1)

book = api.order_book()
book['bids'] = book['bids'][:5]
book['asks'] = book['asks'][:5]
print('Order book %s' % book)
time.sleep(1.1)

ticker = api.ticker()
print('Ticker %s' % ticker)
time.sleep(1.1)

transactions = api.transactions(limit = 5)
print('Transactions %s' % transactions)
time.sleep(1.1)
