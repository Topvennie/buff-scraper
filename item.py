import config


class ItemURL:
    def __init__(self, data: dict):
        self.code = data['id']
        self.name = data['name']
        self.type = data['goods_info']['info']['tags']['type']['localized_name']
        self.icon_url = data['goods_info']['icon_url']
        self.steam_market_url = data['steam_market_url']

    def __hash__(self):
        return self.code


class ItemAPI:
    def __init__(self, data: dict):
        self.code = data['goods_id']
        self.name = data['name']
        self.type = data['tags']['type']['localized_name']
        self.icon_url = data['icon_url']
        self.steam_market_url = self.make_steam_market_url(self.name)

    def __hash__(self):
        return self.code

    def make_steam_market_url(self, name: str) -> str:
        for key, value in config.REPLACE_DICT.items():
            if key in name:
                name = name.replace(key, value)

        return 'https://steamcommunity.com/market/listings/730/' + name
