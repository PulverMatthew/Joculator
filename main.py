"""
Main module of the game. Contains functions for settings
and for the main menu. 
"""
from util import validate_input, clear_screen, menu_display
from filehandling import FileHandler
from game import play_game
from settings import settings
def main():
    """
    Main loop, only valid way to start the program and contains the main menu.
    Access the game, game settings, credits menu, and exit from here.
    """
    default_file = FileHandler('save.txt')
    game_loop = True
    while game_loop:
        menu_options = {
            '1': 'Play',
            '2': 'Settings',
            '3': 'Credits',
            '4': 'Quit'
        }
        clear_screen()
        print('Welcome to Joculator\n')
        menu_display(menu_options)
        user_input = input('Choose an option: ')
        game_input = validate_input(user_input, menu_options)

        match game_input:
            case '1':
                play_game(default_file)

            case '2':
                settings(default_file)

            case '3':
                clear_screen()
                credits_menu = {
                    'Joculator, based on the game "Balatro"': '',
                    'Balatro by': 'LocalThunk',
                    'Programming by': 'Matthew Pulver',
                    'Planning by': 'Matthew Pulver'
                }
                menu_display(credits_menu)
                user_input = input('Press enter to continue...')
                validate_input(user_input)

            case '4':
                clear_screen()
                # Writes current save data found in memory to save file.
                default_file.close_file()
                game_loop = False

            case _:
                continue


if __name__ == '__main__':
    main()
