class Wallet:
    """
    This is made an object so that players who split their hand can share the same wallet
    aka capital
    """
    def __init__(self):
        self.capital = 0

    @property
    def capital(self):
        return self._capital
    @capital.setter
    def capital(self, value):
        self._capital = value
