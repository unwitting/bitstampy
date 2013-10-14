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
	'timestamp': datetime,   # Datetime
	'volume': decimal,       # Last 24 hours volume
	'last': decimal,         # Last BTC price
	'high': decimal,         # Last 24 hours high
	'low': decimal,          # Last 24 hours low
	'bid': decimal,          # Highest buy order
	'ask': decimal           # Lowest ask order
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
	'timestamp': datetime,              # Datetime
	'bids': [                           # List of bids
		{
			'price': decimal,   ## Price for bid
			'amount': decimal   ## Amount bid
		}, ...
	],
	'asks': [                           # List of asks
		{
			'price': decimal,   ## Price for ask
			'amount': decimal   ## Amount asked
		}, ...
	]
}
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
[                                   # List of transactions, length 'limit'
	{
		'date': datetime,   ## Datetime
		'tid': string,      ## Transaction ID
		'price': decimal,   ## Transaction price
		'amount': decimal   ## Transaction amount
	}, ...
]
```

### EUR/USD Conversion Rate ###

```python
# Bitstamp's Dollar to Euro conversion rate
> bitstampy.eur_usd_conversion_rate()
{
	'sell': decimal,   # Conversion rate for selling
	'buy': decimal     # Conversion rate for buying
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
	'usd_balance': decimal,     # US Dollar balance
	'btc_balance': decimal,     # Bitcoin balance
	'usd_reserved': decimal,    # US Dollars reserved in open orders
	'btc_reserved': decimal,    # Bitcoins reserved in open orders
	'usd_available': decimal,   # US Dollars available
	'btc_available': decimal,   # Bitcoins available
	'fee': decimal              # Account trading fee (in %)
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
[                                       # List of transactions, length 'limit'
	{
		'datetime': datetime,   ## Datetime
		'id': string,           ## Transaction ID
		'type': string,         ## Transaction type - one of
		                        ### api.USER_TRANSACTIONS_TYPE_DEPOSIT,
		                        ### api.USER_TRANSACTIONS_TYPE_WITHDRAWAL,
		                        ### api.USER_TRANSACTIONS_TYPE_MARKET_TRADE
		'usd': decimal,         ## US Dollar amount
		'btc': decimal,         ## Bitcoin amount
		'fee': decimal,         ## Transaction fee (in %)
		'order_id': decimal     ## Transaction amount
	}, ...
]
```

### Open Orders ###

```python
# Your open orders
> bitstampy.open_orders(c, k, s)
[                                       # List of open orders
	{
		'datetime': datetime,   ## Datetime
		'id': string,           ## Order ID
		'type': string,         ## Order type - one of
		                        ### api.OPEN_ORDERS_TYPE_BUY,
		                        ### api.OPEN_ORDERS_TYPE_SELL
		'price': decimal,       ## Order price
		'amount': decimal       ## Order amount
	}, ...
]
```

### Cancel Order ###

```python
# Cancel an order
# Parameters
## id - ID of order to cancel
##    - string
> bitstampy.cancel_order(c, k, s)
True / False   # Returns boolean success
```

### Buy Limit Order ###

```python
# Place a buy order
## amount - Amount to buy
##        - float
## price  - Price to offer
##        - float
> bitstampy.buy_limit_order(c, k, s)
{
	'datetime': datetime,   # Datetime placed
	'id': string,           # Order ID
	'type': string,         # Order type - one of 
	                        ## api.BUY_LIMIT_ORDER_TYPE_BUY,
	                        ## api.BUY_LIMIT_ORDER_TYPE_SELL
	'price': decimal,       # Placed order price
	'amount': decimal       # Placed order amount
}
```

### Sell Limit Order ###

```python
# Place a sell order
## amount - Amount to sell
##        - float
## price  - Price to ask for
##        - float
> bitstampy.sell_limit_order(c, k, s)
{
	'datetime': datetime,   # Datetime placed
	'id': string,           # Order ID
	'type': string,         # Order type - one of 
	                        ## api.SELL_LIMIT_ORDER_TYPE_BUY,
	                        ## api.SELL_LIMIT_ORDER_TYPE_SELL
	'price': decimal,       # Placed order price
	'amount': decimal       # Placed order amount
}
```

### Check Bitstamp Code ###

```python
# Check the value of a bitstamp code
## code - Bitstamp code
##      - string
> bitstampy.check_bitstamp_code(c, k, s)
{
	'usd': decimal,   # US Dollar amount in the code
	'btc': decimal    # Bitcoin amount in the code
}
```

### Redeem Bitstamp Code ###

```python
# Redeem a bitstamp code
## code - Bitstamp code
##      - string
> bitstampy.redeem_bitstamp_code(c, k, s)
{
	'usd': decimal,   # US Dollar amount added to account by code
	'btc': decimal    # Bitcoin amount added to account by code
}
```

### Withdrawal Requests ###

```python
# Get list of withdrawal requests
> bitstampy.withdrawal_requests(c, k, s)
[                                       # List of withdrawal requests
	{
		'datetime': datetime,   ## Datetime
		'id': string,           ## Withdrawal ID
		'type': string,         ## Request type - one of
		                        ### api.WITHDRAWAL_REQUEST_TYPE_SEPA,
		                        ### api.WITHDRAWAL_REQUEST_TYPE_BITCOIN,
		                        ### api.WITHDRAWAL_REQUEST_TYPE_WIRE,
		                        ### api.WITHDRAWAL_REQUEST_TYPE_BITSTAMP_CODE_1,
		                        ### api.WITHDRAWAL_REQUEST_TYPE_BITSTAMP_CODE_2,
		                        ### api.WITHDRAWAL_REQUEST_TYPE_MTGOX
		'status': string,       ## Request status - one of
		                        ### api.WITHDRAWAL_REQUEST_STATUS_OPEN,
		                        ### api.WITHDRAWAL_REQUEST_STATUS_IN_PROCESS,
		                        ### api.WITHDRAWAL_REQUEST_STATUS_FINISHED,
		                        ### api.WITHDRAWAL_REQUEST_STATUS_CANCELLED,
		                        ### api.WITHDRAWAL_REQUEST_STATUS_FAILED
		'amount': decimal,      ## Request amount
		'data': string          ## Extra data (specific to type)
	}, ...
]
```
