import json
from random import randrange
from time import sleep
from typing import Any

import requests

import config
from database import Database
from item import *


class _BuffParser:
    def __init__(self):
        self.items = set()

    def export_to_db(self):
        print('Saving data...')
        items = [vars(item) for item in self.items]
        with Database(config.DATABASE_USER, config.DATABASE_PASSWORD, config.DATABASE_HOST, config.DATABASE) as db:
            db.update_many(items, config.DATABASE_NAME)
        print(f'Saved {len(self.items)} items')


class BuffURLParser(_BuffParser):
    def __init__(self):
        self.sale = False
        self.page = config.START_PAGE
        super().__init__()

    def start(self):
        print('Fetching data...')
        try:
            for url in config.URLS:
                self.page = 1
                response = self.get_response(url)
                self.parse_response(response['data']['items'])
                while self.page < response['data']['total_page']:
                    self.page += 1
                    response = self.get_response(url)
                    self.parse_response(response['data']['items'])
        except KeyError:
            print('-' * 45)
            print('Temporarily cooldown received from buff')
            print(f'Last scraped page was {self.page - 1} in the {"sellings" if self.sale else "buying"} tab')
            print('-' * 45)

        self.export_to_db()

    def get_response(self, url: str) -> Any:
        while True:
            params = config.PARAMS
            if 'buying' not in url:
                self.sale = True
                params['use_suggestion'] = '0'
                params['trigger'] = 'undefined_trigger'
            else:
                self.sale = False
            params['page_num'] = self.page
            try:
                response = requests.get(url, params=params, cookies=config.COOKIES, headers=config.HEADERS)
                if response.status_code == 200:
                    json_response = json.loads(response.text)
                    print(f'[{self.page}/{json_response["data"]["total_page"]}] Parsing: {response.url}')
                    return json_response
            except requests.exceptions.ConnectionError:
                print('No internet - waiting 30 seconds to try again...')
                sleep(30)

            sleep(randrange(5, 10))

    def parse_response(self, responses: list):
        for response in responses:
            item = ItemURL(response)
            self.items.add(item)


class BuffAPIParser(_BuffParser):
    def __init__(self, start_code: int, end_code: int):
        self.start = start_code
        self.end = end_code
        self.code = -1
        super().__init__()

    def start_parsing(self):
        print('Fetching data...')
        for self.code in range(self.start, self.end):
            response = self.get_response(config.URL_API)
            self.parse_response(response)

        self.export_to_db()

    def get_response(self, url: str) -> Any:
        while True:
            params = config.PARAMS
            params['goods_id'] = self.code
            params['page_size'] = 1
            try:
                response = requests.get(url, params=params, headers=config.HEADERS)
                if response.status_code == 200:
                    json_response = json.loads(response.text)
                    print(f'[{self.code}/{self.end}] Parsing: {response.url}')
                    return json_response
            except requests.exceptions.ConnectionError:
                print('No internet - waiting 30 seconds to try again...')
                sleep(30)

            sleep(randrange(5, 10))

    def parse_response(self, data: dict):
        if data['code'] == 'OK' and data['data']['total_count'] > 0:
            item = ItemAPI(data['data']['goods_infos'][str(self.code)])
            self.items.add(item)
