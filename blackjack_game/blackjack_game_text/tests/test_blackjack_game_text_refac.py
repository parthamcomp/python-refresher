import pytest
import types
from blackjack_game_text.blackjack_game_text_refac import Card, Deck, Hand, Game, RANKS, SUITS

def test_card_str():
    card = Card("hearts", "A", 11)
    assert str(card) == "A of hearts"
    
def test_deck_starting_size_and_uniqueness():
    deck = Deck()
    assert len(deck) == 52
    pairs = {(card.rank_symbol, card.suit) for card in deck.cards}
    assert len(pairs) == 52
    
def test_draw_and_deal_behaviour():
    deck = Deck()
    top = deck.draw()
    assert isinstance(top, Card)
    assert len(deck) == 51
    dealt = deck.deal(3)
    assert len(dealt) == 3
    assert len(deck) == 48
    
def test_draw_empty_deck_returns_none():
    deck = Deck()
    while deck.draw():
        pass
    assert deck.draw() is None
    assert deck.deal(2) == []
    
def test_hand_add_card_single_and_iterable():
    hand = Hand()
    card_one = Card("spades", "5", 5)
    card_two = Card("hearts", "K", 10)
    hand.add_card(card_one)
    assert hand.cards == [card_one]
    hand.add_card(card_two)
    assert hand.cards == [card_one, card_two]
    
def test_add_card_none_does_nothing():
    hand = Hand()
    hand.add_card(None)
    assert hand.cards == []
    
def test_hand_values_no_aces():
    hand = Hand()
    hand.add_card(Card("spades", "10", 10))
    hand.add_card(Card("hearts", "7", 7))
    assert hand.value() == 17
    
def test_hand_value_one_ace_adjustment():
    hand_one = Hand()
    hand_one.add_card(Card("spades", "A", 11))
    hand_one.add_card(Card("hearts", "9", 9))
    assert hand_one.value() == 20
    hand_two = Hand()
    hand_two.add_card(Card("spades", "A", 11))
    hand_two.add_card(Card("clubs", "K", 10))
    hand_two.add_card(Card("hearts", "9", 9))
    assert hand_two.value() == 20
    
def test_hand_value_multiple_aces():
    hand_one = Hand()
    # adjust value of one Ace from 11 to 1
    hand_one.add_card(Card("spades", "A", 11))
    hand_one.add_card(Card("diamonds", "A", 11))
    hand_one.add_card(Card("clubs", "9", 9))
    assert hand_one.value() == 21
    hand_two = Hand()
    # adjust value of two Aces
    hand_two.add_card(Card("spades", "A", 11))
    hand_two.add_card(Card("diamonds", "A", 11))
    hand_two.add_card(Card("clubs", "9", 9))
    hand_two.add_card(Card("hearts", "K", 10))
    assert hand_two.value() == 21
    
def test_blackjack_and_bust_checks():
    hand_blackjack = Hand()
    hand_blackjack.add_card(Card("spades", "A", 11))
    hand_blackjack.add_card(Card("diamonds", "J", 10))
    assert hand_blackjack.is_blackjack()
    hand_bust = Hand()
    hand_bust.add_card(Card("spades", "J", 10))
    hand_bust.add_card(Card("spades", "K", 10))
    hand_bust.add_card(Card("spades", "2", 2))
    assert hand_bust.is_busted()
    
def test_hand_to_string_dealer_hidden_and_show():
    dealer_hand = Hand(dealer=True)
    dealer_hand.add_card(Card("spades", "K", 10))
    dealer_hand.add_card(Card("hearts", "4", 4))
    card_hidden = dealer_hand.to_string()
    assert "Hidden" in card_hidden
    card_shown = dealer_hand.to_string(show_all_dealer_cards=True)
    assert "Hidden" not in card_shown
    assert "K of spades" in card_shown
    # Message will only be displayed if assert fails
    assert "K of s" in card_shown, (
        f"Expected: K of s in dealer hand\n"
        f"Actual: {card_shown}"
    )
    
def test_player_bust_condition():
    game = Game()
    player_hand_one = Hand()
    dealer_hand_one = Hand(dealer=True)
    # Player bust
    player_hand_one.add_card(Card("s", "K", 10))
    player_hand_one.add_card(Card("h", "Q", 10))
    player_hand_one.add_card(Card("d", "2", 2))
    assert game.determine_outcome(player_hand_one, dealer_hand_one, final=False) == "player_bust"
    
def test_dealer_bust_condition():
    game = Game()
    # Dealer bust
    player_hand_two = Hand()
    dealer_hand_two = Hand(dealer=True)
    dealer_hand_two.add_card(Card("s", "K", 10))
    dealer_hand_two.add_card(Card("h", "Q", 10))
    dealer_hand_two.add_card(Card("d", "2", 2))
    assert game.determine_outcome(player_hand_two, dealer_hand_two, final=False) == "dealer_bust"
    
def test_player_dealer_tie_condition():
    game = Game()
    # Push blackjack
    player_hand_three = Hand()
    dealer_hand_three = Hand(dealer=True)
    player_hand_three.add_card(Card("s", "A", 11))
    player_hand_three.add_card(Card("h", "K", 10))
    dealer_hand_three.add_card(Card("c", "K", 10))
    dealer_hand_three.add_card(Card("d", "A", 11))
    assert game.determine_outcome(player_hand_three, dealer_hand_three, final=False) == "push_blackjack"
    
def test_player_blackjack_condition():
    game = Game()
    # Player blackjack
    player_hand_four = Hand()
    dealer_hand_four = Hand(dealer=True)
    player_hand_four.add_card(Card("s", "A", 11))
    player_hand_four.add_card(Card("h", "K", 10))
    assert game.determine_outcome(player_hand_four, dealer_hand_four, final=False) == "player_blackjack"
    
def test_player_win_condition_final():
    game = Game()
    # Player win
    player_hand_five = Hand()
    dealer_hand_five = Hand(dealer=True)
    player_hand_five.add_card(Card("s", "K", 10))
    player_hand_five.add_card(Card("c", "9", 9))
    dealer_hand_five.add_card(Card("d", "Q", 10))
    dealer_hand_five.add_card(Card("s", "8", 8))
    assert game.determine_outcome(player_hand_five, dealer_hand_five, final=True) == "player_win"
    
def test_dealer_win_condition_final():
    game = Game()
    # Dealer win
    player_hand_six = Hand()
    dealer_hand_six = Hand(dealer=True)
    player_hand_six.add_card(Card("s", "K", 10))
    player_hand_six.add_card(Card("c", "7", 7))
    dealer_hand_six.add_card(Card("d", "Q", 10))
    dealer_hand_six.add_card(Card("s", "8", 8))
    assert game.determine_outcome(player_hand_six, dealer_hand_six, final=True) == "dealer_win"
    
def test_push_condition_final():
    game = Game()
    # Dealer win
    player_hand_seven = Hand()
    dealer_hand_seven = Hand(dealer=True)
    player_hand_seven.add_card(Card("s", "K", 10))
    player_hand_seven.add_card(Card("c", "9", 9))
    dealer_hand_seven.add_card(Card("d", "Q", 10))
    dealer_hand_seven.add_card(Card("s", "9", 9))
    assert game.determine_outcome(player_hand_seven, dealer_hand_seven, final=True) == "push"