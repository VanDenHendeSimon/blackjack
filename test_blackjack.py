from models.Deck import Deck
from models.Player import Player
from models.Blackjack import Blackjack
import os


def main():
    # Initialize a game of blackjack, using 1 deck of cards
    game = Blackjack(1)

    # Check if all players can be created
    if game.add_player("Bimie") is not None:
        if game.add_player("Drienie") is not None:
            # If all players have been created, start the game
            game.play()


if __name__ == '__main__':
    os.system("cls")
    main()
