from bitstampy import api

print('EUR/USD conversion rate %s' % api.eur_usd_conversion_rate())
print('Order book %s' % api.order_book()[:3])
print('Ticker %s' % api.ticker())
print('Transactions %s' % api.eur_usd_conversion_rate(limit = 3))
