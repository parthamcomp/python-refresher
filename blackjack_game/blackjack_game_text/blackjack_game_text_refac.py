# blackjack_refactor.py
import random
from dataclasses import dataclass
from typing import List, Optional, Iterable, Union, Tuple

RANKS = [
    ("A", 11), ("2", 2), ("3", 3), ("4", 4), ("5", 5),
    ("6", 6), ("7", 7), ("8", 8), ("9", 9), ("10", 10),
    ("J", 10), ("Q", 10), ("K", 10)
]
SUITS = ["spades", "clubs", "diamonds", "hearts"]

@dataclass(frozen=True)
class Card:
    suit: str
    rank_symbol: str
    rank_value: int

    def __str__(self):
        return f"{self.rank_symbol} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards: List[Card] = [
            Card(suit, symbol, value)
            for suit in SUITS
            for symbol, value in RANKS
        ]

    def shuffle(self) -> None:
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def draw(self) -> Optional[Card]:
        return self.cards.pop() if self.cards else None

    def deal(self, n: int) -> List[Card]:
        dealt: List[Card] = []
        for _ in range(n):
            c = self.draw()
            if c is None:
                break
            dealt.append(c)
        return dealt

    def __len__(self) -> int:
        return len(self.cards)

class Hand:
    def __init__(self, dealer: bool = False):
        self.cards: List[Card] = []
        self.dealer = dealer

    def add_card(self, value):
        if value is None:
            return
        if isinstance(value, Card):
            self.cards.append(value)
        else:
            self.cards.extend(value)


    def value(self) -> int:
        total = 0
        aces = 0
        for c in self.cards:
            total += c.rank_value
            if c.rank_symbol == "A":
                aces += 1
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.value() == 21

    def is_busted(self) -> bool:
        return self.value() > 21

    def to_string(self, show_all_dealer_cards: bool = False) -> str:
        lines = [f"{'Dealer' if self.dealer else 'Your'} hand:"]
        for i, c in enumerate(self.cards):
            if i == 0 and self.dealer and not show_all_dealer_cards and not self.is_blackjack():
                lines.append("Hidden")
            else:
                lines.append(str(c))
        if not self.dealer:
            lines.append(f"Value: {self.value()}")
        return "\n".join(lines)

class Game:
    def ask_number_of_games(self) -> int:
        while True:
            try:
                n = int(input("How many games do you want to play? "))
                if n > 0:
                    return n
                print("Enter a positive number.")
            except ValueError:
                print("You must enter a number!")

    def ask_hit_or_stand(self) -> str:
        while True:
            choice = input("Please choose 'Hit' or 'Stand' (H/S): ").strip().lower()
            if choice in ("h", "hit"):
                return "hit"
            if choice in ("s", "stand"):
                return "stand"
            print("Please enter 'Hit' or 'Stand' or H/S.")

    def initial_deal(self, deck: Deck) -> Tuple[Hand, Hand]:
        player = Hand()
        dealer = Hand(dealer=True)
        for _ in range(2):
            player.add_card(deck.draw())
            dealer.add_card(deck.draw())
        return player, dealer

    def player_turn(self, deck: Deck, player: Hand) -> None:
        while player.value() < 21:
            choice = self.ask_hit_or_stand()
            if choice == "stand":
                break
            player.add_card(deck.draw())

    def dealer_turn(self, deck: Deck, dealer: Hand) -> None:
        while dealer.value() < 17:
            dealer.add_card(deck.draw())

    def determine_outcome(self, player: Hand, dealer: Hand, final: bool = False) -> str:
        if not final:
            if player.is_busted():
                return "player_bust"
            if dealer.is_busted():
                return "dealer_bust"
            if player.is_blackjack() and dealer.is_blackjack():
                return "push_blackjack"
            if player.is_blackjack():
                return "player_blackjack"
            if dealer.is_blackjack():
                return "dealer_blackjack"
            return "none"
        pv, dv = player.value(), dealer.value()
        if pv > dv:
            return "player_win"
        if pv == dv:
            return "push"
        return "dealer_win"

    def print_outcome(self, code: str, player: Hand, dealer: Hand) -> None:
        mapping = {
            "player_bust": "You busted! Dealer wins.",
            "dealer_bust": "Dealer busted! You win.",
            "push_blackjack": "Both players got blackjack! Tied.",
            "player_blackjack": "You have blackjack! You win.",
            "dealer_blackjack": "Dealer has blackjack! Dealer wins.",
            "player_win": "You win!",
            "push": "Tie!",
            "dealer_win": "Dealer wins!",
            "none": None
        }
        msg = mapping.get(code)
        if msg:
            print(msg)

    def play(self) -> None:
        games_to_play = self.ask_number_of_games()
        for game_number in range(1, games_to_play + 1):
            deck = Deck()
            deck.shuffle()
            player, dealer = self.initial_deal(deck)

            print("\n" + "*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print("*" * 30)
            print(player.to_string())
            print()
            print(dealer.to_string())  # hides by default
            print()

            # early checks (blackjack/bust)
            code = self.determine_outcome(player, dealer, final=False)
            if code != "none":
                self.print_outcome(code, player, dealer)
                continue

            # player's turn
            self.player_turn(deck, player)
            code = self.determine_outcome(player, dealer, final=False)
            if code != "none":
                self.print_outcome(code, player, dealer)
                continue

            # dealer's turn
            self.dealer_turn(deck, dealer)

            # show final hands
            print(dealer.to_string(show_all_dealer_cards=True))
            print()

            code = self.determine_outcome(player, dealer, final=False)
            if code != "none":
                self.print_outcome(code, player, dealer)
                continue

            print("Final Results")
            print("Your hand:", player.value())
            print("Dealer's hand:", dealer.value())
            final_code = self.determine_outcome(player, dealer, final=True)
            self.print_outcome(final_code, player, dealer)

        print("\nThanks for playing!")

if __name__ == "__main__":
    Game().play()
