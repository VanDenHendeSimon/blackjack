from models.Deck import Deck
from models.Player import Player
from models.Blackjack import Blackjack
import os


def main():
    game = Blackjack(1)
    if game.add_player("Bimie") is not None:
        if game.add_player("Drienie") is not None:
            print("Game started succesfully")

    game.play()


if __name__ == '__main__':
    os.system("cls")
    main()
