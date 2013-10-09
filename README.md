bitstampy
=========

Bitstamp API wrapper for Python

bitstampy provides Python wrappers for the 
[Bitstamp API](https://www.bitstamp.net/api/).

Usage
=====

```python
import bitstampy
```

bitstampy currently provides support for the un-authorised calls to the API:

**Ticker**

```python
> bitstampy.ticker()
{u'volume': 19233.85232961, u'last': 125.85, u'timestamp': 1381337697, u'bid': 125.75, u'high': 125.9, u'low': 122.3, u'ask': 125.84}
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
