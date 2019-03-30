from carousell_query import CarousellQuery
import time

# shares state with carousell poll.
# hacky but hey.
class CarousellPollWorker:
  def __init__(self, poller):
    self.poll_worker(poller)

  def poll_worker(self, poller):
    while poller.started:
      try:
        products = self.query(poller)
        poller.alert_listeners(products)
      except Exception as e:
        print(e)
      finally:
        time.sleep(poller.freq_seconds)

  # queries carousell and returns all the new products in increasing chronological order
  def query(self, poller):
    carousell_query = CarousellQuery(poller.keyword)
    new_products = carousell_query.get_new_products(poller.last_sent_product_id)
    # update last_sent_product_id in the CarousellPoll state
    # TODO: VERY HACKY
    if len(new_products) > 0:
      poller.last_sent_product_id = new_products[0]['id']
    return list(reversed(new_products))
