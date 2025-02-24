"""
Settings module, allows settings to be called from anywhere in the program without an ImportError.
"""
from util import menu_display, read_file, write_file, clear_screen, validate_input
def settings():
    """
    Settings function which allows the user to modify the save file containing game settings.
    Settings cannot be changed if a game is currently being played.
    This is mainly meant to prevent cheating, but nothing stops you from modifying the save file. 
    """
    # Reads save file and copies it to variable 'data' then closes.
    save_settings = False
    data = read_file('save.txt')
    # Opens save file in write mode. Loops until player has confirmed every setting changed.
    while not save_settings:
        clear_screen()
        print('Current values:')
        labels = {
            0: 'Hands',
            1: 'Discards',
            2: 'Hand Size',
            3: 'Name',
            4: 'Ante',
            5: 'Round',
            6: 'Money',
            7: 'Deck',
            8: 'Seed',
        }
        for index, entry in enumerate(data):
            label = labels.get(index)
            print(f'{label}: {entry.strip()}', end=', ')
        print('\n')
        menu_options = {
            '1': 'Name',
            '2': 'Deck Style',
            '3': 'Difficulty',
            '4': 'Seed',
            '5': 'Save Settings'
        }
        print('Game Options:\n')
        menu_display(menu_options)
        user_input = input('Choose an option: ')
        game_input = validate_input(user_input, menu_options)
        clear_screen()
        match game_input:
            case '1':
                user_input = input('What is your name? ')
                game_input = validate_input(user_input)
                if game_input == '':
                    data[3] = 'Jack Joculator\n'
                else:
                    data[3] = game_input + '\n'
            case '2':
                menu_options = {
                    '1': 'Default Deck: Standard deck used in card games.',
                    '2': 'Oops, Spades and Hearts: Has 2 copies of every spade/heart rank.',
                }
                menu_display(menu_options)
                user_input = input('Choose an option: ')
                game_input = validate_input(user_input, valid_options=menu_options)
                match game_input:
                    case '1':
                        data[7] = 'Default\n'
                    case '2':
                        data[7] = 'Oops\n'
                    case _:
                        continue
            case '3':
                menu_options = {
                    '1': 'Easy: Start with 6 hands, 4 discards, 10 card hand, and 10 money',
                    '2': 'Medium: Start with 4 hands, 3 discards, 7 card hand, and 4 money',
                    '3': 'Hard: Start with 2 hands, 2 discards, 7 card hand, and 0 money',
                    '4': 'Mission: Improbable: Has 1 hand, 0 discards, 7 card hand, and 0 money' 
                }
                menu_display(menu_options)
                user_input = input('Choose an option: ')
                game_input = validate_input(user_input, menu_options)
                match game_input:
                    case '1':
                        data[0] = '6\n'
                        data[1] = '4\n'
                        data[2] = '10\n'
                        data[6] = '10\n'
                    case '2':
                        data[0] = '4\n'
                        data[1] = '3\n'
                        data[2] = '7\n'
                        data[6] = '4\n'
                    case '3':
                        data[0] = '2\n'
                        data[1] = '2\n'
                        data[2] = '7\n'
                        data[6] = '0\n'
                    case '4':
                        data[0] = '2\n'
                        data[1] = '0\n'
                        data[2] = '7\n'
                        data[6] = '0\n'
                    case _:
                        continue
            case '4':
                user_input = input('What seed do you want? ')
                game_input = validate_input(user_input)
                data[8] = game_input + '\n'
            case '5':
                write_file('save.txt', data)
                save_settings = True

            case _:
                save_settings = False
