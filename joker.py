"""
The Joker module holds every class and function related to joker cards in 
Joculator.
"""
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
        chips (int): The number of chips a given Joker is modifying.
        mult (int): The multiplier that a given Joker is modifying.s
    """
    def __init__(self, rarity, effect, chips, mult):
        rarity_price_chart = {
            'common': 3,
            'uncommon': 5,
            'rare': 7,
            'epic': 9,
            'legendary': 15
        }
        self.rarity = rarity
        self.price = rarity_price_chart[rarity]
        self.effect = effect
        self.chips = chips
        self.mult = mult
    def joker(self):
        """
        Defines a basic joker. The basic joker adds 4 mult to the current mult passed into
        the joker class.
        """
        self.mult += 4
