# Simulated Bitget Client for local import
class Client:
    def __init__(self, api_key, api_secret, passphrase, use_server_time=True): pass
    def mix_place_order(self, **kwargs): return {'result': 'simulated_order'}
    def mix_get_account(self, symbol, marginCoin): return {'data': {'available': '100'}}
