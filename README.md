bitstampy
=========

[Bitstamp API](https://www.bitstamp.net/api/) wrapper for Python

Usage
=====

```python
import bitstampy
```

bitstampy currently provides support for the un-authorised calls to the API:

**Ticker**

```python
# Ticker information
> bitstampy.ticker()
{
	'timestamp': int,
	'volume': float,   # Last 24 hours volume
	'last': float,     # Last BTC price
	'high': float,     # Last 24 hours high
	'low': float,      # Last 24 hours low
	'bid': float,      # Highest buy order
	'ask': float       # Lowest ask order
}
```

**Order Book**

```python
# Global order book (what's displayed [here](https://www.bitstamp.net/market/order_book/))
> bitstampy.order_book(group = True)
{
	'timestamp': int,
	'bids': [                 # List of bids
		{
			'price': float,   ## Price for bid
			'amount': float   ## Amount bid
		}, ...
	],
	'asks': [                 # List of asks
		{
			'price': float,   ## Price for ask
			'amount': float   ## Amount asked
		}, ...
	]
```

**Transactions**
```python
> bitstampy.transactions(offset = 0, limit = 100, sort_descending = True)
[{u'date': 1381337887, u'tid': 1523169, u'price': 125.78, u'amount': 0.06363003}, {u'date': 1381337838, u'tid': 1523168, u'price': 125.78, u'amount': 0.12543023}, ...]
```

**EUR/USD Conversion Rate**
```python
> bitstampy.eur_usd_conversion_rate()
{u'sell': 1.3508, u'buy': 1.3618}
```

Support is on the way for authorised requests, watch this space.
