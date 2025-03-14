"""
test_units is a module designed to test core Joculator functions,
methods, and objects.
Tests utility functions, poker card objects, and the poker deck
functionalities.

"""
from cards import PokerCard, PokerDeck
from util import validate_input, shuffle, hand_evaluator, Sorter

def test_utility_functions():
    """
    Function which tests utility functions.
    Tests the input validation to make sure that invalid
    inputs are caught and valid inputs are accepted.
    """
    card1 = PokerCard('Hearts', '6')
    card2 = PokerCard('Hearts', '2')
    card3 = PokerCard('Hearts', '3')
    card4 = PokerCard('Hearts', '4')
    card5 = PokerCard('Hearts', '5')
    card6 = PokerCard('Hearts', '5')
    card7 = PokerCard('Hearts', '5')
    card8 = PokerCard('Hearts', '5')
    card11 = PokerCard('Hearts', '6')
    card12 = PokerCard('Hearts', '5')
    card13 = PokerCard('Clubs', '5')
    card14 = PokerCard('Clubs', '6')
    empty = []
    high_card = [card1, card2, card3, card4]
    pair = [card5, card6, card1, card2]
    pair2 = [card1, card11, card5, card6]
    kind3 = [card5, card6, card7, card1]
    kind4 = [card5, card6, card7, card8]
    kind5 = [card5, card6, card7, card8, card13]
    flush5 = [card5,card6,card7,card8,card12]
    fullhouse = [card1, card11, card13, card5, card6]
    flushhouse = [card1, card11, card5, card6, card7]
    flush = [card1, card2, card3, card7, card8]
    straight = [card2,card3,card4,card5, card14]
    straightflush = [card1, card2, card3, card4, card5]
    assert hand_evaluator(empty) is None
    assert hand_evaluator(high_card) == 'high'
    assert hand_evaluator(pair) == 'pair'
    assert hand_evaluator(pair2) == '2pair'
    assert hand_evaluator(kind3) == '3kind'
    assert hand_evaluator(kind4) == '4kind'
    assert hand_evaluator(kind5) == '5kind'
    assert hand_evaluator(flush5) == 'flush five'
    assert hand_evaluator(fullhouse) == 'fullhouse'
    assert hand_evaluator(flushhouse) == 'flush house'
    assert hand_evaluator(flush) == 'flush'
    assert hand_evaluator(straight) == 'straight'
    assert hand_evaluator(straightflush) == 'straight flush'


    menu_options = {
        'test1': 'test2',
        'test3': 'test4',
        'test5': 'test6',
    }
    assert validate_input('InvalidInput', menu_options) is None
    assert validate_input('test1', menu_options) == 'test1'

    # Testing shuffle and sorting algorithm

    # Default Deck
    default_deck_original = PokerDeck()
    default_deck_modified = PokerDeck()
    default_deck_modified.card_deck = shuffle(default_deck_modified.card_deck)
    default_deck_modified.card_deck = Sorter.sort_suit(default_deck_modified.card_deck)
    for i in range(default_deck_modified.card_count):
        assert (default_deck_original.card_deck[i].suit, default_deck_original.card_deck[i].rank) == (default_deck_modified.card_deck[i].suit, default_deck_modified.card_deck[i].rank)

    # Oops Deck
    oops_original = PokerDeck()
    oops_original.set_deck('Oops')
    oops_modified = PokerDeck()
    oops_modified.set_deck('Oops')
    oops_modified.card_deck = shuffle(oops_modified.card_deck)
    oops_modified.card_deck = Sorter.sort_suit(oops_modified.card_deck)
    for i in range(oops_original.card_count):
        assert (oops_original.card_deck[i].suit, oops_original.card_deck[i].rank) == (oops_modified.card_deck[i].suit, oops_modified.card_deck[i].rank)


def test_poker_card_identity():
    """
    Tests PokerCard object identity to make sure functionality works.
    Makes sure face cards and aces have correct chip value.
    Makes sure every suit works.
    Makes sure face and non-face cards are identified correctly.
    """
    card1 = PokerCard('Hearts', 'A')
    assert (card1.suit, card1.rank, card1.chips, card1.is_face) == ('Hearts', 'A', 11, False)

    card2 = PokerCard('Spades', '10')
    assert (card2.suit, card2.rank, card2.chips, card2.is_face) == ('Spades', '10', 10, False)

    card3 = PokerCard('Diamonds', 'J')
    assert (card3.suit, card3.rank, card3.chips, card3.is_face) == ('Diamonds', 'J', 10, True)

    card4 = PokerCard('Clubs', '7')
    assert (card4.suit, card4.rank, card4.chips, card4.is_face) == ('Clubs', '7', 7, False)

def test_poker_card_setters():
    """
    Tests setter methods for the PokerCard object.
    Makes sure functionality is different if card is new or modified.
    Allows chip value to be changed regardless of rank or suit.
    Makes sure default chip value is maintained regardless of rank
    or suit.
    Makes sure face card trueness is maintained if a non-face card is
    treated as a face card.
    """
    card1 = PokerCard('Hearts', 'A')
    card1.set_suit('Diamonds')
    assert card1.suit == 'Diamonds'

    card2 = PokerCard('Spades', '10')
    card2.set_rank('A')
    assert card2.rank == 'A'

    card3 = PokerCard('Diamonds', 'J')
    card3.set_chips(200)
    assert card3.chips == 200

    card3.set_rank('J')
    assert card3.chips == 200

    card4 = PokerCard('Clubs', '7')
    card4.set_face(True)
    assert card4.is_face is True
    card4.set_rank('10')
    assert card4.is_face is True

def test_poker_deck():
    """
    Tests PokerDeck object functionality.
    Makes sure that the default deck actually generates
    a proper playing card deck, containing all of the cards
    of a correct suit and rank.py
    Checks that the length of the deck is correct.
    """
    # Testing default deck with all suit/rank pairs.
    default_deck = PokerDeck()
    suits = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    default_deck_check = [(suit, rank) for suit in suits for rank in ranks]
    for card in default_deck.card_deck:
        assert (card.suit, card.rank) in default_deck_check
    assert len(default_deck.card_deck) == default_deck.card_count
    assert default_deck.card_count == len(default_deck_check)

    # Testing oops spades hearts deck with all spades and hearts.
    oops_deck = PokerDeck()
    oops_deck.set_deck('Oops')
    suits = ['Spades', 'Hearts']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    oops_deck_check = [(suit, rank) for suit in suits for rank in ranks for _ in range(2)]
    for card in oops_deck.card_deck:
        assert (card.suit, card.rank) in oops_deck_check
    assert len(oops_deck.card_deck) == oops_deck.card_count
    assert oops_deck.card_count == len(oops_deck_check)
test_utility_functions()
test_poker_card_identity()
test_poker_card_setters()
test_poker_deck()
