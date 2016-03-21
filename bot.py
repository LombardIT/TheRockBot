#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import Updater, ReplyKeyboardMarkup, ReplyKeyboardHide
import logging
import pytrtbot
import pickledb
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('settings.ini')
token = str(config.get('main', 'token'))

REG = {
    'apikey': None,
    'apisecret': None,
    'register': True
    }

FUNDS = ['BTCEUR', 'BTCUSD', 'LTCEUR', 'LTCBTC', 'BTCXRP',
         'EURXRP', 'USDXRP', 'LTCUSD', 'NMCBTC', 'PPCEUR',
         'EURDOG', 'PPCBTC', 'BTCDOG']

CURRENCIES = ['BTC', 'EUR', 'USD', 'LTC', 'XRP', 'NMC', 'PPC', 'DOGE']

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def home(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    db = pickledb.load('db/users.db', False)
    userId = str(update.message.from_user.id)
    try:
        registered = not db.get(userId)['register']
    except:
        registered = False
    if registered:
        reply_markup = ReplyKeyboardMarkup([['/price', '/tickers'],
                                            ['/balances', '/discounts'],
                                            ['/trades', '/transactions'],
                                            ['/orders', '/bitcoin_data'],
                                            ['/help']])
    else:
        reply_markup = ReplyKeyboardMarkup([['/price', '/tickers'],
                                            ['/bitcoin_data'],
                                            ['/register', '/help']])
    bot.sendMessage(update.message.chat_id,
                    text=pytrtbot.Home(),
                    reply_markup=reply_markup)


def help(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    db = pickledb.load('db/users.db', False)
    userId = str(update.message.from_user.id)
    try:
        registered = not db.get(userId)['register']
    except:
        registered = False
    if registered:
        reply_markup = ReplyKeyboardMarkup([['/delete_keys'],
                                            ['/home']])
    else:
        reply_markup = ReplyKeyboardMarkup([['/home']])
    bot.sendMessage(update.message.chat_id,
                    text=pytrtbot.Help(),
                    reply_markup=reply_markup)


def price(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    reply_markup = ReplyKeyboardMarkup([['/home']])
    bot.sendMessage(update.message.chat_id,
                    text=pytrtbot.Last(),
                    reply_markup=reply_markup)


def ticker(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    reply_markup = ReplyKeyboardMarkup([['/tickers'], ['/home']])
    fund_id = str(update.message.text).replace('/tick_', '')
    bot.sendMessage(update.message.chat_id,
                    text=pytrtbot.Ticker(fund_id),
                    reply_markup=reply_markup)


def tickers(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    reply = 'Select a fund to get some info on it!'
    reply_markup = ReplyKeyboardMarkup([['/tick_BTCEUR', '/tick_BTCUSD'],
                                        ['/tick_LTCEUR', '/tick_LTCBTC'],
                                        ['/tick_BTCXRP', '/tick_EURXRP'],
                                        ['/tick_USDXRP', '/tick_LTCUSD'],
                                        ['/tick_NMCBTC', '/tick_PPCEUR'],
                                        ['/tick_EURDOG', '/tick_PPCBTC'],
                                        ['/tick_BTCDOG', '/home']])
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=reply_markup)


def bitcoinData(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    reply_markup = ReplyKeyboardMarkup([['/home']])
    text = pytrtbot.bitcoinData()
    bot.sendMessage(update.message.chat_id,
                    text=text, reply_markup=reply_markup)


def register(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    db = pickledb.load('db/users.db', False)
    db.set(update.message.from_user.id, REG)
    db.dump()
    reply_markup = ReplyKeyboardHide()
    bot.sendMessage(update.message.chat_id,
                    text='Send your public API Key and API ' +
                    'secret, with a space between them.',
                    reply_markup=reply_markup)


def deleteKeys(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    db = pickledb.load('db/users.db', False)
    db.rem(str(update.message.from_user.id))
    db.dump()
    reply_markup = ReplyKeyboardMarkup([['/price', '/tickers'],
                                        ['/bitcoin_data'],
                                        ['/register', '/help']])
    bot.sendMessage(update.message.chat_id,
                    text='Your keys are deleted. You can use the bot anyway!',
                    reply_markup=reply_markup)


def signup(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    userId = str(update.message.from_user.id)
    db = pickledb.load('db/users.db', False)
    try:
        if db.get(userId)['register']:
            key = update.message.text.split()[0]
            secret = update.message.text.split()[1]
            insertApiKey = {
                'apikey': key,
                'apisecret': secret,
                'register': False
            }
            db.set(userId, insertApiKey)
            db.dump()
            reply_markup = ReplyKeyboardMarkup([['/balances'], ['/home']])
            bot.sendMessage(update.message.chat_id,
                            text='User registered! Use /balances to try it',
                            reply_markup=reply_markup)
    except:
        reply_markup = ReplyKeyboardMarkup([['/register'],
                                            ['/home'],
                                            ['/help']])
        bot.sendMessage(update.message.chat_id,
                        text='You can register! Type /register ' +
                             'and follow the instructions',
                        reply_markup=reply_markup)


def balances(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    userId = str(update.message.from_user.id)
    db = pickledb.load('db/users.db', False)
    try:
        apikey = db.get(userId)['apikey']
        apisecret = db.get(userId)['apisecret']
        markup, reply = pytrtbot.MyBalances(apikey, apisecret)
        reply_markup = ReplyKeyboardMarkup([[markup]])
        bot.sendMessage(update.message.chat_id,
                        text=reply,
                        reply_markup=reply_markup)
    except:
        reply_markup = ReplyKeyboardMarkup([['/register'], ['/home']])
        bot.sendMessage(update.message.chat_id,
                        text='You must register! Type /register ' +
                             'and follow the instructions',
                        reply_markup=reply_markup)


def transactions(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    userId = str(update.message.from_user.id)
    db = pickledb.load('db/users.db', False)
    try:
        apikey = db.get(userId)['apikey']
        apisecret = db.get(userId)['apisecret']
        markup, reply = pytrtbot.MyTransactions(apikey, apisecret)
        reply_markup = ReplyKeyboardMarkup([[markup]])
        bot.sendMessage(update.message.chat_id,
                        text=reply,
                        reply_markup=reply_markup)
    except:
        reply_markup = ReplyKeyboardMarkup([['/register'], ['/home']])
        bot.sendMessage(update.message.chat_id,
                        text='You must register! Type /register ' +
                             'and follow the instructions',
                        reply_markup=reply_markup)


def trades(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    reply = 'Select a fund to get your trades!'
    reply_markup = ReplyKeyboardMarkup([['/tr_BTCEUR', '/tr_BTCUSD'],
                                        ['/tr_LTCEUR', '/tr_LTCBTC'],
                                        ['/tr_BTCXRP', '/tr_EURXRP'],
                                        ['/tr_USDXRP', '/tr_LTCUSD'],
                                        ['/tr_NMCBTC', '/tr_PPCEUR'],
                                        ['/tr_EURDOG', '/tr_PPCBTC'],
                                        ['/tr_BTCDOG', '/home']])
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=reply_markup)


def fundTrades(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    userId = str(update.message.from_user.id)
    db = pickledb.load('db/users.db', False)
    try:
        apikey = db.get(userId)['apikey']
        apisecret = db.get(userId)['apisecret']
        fund_id = str(update.message.text).replace('/tr_', '')
        markup, reply = pytrtbot.MyTrades(apikey, apisecret, fund_id)
        reply_markup = ReplyKeyboardMarkup([[markup], ['/home']])
        bot.sendMessage(update.message.chat_id,
                        text=reply,
                        reply_markup=reply_markup)
    except:
        reply_markup = ReplyKeyboardMarkup([['/register'], ['/home']])
        bot.sendMessage(update.message.chat_id,
                        text='You must register! Type /register ' +
                             'and follow the instructions',
                        reply_markup=reply_markup)


def discounts(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    reply = 'Select a currency to get info on your discounts!'
    reply_markup = ReplyKeyboardMarkup([['/disc_BTC', '/disc_EUR'],
                                        ['/disc_USD', '/disc_LTC'],
                                        ['/disc_XRP', '/disc_NMC'],
                                        ['/disc_PPC', '/disc_DOGE'],
                                        ['/home']])
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=reply_markup)


def currDiscount(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    userId = str(update.message.from_user.id)
    db = pickledb.load('db/users.db', False)
    try:
        apikey = db.get(userId)['apikey']
        apisecret = db.get(userId)['apisecret']
        fund_id = str(update.message.text).replace('/disc_', '')
        markup, reply = pytrtbot.MyDiscount(apikey, apisecret, fund_id)
        reply_markup = ReplyKeyboardMarkup([[markup], ['/home']])
        bot.sendMessage(update.message.chat_id,
                        text=reply,
                        reply_markup=reply_markup)
    except:
        reply_markup = ReplyKeyboardMarkup([['/register'], ['/home']])
        bot.sendMessage(update.message.chat_id,
                        text='You must register! Type /register ' +
                             'and follow the instructions',
                        reply_markup=reply_markup)


def orders(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    reply = 'Select a fund to get your orders!'
    reply_markup = ReplyKeyboardMarkup([['/ord_BTCEUR', '/ord_BTCUSD'],
                                        ['/ord_LTCEUR', '/ord_LTCBTC'],
                                        ['/ord_BTCXRP', '/ord_EURXRP'],
                                        ['/ord_USDXRP', '/ord_LTCUSD'],
                                        ['/ord_NMCBTC', '/ord_PPCEUR'],
                                        ['/ord_EURDOG', '/ord_PPCBTC'],
                                        ['/ord_BTCDOG', '/home']])
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=reply_markup)


def fundOrders(bot, update):
    pytrtbot.writedb(update.message.to_dict())
    userId = str(update.message.from_user.id)
    db = pickledb.load('db/users.db', False)
    try:
        apikey = db.get(userId)['apikey']
        apisecret = db.get(userId)['apisecret']
        fund_id = str(update.message.text).replace('/ord_', '')
        markup, reply = pytrtbot.MyOrders(apikey, apisecret, fund_id)
        reply_markup = ReplyKeyboardMarkup([[markup], ['/home']])
        bot.sendMessage(update.message.chat_id,
                        text=reply,
                        reply_markup=reply_markup)
    except:
        reply_markup = ReplyKeyboardMarkup([['/register'], ['/home']])
        bot.sendMessage(update.message.chat_id,
                        text='You must register! Type /register ' +
                             'and follow the instructions',
                        reply_markup=reply_markup)


def error(bot, update, error):
    pytrtbot.writedb(update.message.to_dict())
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("start", home)
    dp.addTelegramCommandHandler("home", home)
    dp.addTelegramCommandHandler("price", price)
    dp.addTelegramCommandHandler("register", register)
    dp.addTelegramCommandHandler("balances", balances)
    dp.addTelegramCommandHandler("transactions", transactions)
    dp.addTelegramCommandHandler("trades", trades)
    dp.addTelegramCommandHandler("tickers", tickers)
    dp.addTelegramCommandHandler("discounts", discounts)
    dp.addTelegramCommandHandler("delete_keys", deleteKeys)
    dp.addTelegramCommandHandler("bitcoin_data", bitcoinData)
    dp.addTelegramCommandHandler("orders", orders)
    for fund in FUNDS:
        dp.addTelegramCommandHandler(('tr_' + fund), fundTrades)
        dp.addTelegramCommandHandler(('tick_' + fund), ticker)
        dp.addTelegramCommandHandler(('ord_'+fund), fundOrders)
    for currency in CURRENCIES:
        dp.addTelegramCommandHandler(('disc_' + currency), currDiscount)
    dp.addTelegramMessageHandler(signup)

    dp.addErrorHandler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
