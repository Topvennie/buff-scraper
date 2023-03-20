class Item:
    def __init__(self, data: dict):
        self.code = data['id']
        self.name = data['name']
        self.type = data['goods_info']['info']['tags']['type']['localized_name']
        self.icon_url = data['goods_info']['icon_url']
        self.steam_market_url = data['steam_market_url']

    def __hash__(self):
        return self.code
