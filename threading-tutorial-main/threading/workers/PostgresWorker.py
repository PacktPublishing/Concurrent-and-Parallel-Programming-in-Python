import os
import threading

from queue import Empty

from sqlalchemy import create_engine
from sqlalchemy.sql import text


class PostgresMasterScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        if 'output_queue' in kwargs:
            kwargs.pop('output_queue')
        super(PostgresMasterScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self):
        while True:
            try:
                val = self._input_queue.get(timeout=10)
            except Empty:
                print('Timeout reached in postgres scheduler, stopping')
                break

            if val == 'DONE':
                break

            symbol, price, extracted_time = val
            postgresWorker = PostgresWorker(symbol, price, extracted_time)
            postgresWorker.insert_into_db()


class PostgresWorker():
    def __init__(self, symbol, price, extracted_time):
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time

        self._PG_USER = os.environ.get('PG_USER')
        self._PG_PW = os.environ.get('PG_PW')
        self._PG_HOST = os.environ.get('PG_HOST')
        self._PG_DB = os.environ.get('PG_DB')

        self._engine = create_engine(f'postgresql://{self._PG_USER}:{self._PG_PW}@{self._PG_HOST}/{self._PG_DB}')

    def _create_insert_query(self):
        SQL = """INSERT INTO prices (symbol, price, extracted_time) VALUES 
        (:symbol, :price, :extracted_time)"""
        return SQL

    def insert_into_db(self):
        insert_query = self._create_insert_query()

        with self._engine.connect() as conn:
            conn.execute(text(insert_query), {'symbol': self._symbol,
                                              'price': self._price,
                                              'extracted_time': str(self._extracted_time)})
