from .Deck import Deck
from .Player import Player
import os


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
        return sum([p.current_bet for p in self.players]) * self.payout_wage

    @property
    def starting_bet(self):
        return self._starting_bet
    @starting_bet.setter
    def starting_bet(self, value):
        self._starting_bet = value

    def add_player(self, name, index=None):
        if name not in self.player_names:
            if not index:
                new_player = Player(name, self.deck)
                self._players.append(new_player)
                print("The starting bet is: %s" % self.starting_bet)
            else:
                # Only inserting when splitting, so no need to greet the second hand here
                new_player = Player(name, self.deck, skip_greeting=True)
                self._players.insert(index, new_player)

            return new_player
        else:
            print("This name is already chosen. Choose again.")
            return None

    def play(self):
        # No winner at the start of the game
        list_of_winners = []

        # Start the game by giving each player 2 cards from the deck
        for _ in range(2):
            for player in self.players:
                player.hand.take_card()
                # update the list of winners if this is necassery
                list_of_winners = Blackjack.check_blackjack(player, list_of_winners)
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
        else:
            # 3:2
            self.payout_wage *= 1.5

        self.show_cards()
        Blackjack.announce_winner(list_of_winners)
        Blackjack.give_out_payment(list_of_winners, self.wager)

    def get_decision(self, player):
        print("\n%s, what is your decision?" % player.name)
        Blackjack.print_player_cards(player)
        possibilities = [
            "hit",
            "stand",
            "double down",
        ]

        if player.decisions_left == -1:
            # Players can only surrender as their first decision
            possibilities.append("surrender")
            player.decisions_left = 999

            # List has to be of length 2
            # (There hasnt been any decisions yet and players start with 2 cards)
            # Splitting is allowed on face cards and 10s as well (10 & king / 10 & Jack / ...)
            # If you want to limit this to only 10s change the character property in the Card class
            if player.hand.cards[0].character == player.hand.cards[1].character:
                # 2 Cards are the same -> possibility to split into 2 hands
                possibilities.append("split")

        decision = self.ask_decision(possibilities)
        while decision not in possibilities:
            if decision == "soft":
                player.hand.soft = True
                print("\nTurned hand soft. Aces are now worth 11 in stead of 1")
                Blackjack.print_player_cards(player)
            elif decision == "hard":
                player.hand.soft = False
                print("\nTurned hand hard. Aces are now worth 1 in stead of 11")
                Blackjack.print_player_cards(player)
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
        os.system("cls")
        print("%s chose to double down" % player.name)

        # Put the player that doubled down as the first index of the queried list
        active_players.remove(player)
        active_players.insert(0, player)

        # ask what the rest of the players want to do
        for _player in active_players:
            if _player != player:
                # ask to double
                Blackjack.print_player_cards(_player, new_line=True)
                double_down = input("would you like to double your wager as well, %s? [y/n] >> " % _player.name)
                if double_down == "y":
                    _player.current_bet *= 2
            else:
                # Dont ask, just double it
                _player.current_bet *= 2

            # ask for another card
            Blackjack.print_player_cards(_player, new_line=True)
            another_card = input("would you like to hit once more, %s? [y/n] >> " % _player.name)
            if another_card == "y":
                Blackjack.hit(_player)

            _player.decisions_left = 0

    def split(self, player):
        # if the two cards have the same value, separate them to make two hands
        print("%s chose to split" % player.name)

        # Create new player for the second hand of the current player
        second_hand = self.add_player(player.name + " (2)", index=self.active_players.index(player)+1)

        # Link the two players' capitals
        second_hand.wallet = player.wallet

        # Match first hand's bet (out of the same wallet)
        Blackjack.take_money(second_hand, player.current_bet)

        # Change initial player's name
        player.name = player.name + " (1)"

        # Split cards
        second_hand.hand.cards = [player.hand.cards[1]]
        player.hand.cards = [player.hand.cards[0]]

        # draw an additional card for each
        player.hand.take_card()
        second_hand.hand.take_card()

        # Now that both hands have 2 cards, check for blackjack
        Blackjack.check_blackjack(player, [])
        Blackjack.check_blackjack(second_hand, [])

    @staticmethod
    def surrender(player):
        # The house takes half of the player's bet and returns the other half to the player
        print("%s chose to surrender" % player.name)
        player.capital += (player.current_bet * 0.5)
        player.decisions_left = 0

    @staticmethod
    def do_nothing(_):
        pass

    @staticmethod
    def check_blackjack(player, winners):
        if len(player.hand.cards) == 2:
            characters = [c.character for c in player.hand.cards]
            # Check if there is a 10 and an ace
            if 10 in characters and 1 in characters:
                print("*** %s has blackjack! ***" % player.name)
                winners.append(player)
                player.decisions_left = 0

        return winners

    def show_cards(self):
        print("\n" + "*" * 20)
        print("Game is done!")
        print("*" * 20 + "\n")
        for player in self.players:
            Blackjack.print_player_cards(player)

    @staticmethod
    def announce_winner(winner):
        if len(winner) == 1:
            print("\nThe winner is: %s" % winner[0].name)
        elif len(winner) > 1:
            print("\nThe winners are: %s" % ", ".join([w.name for w in winner]))
        else:
            print("\nNo winner determined. Everyone burned.")

    @staticmethod
    def give_out_payment(winners, wager):
        print("Wager of the game: %s" % wager)
        for winner in winners:
            # Divide total wager over all winners
            winner.wallet.capital += (wager / len(winners))
            print(winner.wallet.capital)

    @staticmethod
    def take_money(player, amount):
        if amount <= player.wallet.capital:
            player.current_bet += amount
            player.wallet.capital -= amount
        else:
            print("%s can not afford to play anymore. Bitch's broke" % player.name)

    @staticmethod
    def print_player_cards(player, new_line=False):
        if new_line:
            print("")

        card_value = player.hand.sum_of_cards if not \
            len(Blackjack.check_blackjack(player, [])) > 0 else "BLACKJACK"
        print("%s's cards: %s (%s)" % (player.name, player.hand.cards, card_value))

    def __str__(self):
        return "Currently playing with %s. %s Cards remaining in the deck" % (
            ", ".join(self.player_names), self.deck.amount_of_cards
        )

    def __repr__(self):
        return self.__str__()
