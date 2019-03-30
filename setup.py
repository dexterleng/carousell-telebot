import telebot
import time
from carousell_poll import CarousellPoll
import json

credentials = None

with open('credentials.json', 'r') as credentials_json:
    credentials = json.load(credentials_json)

token = credentials['bot_token']
chat_id = credentials['chat_id']
bot = telebot.TeleBot(token, True)
carousell_poller = None

def telegram_listener(products):
  for product in products:
    url = 'https://sg.carousell.com/p/' + product['id']
    message = """
Title: {}

Additional Info: {}

Price: {}

Used Status: {}

Seller: {}

URL: {}

""".format(product['title'], product['primaryAttribute'], product['price'], product['secondaryAttribute'], product['sellerUsername'], url)
    bot.send_message(chat_id, message)

@bot.message_handler(commands=['listen'])
def listen_to_keyword(message):
  if message.chat.id != chat_id:
    return
  keyword = message.text.replace('/listen', '').strip()
  if len(keyword) == 0:
    return
  # stop the existing polling worker
  global carousell_poller
  if carousell_poller is not None:
    carousell_poller.stop()
  carousell_poller = CarousellPoll(keyword, 60)
  carousell_poller.add_listener(telegram_listener)
  bot.send_message(chat_id, "You are now subscribed to the \"{}\" keyword.".format(keyword))
  carousell_poller.start()

bot.polling()
