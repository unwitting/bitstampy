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
> import bitstampy
```

## Public calls (no API authorisation needed) ##

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
## [sort = 'desc'] - Results are sorted by datetime
##                 - string - api.TRANSACTIONS_SORT_DESCENDING or
##                 -        - api.TRANSACTIONS_SORT_ASCENDING
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

## Private calls (authorisation required) ##

Every call after this point requires you to have a working API key and secret
associated with your account on Bitstampy.
To get one set up, head to your Account > Security > API Access.
Choose a set of permissions you'd like the key to have - the meaning of each
of these should be pretty clear. After you've *created* a key, you need to 
*activate* it - this is done via a confirmation link in an email.

You'll get an API key and an associated secret. Note these down in your 
incredibly secure password manager / encrypted system / sneaky hidden notepad
of choice, because Bitstampy'll only let you view the API secret for 5 minutes
after you activate it ('cus security).

Each of the following API function calls takes three additional parameters - 
`client_id`, `api_key` and `api_secret`. The API key and secret are obvious, 
and `client_id` is your customer ID on Bitstampy (the numerical one). I'll 
include them in the function prototypes abbreviated as `c`, `k`, `s`.

Let's see the rest of the calls! These are the interesting ones because they
get you access to do actual *stuff* stuff with your account.

### Account Balance ###

```python
# Your account balance
> bitstampy.account_balance(c, k, s)
{
	'usd_balance': float,     # US Dollar balance
	'btc_balance': float,     # Bitcoin balance
	'usd_reserved': float,    # US Dollars reserved in open orders
	'btc_reserved': float,    # Bitcoins reserved in open orders
	'usd_available': float,   # US Dollars available
	'btc_available': float,   # Bitcoins available
	'fee': float              # Account trading fee (in %)
}
```

### User Transactions ###

```python
# Your transactions
# Parameters
## [offset = 0]    - Skip this many transactions before starting return list
##                 - int
## [limit = 100]   - Return this many transactions after the offset
##                 - int
## [sort = 'desc'] - Results are sorted by datetime
##                 - string - api.USER_TRANSACTIONS_SORT_DESCENDING or
##                 -        - api.USER_TRANSACTIONS_SORT_ASCENDING
> bitstampy.user_transactions(c, k, s)
[                           # List of transactions, length 'limit'
	{
		'datetime': int,    ## Datetime
		'id': string,       ## Transaction ID
		'type': string,     ## Transaction type - one of
		                    ### api.USER_TRANSACTIONS_TYPE_DEPOSIT,
		                    ### api.USER_TRANSACTIONS_TYPE_WITHDRAWAL,
		                    ### api.USER_TRANSACTIONS_TYPE_MARKET_TRADE
		'usd': float,       ## US Dollar amount
		'btc': float,       ## Bitcoin amount
		'fee': float,       ## Transaction fee (in %)
		'order_id': float   ## Transaction amount
	}, ...
]
```

### Open Orders ###

```python
# Your open orders
> bitstampy.open_orders(c, k, s)
[                          # List of open orders
	{
		'datetime': int,   ## Datetime
		'id': string,      ## Order ID
		'type': string,    ## Order type - one of
		                   ### api.OPEN_ORDERS_TYPE_BUY,
		                   ### api.OPEN_ORDERS_TYPE_SELL
		'price': float,    ## Order price
		'amount': float    ## Order amount
	}, ...
]
```