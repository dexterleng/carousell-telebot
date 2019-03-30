from carousell_poll_worker import CarousellPollWorker
import threading
import time

class CarousellPoll:
  def __init__(self, keyword, freq_seconds):
    self.keyword = keyword
    self.freq_seconds = freq_seconds
    self.listeners = []
    self.started = False
    self.last_sent_product_id = None
    self.poll_thread = threading.Thread(target=lambda : CarousellPollWorker(self))

  def add_listener(self, listener):
    self.listeners.append(listener)
  
  def set_listeners(self, listeners):
    self.listeners = listeners
  
  def alert_listeners(self, products):
    for listener in self.listeners:
      listener(products)

  def start(self):
    self.started = True
    self.poll_thread.start()
  
  def stop(self):
    self.started = False
