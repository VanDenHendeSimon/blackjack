from .Deck import Deck
from .Player import Player


class Blackjack:
    def __init__(self, decks):
        self._players = []

        self.deck = Deck(decks)
        self.deck.shuffle_deck(2)

        self.starting_bet = 12.5
        # x times the wager
        self.payout_wage = 1

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

    @property
    def wager(self):
        return sum([p.current_bet for p in self.players])

    @property
    def starting_bet(self):
        return self._starting_bet
    @starting_bet.setter
    def starting_bet(self, value):
        self._starting_bet = value

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
                # update the list of winners if this is necassery
                list_of_winners = self.check_blackjack(player, list_of_winners)
                Blackjack.take_money(player, self.starting_bet*0.5)

        # while playing
        while len(self.active_players) > 0:
            for player in self.active_players:
                decision = self.get_decision(player)
                if decision == "double down":
                    self.actions.get(decision, self.do_nothing)(player, self.active_players)
                    # make sure that the game ends after running the code above
                    break
                else:
                    self.actions.get(decision, self.do_nothing)(player)

        # After playing
        if len(list_of_winners) == 0:
            list_of_winners = self.decide_winner()
        self.show_cards()
        Blackjack.announce_winner(list_of_winners)
        print("Wager of the game: %s" % self.wager)

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
    def double_down(player, active_players):
        # The player is allowed to increase the initial bet by up to 100%
        # in exchange for committing to stand after receiving exactly one more card
        # Other players can choose to double down as well,
        # but they have to stand after taking maximum one more card
        print("%s chose to double down" % player.name)

        # Put the player that doubled down as the first index of the queried list
        active_players.remove(player)
        active_players.insert(0, player)
        print(active_players)

        # ask what the rest of the players want to do
        for _player in active_players:
            if _player != player:
                # ask to double
                double_down = input("\nwould you like to double your wager as well, %s? [y/n] >> " % _player.name)
                if double_down == "y":
                    _player.current_bet *= 2
            else:
                # Dont ask, just double it
                _player.current_bet *= 2

            # ask for another card
            another_card = input("would you like to hit once more, %s? [y/n] >> " % _player.name)
            if another_card == "y":
                Blackjack.hit(_player)

            _player.decisions_left = 0

    @staticmethod
    def split(player):
        # if the two cards have the same value, separate them to make two hands
        print("%s chose to split" % player.name)
        if len(player.hand.cards) == 2:
            if player.hand.cards[0] == player.hand.cards[1]:
                pass

    @staticmethod
    def surrender(player):
        # The house takes half of the player's bet and returns the other half to the player
        print("%s chose to surrender" % player.name)
        player.capital += (player.current_bet * 0.5)
        player.decisions_left = 0

    @staticmethod
    def do_nothing(_):
        pass

    def check_blackjack(self, player, winners):
        if len(player.hand.cards) == 2:
            characters = [c.character for c in player.hand.cards]
            # Check if there is a 10 and an ace
            if 10 in characters and 1 in characters:
                print("*** %s has blackjack! ***" % player.name)
                winners.append(player)
                player.decisions_left = 0
                # 3:2
                self.payout_wage = 1.5

        return winners

    def show_cards(self):
        print("Game is done!\n")
        for player in self.players:
            print("%s had: %s (%s)" % (
                player.name, player.hand.cards, player.hand.sum_of_cards
            ))

    @staticmethod
    def announce_winner(winner):
        if len(winner) == 1:
            print("\nThe winner is: %s" % winner[0].name)
        elif len(winner) > 1:
            print("\nThe winners are: %s" % ", ".join([w.name for w in winner]))
        else:
            print("\nNo winner determined. Everyone burned.")

    @staticmethod
    def take_money(player, amount):
        if amount <= player.capital:
            player.current_bet += amount
            player.capital -= amount
        else:
            print("%s can not afford to play anymore. Bitch's broke" % player.name)

    def __str__(self):
        return "Currently playing with %s. %s Cards remaining in the deck" % (
            ", ".join(self.player_names), self.deck.amount_of_cards
        )

    def __repr__(self):
        return self.__str__()
