"""
util.py: provides utility functions for the rest of Joculator:
    validate_input validates given inputs, used for menus.
    check_file, read_file, write_file do file handling tasks.
    save_generation makes a save file if one doesn't exist.
    clear_screen clears the screen and is cross-platform on Linux and Windows.
    menu_display provides a readable alternative for making menu options.
"""
import os
import random
from cards import PokerCard
def shuffle(original_deck):
    """
    Method which shuffles the selected deck.
    Implementation of the Fisher-Yates shuffle algorithm.

    Parameters: original_deck (lst): An unshuffled list.

    Returns: original_deck (lst): A list which has been shuffled.
    """
    original_deck_range = len(original_deck)
    for i in range(original_deck_range-1, 0, -1):
        j = random.randint(0, i)
        original_deck[i], original_deck[j] = original_deck[j], original_deck[i]
    return original_deck

def sort_suit(original_deck):
    """
    Sorting method implementing a hybrid bucket sort/selection sort algorithm.
    First, sublists are made from the original list sorted by suit.
    Second, each sublist is selection sorted based on rank value hierarchy.
    Finally, append a new list in suit order and return the sorted

    Parameters: original_deck (lst): A list to be sorted.

    Returns: modified_deck (lst): A list which is sorted.
    """
    buckets = {}
    # Put same-suit cards in sublists.
    for card in original_deck:
        if card.suit not in buckets:
            buckets[card.suit] = []
        buckets[card.suit].append(card)
    # For every sublist, selection sort the sublist by rank.
    for card_list in buckets.values():
        for i in range(len(card_list) - 1):
            min_index = i
            for j in range(i + 1, len(card_list)):
                compare_1 = PokerCard.rank_hierarchy_lookup[card_list[j].rank]
                compare_2 = PokerCard.rank_hierarchy_lookup[card_list[min_index].rank]
                if compare_1 < compare_2:
                    min_index = j
            card_list[i], card_list[min_index] = card_list[min_index], card_list[i]
    modified_deck = []
    # Append the sublists in suit order.
    for suit in PokerCard.suits:
        if suit in buckets:
            modified_deck += buckets[suit]
    for card in modified_deck:
        print(card.suit)
    return modified_deck
def sort_rank(original_deck):
    """
    Selection sort which sorts by rank irrespective of suit.
    Parameters:
        original_deck (lst): The original deck to be sorted.

    Returns:
        original_deck (lst): The original deck in rank-sorted form.
    """
    original_deck = []
    for i in range(len(original_deck) - 1):
        min_index = i
        for j in range(i + 1, len(original_deck)):
            compare_1 = PokerCard.rank_hierarchy_lookup[original_deck[j].rank]
            compare_2 = PokerCard.rank_hierarchy_lookup[original_deck[min_index].rank]
            if compare_1 < compare_2:
                min_index = j
        original_deck[i], original_deck[min_index] = original_deck[min_index], original_deck[i]
    return original_deck
def hand_evaluator(played_hand):
    """
    Evaluates identity of the given played hand. 
    Evaluates mult value and chip value based on evaluated
    hand, evaluates all modifiers as well.
    Animates evaluation process for suspense.
    Adds together mult value and returns added score

    Parameters:
        played_hand (lst): List of cards selected by the player.
    Returns:
        eval_data (tuple): A tuple containing a string of the hand name
        and a score containing the evaluated value of the played hand.
    """
    # if played hand is null, break out of the function.
    if played_hand == []:
        return None
    # Entry is as follows: Name:{mult, chips}
    hand_score_lookup = {
        'high': [1, 5],
        'pair': [2, 5],
        '2pair': [2, 10],
        '3kind': [3, 15],
        'straight': [5, 20],
        'flush': [5, 25],
        'fullhouse': [5,35],
        '4kind': [10, 50],
        'straightflush': [20,100],
        'flushhouse': [25, 100],
        '5kind': [25, 100],
        'flush5': [50, 100]
    }
    # Card patterns for which hand matches.
    hand_descriptors = ['high']
    # Play what cards are a part of the hand.
    active_cards = []

    # Straight: Sort the list by rank, and check if each rank is consecutive. No low aces.
    sort_rank(played_hand)
    consecutive_ranks = 0
    for i in range(len(played_hand)-1):
        if PokerCard.rank_hierarchy_lookup[played_hand[i].rank] - PokerCard.rank_hierarchy_lookup[played_hand[i+1].rank] == 1:
            consecutive_ranks += 1
    if consecutive_ranks == 4:
        hand_descriptors.append('straight')
        active_cards = played_hand
    # Pair, 2 Pair, 3Kind, 4Kind, Full House:
    buckets = {}
    for card in played_hand:
        if card.rank not in buckets:
            buckets[card.rank] = []
        buckets[card.rank].append(card)
    # Corresponds to: ["2 of a kind", "3 of a kind", "4 of a kind", "5 of a kind"]
    of_kind = [0, 0, 0, 0]
    for card_list in buckets.values():
        match len(card_list):
            case 1:
                active_cards = card_list
            case 2:
                of_kind[0] += 1
                active_cards += card_list
            case 3:
                of_kind[1] += 1
                active_cards += card_list
            case 4:
                of_kind[2] += 1
                active_cards += card_list

            case 5:
                of_kind[3] += 1
                active_cards += card_list

    match of_kind:
        # Single pair found
        case [1,0,0,0]:
            hand_descriptors[0] = 'pair'
        # Two pairs found
        case [2,0,0,0]:
            hand_descriptors[0] = '2pair'
        # One 3-kind found
        case [0,1,0,0]:
            hand_descriptors[0] = '3kind'
        # One pair, and one 3-kind found.
        case [1,1,0,0]:
            hand_descriptors[0] = 'fullhouse'
        # One 4-kind found
        case [0,0,1,0]:
            hand_descriptors[0] = '4kind'
        # One 5-kind found
        case [0,0,0,1]:
            hand_descriptors[0] = '5kind'
    # Flush: same suit as first, 5 cards in deck
    check_suit = played_hand[0].suit
    same_suit = 0
    for card in played_hand:
        if card.suit == check_suit:
            same_suit += 1
    if same_suit == 5:
        hand_descriptors.append('flush')
        active_cards = played_hand
    eval_score = [1,5]
    eval_name = 'high'
    eval_data = (eval_name, eval_score)
    if len(active_cards) < 5:
        eval_score = hand_score_lookup[hand_descriptors[0]]
        eval_name = hand_descriptors[0]
    try:
        if hand_descriptors[1] == 'flush':
            eval_score = hand_score_lookup['flush']
            eval_name = 'flush'
        match (hand_descriptors[0], hand_descriptors[1]):
            case ('straight', 'flush'):
                eval_score = hand_score_lookup['straightflush']
                eval_name = 'straight flush'
            case ('fullhouse', 'flush'):
                eval_score = hand_score_lookup['flushhouse']
                eval_name = 'flush house'
            case ('5kind', 'flush'):
                eval_score = hand_score_lookup['flush5']
                eval_name = 'flush five'
    except IndexError:
        pass
    for card in active_cards:
        # eval_score[0] = placeholder for multiplier.
        eval_score[1] += card.chips
        evaluated_score = eval_score[0] * eval_score[1]
        eval_data = (eval_name, evaluated_score)
    # returns added mult and chip value.
    return eval_data

