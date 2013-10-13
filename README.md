# bitstampy #

[Bitstamp API](https://www.bitstamp.net/api/) wrapper for Python

# Installation

Is pretty bloody easy, as long as you've got **pip** installed.
If you haven't, take a look at the 
[pip documentation](http://www.pip-installer.org/en/latest/index.html) - 
it's worth getting familiar with!

```
pip install bitstampy
```

# Usage #

```python
import bitstampy
```

## Public Calls (no API authorisation needed) ##

### Ticker ###

```python
# Ticker information
> bitstampy.ticker()
{
	'timestamp': int,   # Datetime
	'volume': float,    # Last 24 hours volume
	'last': float,      # Last BTC price
	'high': float,      # Last 24 hours high
	'low': float,       # Last 24 hours low
	'bid': float,       # Highest buy order
	'ask': float        # Lowest ask order
}
```

### Order Book ###

```python
# Global order book (see live at https://www.bitstamp.net/market/order_book/)
# Parameters
## [group = True] - Group orders with same price?
##                - boolean
> bitstampy.order_book()
{
	'timestamp': int,         # Datetime
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

### Transactions ###

```python
# Global transactions
# Parameters
## [offset = 0]    - Skip this many transactions before starting return list
##                 - int
## [limit = 100]   - Return this many transactions after the offset
##                 - int
## [sort = 'desc'] - Results are sorted by datetime, but which way?!
##                 - string - 'desc' or 'asc'
> bitstampy.transactions()
[                         # List of transactions, length 'limit'
	{
		'date': int,      ## Datetime
		'tid': string,    ## Transaction ID
		'price': float,   ## Transaction price
		'amount': float   ## Transaction amount
	}, ...
]
```

### EUR/USD Conversion Rate ###

```python
# Bitstamp's Dollar to Euro conversion rate
> bitstampy.eur_usd_conversion_rate()
{
	'sell': float,   # Conversion rate for selling
	'buy': float     # Conversion rate for buying
}
```
