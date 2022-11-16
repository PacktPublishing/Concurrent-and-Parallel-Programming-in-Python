import threading
import datetime
import random
import time
from queue import Empty

import requests
from lxml import html


class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue, output_queue, **kwargs):
        super(YahooFinancePriceScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        temp_queue = output_queue
        if type(temp_queue) != list:
            temp_queue = [temp_queue]
        self._output_queues = temp_queue
        self.start()

    def run(self):
        while True:
            try:
                val = self._input_queue.get(timeout=10)
            except Empty:
                print('Yahoo scheduler queue is empty, stopping')
                break
            if val == 'DONE':
                break

            yahooFinacePriceWorker = YahooFinacePriceWorker(symbol=val)
            price = yahooFinacePriceWorker.get_price()
            for output_queue in self._output_queues:
                output_values = (val, price, datetime.datetime.utcnow())
                output_queue.put(output_values)
            time.sleep(random.random())


class YahooFinacePriceWorker():
    def __init__(self, symbol):
        self._symbol = symbol
        base_url = 'https://finance.yahoo.com/quote/'
        self._url = f'{base_url}{self._symbol}'

    def get_price(self):
        r = requests.get(self._url)
        if r.status_code != 200:
            return
        page_contents = html.fromstring(r.text)
        raw_price = page_contents.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')[0].text
        price = float(raw_price.replace(',', ''))
        return price
