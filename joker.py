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
        self.rarity = None
        self.price = None
        self.effect = None

    def apply(self, score):
        """
        Calls the stored effect with the given score.
        """
        if self.effect:
            return self.effect(score)
        else:
            raise ValueError("No effect function provided")

    def define_type(self, joker_type):
        """
        Defines type of joker.
        
        Parameters:
            type (str): The type of joker being defined.
        """
        type_information_lookup = {
            'joker': ['Basic Joker', 'Common', 3, self.joker]
        }
        jonkler = type_information_lookup[joker_type]
        self.name = jonkler[0]
        self.rarity = jonkler[1]
        self.price = jonkler[2]
        self.effect = jonkler[3]

    def joker(self, score):
        """
        Defines a basic joker. The basic joker adds 4 mult to the current mult passed into
        the joker class.
        
        Common (Costs 3 dollars): Adds 4 to mult.

        Parameters:
        score (lst): A list containing mult and score of the current hand.

        Returns:
        score (lst): A list containing mult and score modified by the joker.
        """
        score[0] += 4
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
