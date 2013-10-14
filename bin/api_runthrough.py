from bitstampy import api
import time

# Incrementally call all non-private API endpoints

# Ticker
print('Ticker %s' % api.ticker())
time.sleep(1.1)

# Order Book
book = api.order_book()
book['bids'] = book['bids'][:5]
book['asks'] = book['asks'][:5]
print('Order book %s' % book)
time.sleep(1.1)

# Transactions
print('Transactions %s' % api.transactions(limit=5))
time.sleep(1.1)

# EUR / USD
print('EUR / USD conversion %s' % api.eur_usd_conversion_rate())
time.sleep(1.1)
