from .Card import Card
import random


class Deck:
    def __init__(self, amount):
        self.__suits = [
            'Clubs',
            'Diamonds',
            'Hearts',
            'Spades',
        ]

        self._cards = []
        self.__fill_deck(amount)

    @property
    def cards(self):
        return self._cards

    @property
    def amount_of_cards(self):
        return len(self.cards)

    def __fill_deck(self, amount=1):
        # amount of decks to mix together
        for _ in range(amount):
            for suit in self.__suits:
                # 13 Cards in each suit
                for i in range(13):
                    card = Card(i+1, suit)
                    self.cards.append(card)

    def shuffle_deck(self, amount):
        # Shuffle the deck x amounts of time
        for _ in range(amount):
            random.shuffle(self.cards)

    def give_card(self):
        card = self.cards[0]
        self._cards = self.cards[1:]
        return card

    def __str__(self):
        return "Deck with %s cards" % self.amount_of_cards

    def __repr__(self):
        return self.__str__()
