"""
cards.py: Contains classes for objects in Joculator related to playing cards, 
such as numbered cards, face cards, and aces. Will implement Jokers,
and other cards found in Balatro later.
"""
class PokerCard:
    """
    The PokerCard object represents a standard playing card in a playing card deck.
    Has a suit, rank, and a chip value. 3 ranks are face cards and each object can
    have its suit, rank, or chip value dynamically changed depending on game state.
    """
    # Valid poker suits
    suits = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
    # Valid poker ranks
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    rank_hierarchy_lookup = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 14
        }
    def __init__(self, suit, rank):
        """
        Initializes the PokerCard object with a suit, rank, and chip value.

        Parameters:
            suit (str) (): Specifies the suit of the playing card.
            rank (str): Specifies the rank of the playing card.
            'Clubs', 'Spades', 'Hearts', 'Diamonds'
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'J', 'Q', 'K'


        Raises: ValueError if the suit or rank is not a valid suit or rank.
        """
        # Defines suits and ranks.
        if suit not in PokerCard.suits:
            raise ValueError(f'Invalid suit: {suit}')
        if rank not in PokerCard.ranks:
            raise ValueError(f'Invalid rank: {rank}')
        self.suit = suit
        self.rank = rank
        # Checks to see if the card has been modified in game.
        self.is_modified = False
        # Chip value can be intuited based on rank value. If a face card, then 10. If ace, then 11.
        self.chips = rank
        if self.chips in ('J', 'Q', 'K'):
            self.chips = 10
        elif self.chips in ('A'):
            self.chips = 11
        else:
            self.chips = int(self.rank)
        # If the rank is J, Q, or K, then set is_face to true.
        self.is_face = False
        if str(self.rank) in ('J', 'Q', 'K'):
            self.is_face = True
    def set_suit(self, suit):
        """
        Setter method for the suit value for a PokerCard object.
        
        Parameters:
            suit (str): Suit which a PokerCard object is being changed to.

        Raises: ValueError if suit is invalid.
        """
        if suit not in PokerCard.suits:
            raise ValueError(f'Invalid suit: {suit}')
        self.suit = suit
        self.is_modified = True
    # Setter method for rank.
    def set_rank(self, rank):
        """
        Setter method for the rank value for a PokerCard object.
        Unless the card has already been modified:
        If the rank is a jack, queen, or king, change the chips to 10.
        If the rank is an ace, change the chips to 11.
        
        Parameters:
            rank (str): rank which a PokerCard object is being changed to.

        Raises: ValueError if rank is invalid.
        """
        if rank not in PokerCard.ranks:
            raise ValueError(f'Invalid rank: {rank}')
        self.rank = rank
        # If set rank is J, Q, or K, then set chips to 10 and designates as a face card.
        if str(self.rank) in ('J', 'Q', 'K') and self.is_modified is False:
            self.chips = 10
            self.is_face = True
        # If ace, set chips to 11.
        elif str(self.chips) in ('A') and self.is_modified is False:
            self.chips = 11
        self.is_modified = True
    def set_chips(self, chips):
        """
        Setter method for the chips value for a PokerCard object.
        
        Parameters:
            chips (int): The chip value which a PokerCard object is being changed to.
        """
        self.chips = chips
        self.is_modified = True
    def set_face(self, face_card):
        """
        Setter method for the boolean deciding if a card is considered a face card.
        
        Parameters:
            face_card (bool): Is the card a face card or not a face card?
        """
        self.is_face = face_card
        self.is_modified = True
class PokerDeck:
    """
    The PokerDeck object describes an object containing a list of PokerCard objects.
    Can be configured with various custom deck types, uses a standard poker deck as
    a default setting.
    """
    def __init__(self):
        """
        Instantiates the PokerDeck object. Makes an empty card_deck list and
        tracks the length of the deck.
        """
        self.card_deck = []
        for suit in PokerCard.suits:
            for rank in PokerCard.ranks:
                self.card_deck.append(PokerCard(suit, rank))
        self.card_count = len(self.card_deck)
    def set_deck(self, deck):
        """
        Setter method for the deck which sets the type of deck used.
        
        Parameters:
            deck (str): A string representing a deck to change to.
        """
        match deck:
            case 'Default':
                new_deck = self.default_deck()
            case 'Oops':
                new_deck = self.oops_spade_hearts_deck()
        self.card_deck = new_deck
        self.card_count = len(new_deck)
    def deal(self, target_list):
        """
        Sends the first card in a deck to the specified list.
        Parameters:
            target_list (lst): The list for which the poker card
            will be sent to. 
        """
        selected_hand = self.card_deck.pop()
        target_list.append(selected_hand)
    def default_deck(self):
        """
        Generates the default deck of playing cards.
        Has one card of each acceptable suit and rank.
        Contains 52 cards in the deck.

        Returns:
            deck: A list containing every generated poker card.
        """
        deck = []
        for suit in PokerCard.suits:
            for rank in PokerCard.ranks:
                deck.append(PokerCard(suit, rank))
        return deck
    def oops_spade_hearts_deck(self):
        """
        Generates a deck similar to the default deck,
        but has 2 copies of spade and heart suite cards.
        Contains 52 cards in the deck.

        Returns:
            deck: A list containing every generated poker card.
        """
        deck = []
        for rank in PokerCard.ranks:
            for _ in range(2):
                deck.append(PokerCard('Spades', rank))
        for rank in PokerCard.ranks:
            for _ in range(2):
                deck.append(PokerCard('Hearts', rank))
        return deck
