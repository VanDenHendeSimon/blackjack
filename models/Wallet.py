class Wallet:
    def __init__(self):
        self.capital = 0

    @property
    def capital(self):
        return self._capital
    @capital.setter
    def capital(self, value):
        self._capital = value
