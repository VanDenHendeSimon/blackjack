class Card:
    character_aliasses = {
        1: 'Ace',
        11: 'Jack',
        12: 'Queen',
        13: 'King',
    }
    def __init__(self, character, suit):
        self.character = character
        self.suit = suit

    @property
    def suit(self):
        return self._suit
    @suit.setter
    def suit(self, value):
        self._suit = value

    @property
    def character(self):
        return self._character
    @character.setter
    def character(self, value):
        self._character = value

    @property
    def character_alias(self):
        # Lookup the character, if its not in the table, set it to the given value
        return Card.character_aliasses.get(self.character, self.character)

    def __str__(self):
        return '%s of %s' % (self.character_alias, self.suit)

    def __repr__(self):
        return self.__str__()
