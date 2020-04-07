from .Deck import Deck
from .Player import Player


class Blackjack:
    def __init__(self, decks):
        self._players = []

        self.deck = Deck(decks)
        self.deck.shuffle_deck(2)

        self.actions = {
            'hit': self.hit,
            'stand': self.stand,
            'double down': self.double_down,
            'split': self.split,
            'surrender': self.surrender,
        }

    @property
    def players(self):
        return self._players

    @property
    def active_players(self):
        return [
            p for p in self.players if
            p.decisions_left != 0 and
            p.hand.sum_of_cards <= 21
        ]

    @property
    def player_names(self):
        return [p.name for p in self.players]

    @property
    def player_count(self):
        return len(self.players)

    def add_player(self, name):
        if name not in self.player_names:
            new_player = Player(name, self.deck)
            self._players.append(new_player)
        else:
            print("This name is already chosen. Choose again.")

    def play(self):
        # No winner at the start of the game
        list_of_winners = []

        # Start the game by giving each player 2 cards from the deck
        for _ in range(2):
            for player in self.players:
                player.hand.take_card()
                if Blackjack.check_blackjack(player):
                    list_of_winners.append(player)
                    player.decisions_left = 0
                    print("%s has blackjack!" % player.name)

        # while playing
        while len(self.active_players) > 0:
            for player in self.active_players:
                decision = self.get_decision(player)
                self.actions.get(decision, self.do_nothing)(player)

                if Blackjack.check_blackjack(player):
                    list_of_winners.append(player)
                    player.decisions_left = 0
                    print("%s has blackjack!" % player.name)

        # After playing
        if len(list_of_winners) == 0:
            list_of_winners = self.decide_winner()
        Blackjack.announce_winner(list_of_winners)

    def get_decision(self, player):
        print("\n%s, what is your decision?" % player.name)
        print("Current cards: %s (%s)" % (player.hand.cards, player.hand.sum_of_cards))
        possibilities = [
            "hit",
            "stand",
            "double down",
            "split",
        ]

        if player.decisions_left == -1:
            # Players can only surrender as their first decision
            possibilities.append("surrender")
            player.decisions_left = 999

        decision = self.ask_decision(possibilities)
        while decision not in possibilities:
            if decision == "soft":
                player.hand.soft = True
                print("\nTurned hand soft. Aces are now worth 11 in stead of 1")
                print("Current cards: %s (%s)\n" % (player.hand.cards, player.hand.sum_of_cards))
            elif decision == "hard":
                player.hand.soft = False
                print("\nTurned hand hard. Aces are now worth 1 in stead of 11")
                print("Current cards: %s (%s)\n" % (player.hand.cards, player.hand.sum_of_cards))
            else:
                print("decision is invalid")

            # ask again
            decision = self.ask_decision(possibilities)

        return decision

    def decide_winner(self):
        scores = [
            ((21 - p.hand.sum_of_cards), p) for p in self.players
            if p.hand.sum_of_cards <= 21
        ]

        if len(scores) > 0:
            min_score = min([score[0] for score in scores])
            winner_list = [score[1] for score in scores if score[0] == min_score]
            return winner_list
        else:
            # empty list
            return scores

    @staticmethod
    def ask_decision(possibilities):
        return input("%s, soft, hard >> " % ", ".join(possibilities)).lower()

    @staticmethod
    def hit(player):
        print("%s chose to hit" % player.name)
        player.hand.take_card()

    @staticmethod
    def stand(player):
        print("%s chose to stand" % player.name)
        player.decisions_left = 0

    @staticmethod
    def double_down(player):
        # The player is allowed to increase the initial bet by up to 100%
        # in exchange for committing to stand after receiving exactly one more card
        print("%s chose to double down" % player.name)
        player.decisions_left = 1

    @staticmethod
    def split(player):
        print("%s chose to split" % player.name)

    @staticmethod
    def surrender(player):
        print("%s chose to surrender" % player.name)
        player.decisions_left = 0

    @staticmethod
    def do_nothing(_):
        pass

    @staticmethod
    def check_blackjack(player):
        if len(player.hand.cards) == 2:
            characters = [c.character for c in player.hand.cards]
            # Check if there is a 10 and an ace
            if 10 in characters and 1 in characters:
                return True

        return False

    @staticmethod
    def announce_winner(winner):
        if len(winner) == 1:
            print("\nThe winner is: %s" % winner[0].name)
        elif len(winner) > 1:
            print("\nThe winners are: %s" % ", ".join([w.name for w in winner]))
        else:
            print("\nNo winner determined. Everyone burned.")

    def __str__(self):
        return "Currently playing with %s. %s Cards remaining in the deck" % (
            ", ".join(self.player_names), self.deck.amount_of_cards
        )

    def __repr__(self):
        return self.__str__()
