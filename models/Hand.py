class Hand:
    def __init__(self, player):
        self.cards = []
        self.player = player
        self.soft = False

    @property
    def soft(self):
        return self._soft
    @soft.setter
    def soft(self, value):
        self._soft = value

    @property
    def deck(self):
        return self.player.deck

    @property
    def cards(self):
        return self._cards
    @cards.setter
    def cards(self, value):
        self._cards = value

    @property
    def sum_of_cards(self):
        result = 0
        for card in self.cards:
            # Jack, Queen and King = 10
            result += min(card.character, 10)
            if card.character == 1 and self.soft:
                result += 10

        return result

    def take_card(self):
        self.cards.append(self.deck.give_card())
