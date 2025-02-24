"""
The player module. Contains the player class, which regulates information related to the player. 
"""
import random
import math
from cards import PokerDeck
from util import read_file, menu_display, validate_input, clear_screen, shuffle, hand_evaluator
class Player:
    """
    The player class, represents the player and all information related to the player. 
    """
    def __init__(self):
        """
        Initializes the player object. Imports data from the save file.
        hands: Integer representing number of hands which can be played.
        discards: Integer representing times cards can be mulliganned limit 5.
        hand_size: The number of cards which can be in a hand.
        name: Name of the player.
        ante: Current difficulty level of the game.
        round: Current level of the game.
        money: Current amount of money owned by the player.
        score: Current score of the player in the current round.
        deck: Selected deck of the player.
        hand: List representing player's currently selected hand.

        """
        # Strip all lines from the file at once
        data_lines = read_file('save.txt')
        keys = [
            "hands",
            "discards",
            "hand_size",
            "name",
            "ante",
            "round",
            "money",
            "deck",
            "seed"
        ]
        data_dict = {}
        for key, line in zip(keys, data_lines):
            data_dict[key] = line.strip()
        # Initializes save data from the save file.
        self.hands = int(data_dict["hands"])
        self.discards = int(data_dict["discards"])
        self.hand_size = int(data_dict["hand_size"])
        self.name = data_dict["name"]
        self.ante = int(data_dict["ante"])
        self.round = int(data_dict["round"])
        self.money = int(data_dict["money"])
        self.deck = PokerDeck()
        self.deck.set_deck(data_dict["deck"])
        self.seed = data_dict["seed"]
        random.seed(self.seed)

        self.score = 0
        self.hand = []
    def reset(self):
        """
        Resets appropriate player values to their defaults.
        Does not reset ante, round, money, or name.
        """
        # Strip all lines from the file at once
        data_lines = read_file('save.txt')
        keys = [
            "hands",
            "discards",
            "hand_size",
            "name",
            "ante",
            "round",
            "money",
            "deck",
            "seed"
        ]
        data_dict = {}
        for key, line in zip(keys, data_lines):
            data_dict[key] = line.strip()
        self.hands = int(data_dict["hands"])
        self.discards = int(data_dict["discards"])
        self.hand_size = int(data_dict["hand_size"])
        self.money = int(data_dict["money"])
        self.deck = PokerDeck()
        self.deck.set_deck(data_dict["deck"])

class Blind():
    """
    Blind class, regulates score requirements and special effects. 
    One of these is called for each round. 

    Parameters:
        type(str): What kind of blind is this? Pass one of the
        methods below.
        difficulty (int): What ante is this blind on? 
    """
    def __init__(self, difficulty):
        self.score_requirement = 200 * math.exp2(int(difficulty))
        self.blind_type = 'Default'
        self.reward = 1

    def small_blind(self):
        """
        Small blind, has a 1X multiplier with reward of 3. 
        """
        self.score_requirement = self.score_requirement
        self.blind_type = 'Small Blind'
        self.reward = 3
    def big_blind(self):
        """
        Big blind, has a 1.5X multiplier with a reward of 5.
        """
        self.score_requirement = self.score_requirement * 1.5
        self.blind_type = 'Big Blind'
        self.reward = 5
    def wall(self):
        """
        The Wall: Has a 4X multiplier rather than the usual
        2X multiplier for boss binds.
        """
        self.score_requirement = self.score_requirement * 4
        self.blind_type = 'The Wall'
        self.reward = 7
    def challenge_query(self, player):
        """
        Challenge query calls a method which gives the
        player information about the next challenge. The player
        can accept or skip the challenge. 

        Raises: 
            ValueError: If the value of the input is not allowed.

        Returns: 
            blind_decision(bool) - Has the player accepted the challenge?
        """
        query_answer = False
        while not query_answer:
            clear_screen()
            display = {
                'Current Blind': self.blind_type,
                'Reward': str(self.reward),
                'Ante': player.ante,
                'Round': player.round,
                'Options': ''
            }
            menu_display(display)
            options = {
                '1':'Select Blind',
                '2':'Skip'
            }
            menu_display(options)
            blind_decision = None
            user_input = input('Choose an option: ')
            game_input = validate_input(user_input, options)
            match game_input:
                case '1':
                    blind_decision = True
                    query_answer = True
                case '2':
                    blind_decision = False
                    query_answer = True
                case _:
                    continue
        return blind_decision

    def challenge(self, player):
        """
        The challenge method is a method which calls a procedural
        game loop challenging the player to beat the score requirement
        with the number of hands given to them.

        Parameters:
            player (obj): The player object, representing player data.
        Returns:
            win_state (bool): Boolean representing if the game was won or not. 
        """
        shuffle(player.deck.card_deck)
        selected_cards = []
        win_state = None
        for i in range(player.hand_size - len(player.hand)):
            player.deck.deal(player.hand)
        while win_state is None:
            clear_screen()
            hand_type = hand_evaluator(selected_cards)
            print(f'{self.blind_type}: Score at least {self.score_requirement}')
            print(f'Current score is: {player.score}')
            print(f'Hands: {player.hands}')
            print(f'Discards: {player.discards}')
            if hand_type is not None:
                print(f'Hand Selected: {hand_type[0]}')
            # Display selected cards on top of the player's hand. Update every turn.
            print('Selected Cards: ')
            for index, card in enumerate(selected_cards):
                print(f'({index}. {card.suit} {card.rank})', end=' ')
            print('\n')
            print('Current Hand: ')
            for index, card in enumerate(player.hand):
                print(f'({index}. {card.suit} {card.rank})', end=' ')
            print('\n')
            display = {
                'a': 'Play',
                'b': 'Discard'
            }
            valid_choices = []
            for index, card in enumerate(player.hand):
                valid_choices.append(str(index))
            for i in display:
                valid_choices.append(str(i))
            if player.discards == 0:
                display.pop('b')
                valid_choices.remove('b')

            menu_display(display)
            user_input = input('Choose the index of a card or the options above: ')
            game_input = validate_input(user_input, valid_choices)
            index = game_input
            if game_input in valid_choices and len(selected_cards) > 0:
                match game_input:
                    case 'a':
                        hand_score = hand_evaluator(selected_cards)
                        player.score += hand_score[1]
                        player.hands -= 1
                        for i in range(player.hand_size - len(player.hand)):
                            player.deck.deal(player.hand)
                        selected_cards = []
                    case 'b':
                        player.discards -= 1
                        for i in range(player.hand_size - len(player.hand)):
                            player.deck.deal(player.hand)
                        selected_cards = []
            if game_input in valid_choices and len(selected_cards) < 5 and game_input.isdigit():
                index = int(game_input)
                if 0 <= index < len(player.hand):
                    card = player.hand.pop(index)
                    selected_cards.append(card)
            else:
                pass
            if player.score >= self.score_requirement:
                win_state = True
            elif player.hands == 0:
                win_state = False
            else:
                win_state = None
        return win_state