from models.Deck import Deck
from models.Player import Player
from models.Blackjack import Blackjack
import os


def main():
    game = Blackjack(1)
    game.add_player("Bimie")
    game.add_player("Lunie")

    game.play()


if __name__ == '__main__':
    os.system("cls")
    main()
