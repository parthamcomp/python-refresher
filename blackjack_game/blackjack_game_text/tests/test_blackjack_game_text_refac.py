import pytest
import types
from blackjack_game_text.blackjack_game_text_refac import Card, Deck, Hand, Game, RANKS, SUITS

def test_card_str():
    c = Card("hearts", "A", 11)
    assert str(c) == "A of hearts"