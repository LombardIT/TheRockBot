import arrow
import requests
import sqlite3
from PyRock import PyRock

HEADERS = {
    'User-Agent': '@TheRockBot Telegram Bot',
    'content-type': 'application/json'
    }

HOME = """
Select a command from the keyboard!
"""

HELP = """
You can add your API Keys to this bot, if you want! Just log into your The Rock account and generate an Api Key and an Api Secret. They don't need special permissions.
Press /delete_keys and TheRockBot will delete your API Keys.
For any issue, contact @mikexine here on Telegram."""


def Home():
    return HOME


def Help():
    return HELP


def Last():
    last = PyRock().Ticker('btceur')
    return "Last price on BTC/EUR market: %s Eur" % (last['last'])


def Ticker(fund_id):
    pretty = ''
    ticker = PyRock().Ticker(fund_id)
    high = ticker['high']
    low = ticker['low']
    ask = ticker['ask']
    bid = ticker['bid']
    last = ticker['last']
    fund_id = ticker['fund_id']
    volume = ticker['volume']
    pretty += ('\
Fund: %s:\n \
- Last: %s\n \
- High: %s, Low: %s\n \
- Ask: %s, Bid: %s\n \
- Volume: %s\n') % (fund_id, last, high, low,
                    ask, bid, (str(volume) + ' ' + fund_id[3:]))
    return pretty


def bitcoinData():
    url = 'http://btc.blockr.io/api/v1/coin/info'
    headers = {
            'User-Agent': '@TheRockBot Telegram Bot',
            'content-type': 'application/json'
            }
    r = requests.get(url, headers=headers)
    data = r.json()
    lastBlock = data['data']['last_block']
    blockNumber = lastBlock['nb']
    timeMined = (arrow.get(lastBlock['time_utc'])).format('HH:mm, DD-MM-YYYY')
    fees = '%s BTC' % lastBlock['fee']
    transactions = lastBlock['nb_txs']
    currentDifficulty = '%13.f' % float(lastBlock['difficulty'])
    textLastBlock = '* Last block data *\n \
- Block number: %s\n \
- Mined (UTC): %s\n \
- Amount of fees: %s\n \
- Number of transactions %s\n \
- Current difficulty: %s\n\n\
' % (blockNumber, timeMined, fees, transactions, currentDifficulty)
    nextDifficulty = data['data']['next_difficulty']
    retargetBlock = nextDifficulty['retarget_block']
    retargetIn = nextDifficulty['retarget_in']
    percentageChange = nextDifficulty['perc']
    forecastDifficulty = nextDifficulty['difficulty']
    textNextDifficulty = '* Next difficulty *\n \
- Retarget block: %s\n \
- Retarget in %s blocks.\n \
- Percentage change in difficulty: %2.2f %%\n \
- Next expected difficulty: %13.f\n \
' % (retargetBlock, retargetIn, percentageChange, forecastDifficulty)
    return textLastBlock + textNextDifficulty


def MyBalances(key, secret):
    pretty = ''
    rock = PyRock(key, secret)
    data = rock.AllBalances()
    try:
        balances = data['balances']
        for b in balances:
            if b['balance'] != 0.0:
                pretty += "%s -> Total: %.8f, Trading Balance: %.8f\n" % \
                         (b['currency'], b['balance'], b['trading_balance'])
        if pretty is '':
            pretty = 'No balance on The Rock!'
        return ('/home', pretty)
    except:
        pretty = ('Error occured. Check your API Keys! ' +
                  'type /register to update them.')
        return ('/register', pretty)


def MyTransactions(key, secret):
    pretty = ''
    rock = PyRock(key, secret)
    data = rock.Transactions()
    try:
        transactions = data['transactions']
        for transaction in transactions:
            amount = transaction['price']
            currency = transaction['currency']
            transactionType = transaction['type'].replace('_', ' ')
            date = arrow.get(transaction['date']).format('HH:mm, DD-MM-YYYY')
            pretty += '- %r %s, type: %s, date: %s\n' % \
                      (amount, currency, transactionType, date)
        if pretty is '':
            pretty = 'No transactions on The Rock!'
        return ('/home', pretty)
    except:
        pretty = ('Error occured. Check your API Keys! ' +
                  'type /register to update them.')
        return ('/register', pretty)


def MyTrades(key, secret, fund_id):
    pretty = ''
    rock = PyRock(key, secret)
    data = rock.UserTrades(fund_id)
    try:
        trades = data['trades']
        for trade in trades:
            amount = trade['amount']
            price = trade['price']
            side = trade['side']
            order_id = trade['order_id']
            date = arrow.get(trade['date']).format('HH:mm, DD-MM-YYYY')
            pretty += '- %s %s %s %s at price = %s %s. Id: %s.\n' % \
                      (date, side, amount, fund_id[:3],
                       price, fund_id[3:], order_id)
        if pretty is '':
            pretty = 'No trades on The Rock with this fund!'
        return ('/trades', pretty)
    except:
        pretty = ('Error occured. Check your API Keys! ' +
                  'type /register to update them.')
        return ('/register', pretty)


def MyDiscount(key, secret, fund_id):
    pretty = ''
    rock = PyRock(key, secret)
    data = rock.DiscountLevel(fund_id)
    try:
        pretty = 'Discount on %s: %s %%' % (fund_id, data['discount'])
        return ('/discounts', pretty)
    except:
        pretty = ('Error occured. Check your API Keys! ' +
                  'type /register to update them.')
        return ('/register', pretty)


def MyOrders(key, secret, fund_id):
    pretty = ''
    rock = PyRock(key, secret)
    data = rock.ListAllOrders(fund_id)
    try:
        orders = data['orders']
        for order in orders:
            order_id = order['id']
            amount = order['amount']
            price = order['price']
            orderType = order['type']
            side = order['side']
            status = order['status']
            unfilledAmount = order['amount_unfilled']
            date = arrow.get(order['date']).format('HH:mm, DD-MM-YYYY')
            pretty += '\
* Order Id: %s\n \
- Amount: %s %s \n\
- Price: %s %s \n\
- Type: %s %s \n\
- Status: %s \n\
- Unfilled amount: %s \n\
- Date: %s\n\n' % (order_id, amount, fund_id[:3], price, fund_id[3:],
                   orderType, side, status, unfilledAmount, date)
        if pretty is '':
            pretty = 'No open orders on The Rock with this fund!'
        return ('/orders', pretty)
    except:
        pretty = ('Error occured. Check your API Keys! ' +
                  'type /register to update them.')
        return ('/register', pretty)


def writedb(mdict):
    a, b, c, d, e, f, g, h = [0, 0, 0, 0, 0, 0, 0, 0]

    con = sqlite3.connect("db/logs.db")

    try:
        a = mdict["message_id"]
    except:
        pass

    try:
        b = mdict["from"]["id"]
    except:
        pass

    try:
        c = mdict["from"]["username"]
    except:
        pass

    try:
        d = mdict["from"]["first_name"]
    except:
        pass

    try:
        e = mdict["from"]["last_name"]
    except:
        pass

    try:
        f = mdict["text"]
    except:
        pass

    try:
        g = mdict["chat"]["id"]
    except:
        pass
    try:
        h = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss:SSS ZZ')
    except:
        pass

    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO log VALUES (?,?,?,?,?,?,?,?)",
                    (a, b, c, d, e, f, g, h))
