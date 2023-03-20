import json
import random
import time
from typing import Any

import requests

import config
from database import Database
from item import Item


class BuffParser:
    def __init__(self):
        self.database = Database(config.DATABASE_USER, config.DATABASE_PASSWORD, config.DATABASE_HOST, config.DATABASE)
        self.sale = False
        self.page = config.START_PAGE
        self.items = set()

    def start(self) -> None:
        print('Fetching data...')
        try:
            for url in config.URLS:
                self.page = 1
                response = self.get_response(url, self.page)
                self.parse_response(response['data']['items'])
                while self.page < response['data']['total_page']:
                    self.page += 1
                    response = self.get_response(url, self.page)
                    self.parse_response(response['data']['items'])
        except KeyError:
            print('-' * 45)
            print('Temporarily cooldown received from buff')
            print(f'Last scraped page was {self.page - 1} in the {"sellings" if self.sale else "buying"} tab')
            print('-' * 45)

        print('Saving data...')
        self.export_to_db()
        print(f'Saved {self.items.__len__()} items')

    def get_response(self, url: str, page: int) -> Any:
        while True:
            params = config.PARAMS
            if 'buying' not in url:
                self.sale = True
                params['use_suggestion'] = '0'
                params['trigger'] = 'undefined_trigger'
            else:
                self.sale = False
            params['page_num'] = page
            response = requests.get(url, params=params, cookies=config.COOKIES, headers=config.HEADERS)
            if response.status_code == 200:
                json_response = json.loads(response.text)
                print(f'[{page}/{json_response["data"]["total_page"]}] Parsing: {response.url}')
                return json_response

            time.sleep(random.randrange(5, 10))

    def parse_response(self, responses: list) -> None:
        for response in responses:
            item = Item(response)
            self.items.add(item)

    def export_to_db(self) -> None:
        items = [item.__dict__ for item in self.items]
        with self.database as db:
            db.update_many(items, config.DATABASE_NAME)


if __name__ == '__main__':
    BuffParser().start()