def validate_input(message, valid_options=None):
    """
    Validates the provided input message against the valid_options.

    Parameters:
        message (str): The input provided by the user.
        valid_options (list, optional): A list of valid options. If None, any message is valid.

    Raises: 
        ValueError: If the value of the input is not allowed.
        
    Returns:
        str: The original message if it is valid.
    """
    message = message.lower()
    try:
        if valid_options is None or message in valid_options:
            return message
        if message not in valid_options:
            print("Not a valid input!")
    except ValueError as ve:
        print(f"Input error: {ve}")


# List of allowed filenames
filenamesAllowed = ['save.txt']

# Returns the value of the specified line in file.
def check_file(filename, index):
    """
    Returns the content of the specified line in the file.

    Parameters:
        filename (str): The name of the file to read.
        index (int): The index of the line to retrieve.

    Returns:
        str: The content of the specified line, stripped of extra whitespace.

    Raises:
        ValueError: If the filename is not allowed.
    """
    if filename not in filenamesAllowed:
        raise ValueError('Invalid filename')
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.readlines()
    # Explicit close is not needed due to context manager usage.
    selected_data = data[index]
    return str(selected_data).strip()

# Reads file and returns its content as a list of lines.
def read_file(filename):
    """
    Reads the provided file and returns its contents as a list of lines.

    Parameters:
        filename (str): The name of the file to read.

    Returns:
        list: A list containing each line from the file.

    Raises:
        ValueError: If the filename is not allowed.
    """
    if filename not in filenamesAllowed:
        raise ValueError('Invalid filename')
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.readlines()
    return data

# Writes the provided data to the file.
def write_file(filename, data):
    """
    Writes the provided data to a file.

    Parameters:
        filename (str): The name of the file to write to.
        data (list): A list of strings to write into the file.

    Raises:
        ValueError: If the filename is not allowed.
    """
    if filename not in filenamesAllowed:
        raise ValueError('Invalid filename')
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(data)

# Makes a save file in the game's main script directory.
def save_generation():
    """
    Checks for the existence of the save file. If the save file is not found, 
    creates one with default values.
    """
    try:
        read_file('save.txt')
    except FileNotFoundError:
        clear_screen()
        user_input = input('What should the seed be? Enter arbitrary characters.')
        seed_input = validate_input(user_input)
        random.seed(seed_input)
        data = [
            '4\n',  # 1. Number of Hands
            '3\n',  # 2. Number of Discards
            '7\n',  # 3. Hand Size
            'Jack Joculator\n', # 4. Name
            '1\n', # 5. Current ante
            '1\n', # 6. Current round
            '4\n', # 7. Current Money
            'Default\n', # 8. Chosen card deck
            f'{seed_input}\n' # 10 What is the current seed? 
            'False\n',  # 9 Has a game already been started?

        ]
        write_file('save.txt', data)

# Clear the terminal screen in a cross-platform way.
def clear_screen() -> None:
    """
    Clears the terminal screen using the appropriate command for the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# Displays custom menu options.
def menu_display(options):
    """
    Displays menu options on the console.

    Parameters:
        options (dict): A dictionary of options where the key is option and value is descriptor.
    """
    for key, value in options.items():
        print(f"{key}: {value}")
