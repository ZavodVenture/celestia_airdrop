class Proxy:
    ip = ""
    port = ""
    login = ""
    password = ""

    def __init__(self, ip, port, login, password):
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

    def __str__(self):
        return f'{self.ip}:{self.port}:{self.login}:{self.password}'