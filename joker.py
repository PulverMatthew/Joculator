"""
The Joker module holds every class and function related to joker cards in 
Joculator.
"""
from util import clear_screen
class JokerCard:
    """
    The JokerCard object is an object which allows for the special effects
    based on the method called for its effect. Some Jokers will add mult, muliply
    mult, or add chips, sometimes only if a condition is met. 
    
    Parameters:
        rarity (Str): The rarity of a card. The rarer a card is the less there are
        in the given game.
        effect (method): Passes a given joker method into the constructor. Allows
        for special effects depending on what is called.
        score(lst): A list consisting of [chips, mult] which is passed into a joker
        card for modification
    """
    def __init__(self):
        self.name = None
        self.description = None
        self.rarity = None
        self.price = None
        self.effect = None

    def apply(self, score, card_deck=None, joker_deck=None):
        """
        Calls the stored effect with the given score.
        """
        if self.effect:
            return self.effect(score, card_deck, joker_deck)
        else:
            raise ValueError("No effect function provided")

    def define_type(self, joker_type):
        """
        Defines type of joker.
        
        Parameters:
            type (str): The type of joker being defined.
        """
        type_information_lookup = {
            'joker': ['Basic Joker', 'Common', 3, 'Adds +3 Mult to your score.', self.joker],
            'greedy_joker': ['Greedy Joker', 'Common', 3, 'Adds +3 Mult for every diamond card.', self.greedy_joker],
            'lusty_joker': ['Lusty Joker', 'Common', 3, 'Adds +3 Mult for every heart card.', self.lusty_joker],
            'wrathful_joker': ['Wrathful Joker', 'Common', 3, 'Adds +3 Mult for every spade card.', self.wrathful_joker],
            'gluttonous_joker': ['Gluttonous Joker', 'Common', 3, 'Adds +3 Mult for every club card.', self.gluttonous_joker],
        }
        jonkler = type_information_lookup[joker_type]
        self.name = jonkler[0]
        self.rarity = jonkler[1]
        self.price = jonkler[2]
        self.description = jonkler[3]
        self.effect = jonkler[4]

    def joker(self, score, card_deck=None, joker_deck=None):
        """
        Defines a basic joker. The basic joker adds 4 mult to the current mult passed into
        the joker class.
        
        Common (Costs 3 dollars): Adds 4 to mult.

        Parameters:
        score (lst): A list containing( mult and score of the current hand.

        Returns:
        score (lst): A list containing mult and score modified by the joker.
        """
        score[0] += 4
        return score
    def greedy_joker(self, score, card_deck=None, joker_deck=None):
        """
        Played cards add +3 mult if they have a diamond suit.
        """
        for card in card_deck:
            match card.suit:
                case 'Diamonds':
                    score[0] += 3
        return score
    def lusty_joker(self, score, card_deck=None, joker_deck=None):
        """
        Played cards add +3 mult if they have a hearts suit.
        """
        for card in card_deck:
            match card.suit:
                case 'Hearts':
                    score[0] += 3
        return score
    def wrathful_joker(self, score, card_deck=None, joker_deck=None):
        """
        Played cards add +3 mult if they have a spade suit.
        """
        for card in card_deck:
            match card.suit:
                case 'Spades':
                    score[0] += 3
        return score
    def gluttonous_joker(self, score, card_deck=None, joker_deck=None):
        """
        Played cards add +3 mult if they have a club suit.
        """
        for card in card_deck:
            match card.suit:
                case 'Clubs':
                    score[0] += 3
        return score


class JokerDeck:
    """
    The JokerDeck class stores any Joker cards gained by the player.
    It has a defined length which can be modified during gameplay.
    
    """
    def __init__(self):
        self.card_deck = []
        self.deck_count = len(self.card_deck)
        self.card_limit = 5

    def add(self, joker):
        """
        Adds a joker to the deck, assuming your deck has space.
        """
        if self.deck_count < self.card_limit:
            self.card_deck.append(joker)
        else:
            clear_screen()
            input('You have too many jokers in your deck!')
