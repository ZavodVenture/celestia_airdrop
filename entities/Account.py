from entities import Proxy


class Account:
    seed = ''
    address = ''
    proxy: Proxy = None

    def __init__(self, seed, address, host=None, port=None, user=None, password=None):
        self.seed = seed
        self.address = address
        if host and port and user and password:
            self.proxy = Proxy(host, port, user, password)
