from .Hand import Hand


class Player:
    def __init__(self, name, current_deck):
        self.name = name
        self._deck = current_deck
        self._hand = Hand(self)

        self.current_bet = 0
        self.decisions_left = -1

        self.greet_player()

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def current_bet(self):
        return self._current_bet
    @current_bet.setter
    def current_bet(self, value):
        self._current_bet = value

    @property
    def decisions_left(self):
        return self._decisions_left
    @decisions_left.setter
    def decisions_left(self, value):
        self._decisions_left = value

    @property
    def deck(self):
        return self._deck

    @property
    def hand(self):
        return self._hand

    def greet_player(self):
        print("welcome %s, enjoy the game" % self.name)

    def __str__(self):
        return "%s" % self.name

    def __repr__(self):
        return self.__str__()
