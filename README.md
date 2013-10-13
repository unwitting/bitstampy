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
	'volume': float,   # Last 24 hours volume
	'last': float,     # Last BTC price
	'high': float,     # Last 24 hours high
	'low': float,      # Last 24 hours low
	'bid': float,      # Highest buy order
	'ask': float,      # Lowest ask order
	'timestamp': int
}
```

**Order Book**
```python
> bitstampy.order_book(group = True)
{u'timestamp': 1381337763, u'bids': [[125.78, 0.81093974], [125.77, 0.77920013], ...], u'asks': [[50000.0, 0.01], [63000.0, 1.0], ...]}
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
