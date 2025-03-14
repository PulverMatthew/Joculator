"""
Game module, houses the game logic for readability.
"""
from util import clear_screen
from settings import settings
from player import Player, Blind
# from cards import PokerCard, PokerDeck
def play_game(file_handler):
    """
    Basic game loop.
    """
    clear_screen()
    # Checks to see if the player has played the game before.
    has_previous_game = file_handler.read_file(9)
    # Update to reflect new game having been started
    if has_previous_game == 'False':
        data = file_handler.read_file('save.txt')
        data[9] = 'True\n'
        file_handler.write_file('save.txt', data)
    # Check to see if the player wants to restart the game or continue.
    elif has_previous_game == 'True':
        user_input = input("You have a previous game, continue? (Y/N) ").lower()
        match user_input:
            # Resume the last game
            case 'y':
                input("Resuming your last game...")
                clear_screen()
            # Generate new save, allow player to modify settings, set game bool to true.
            case 'n':
                input("You can modify your settings here before you start the new game.")
                settings(file_handler)
                file_handler.data[8] = 'True\n'
                clear_screen()
    player = Player(file_handler)
    outcome = None
    while player.ante < 8:
        current_ante = Blind(player.ante)
        current_ante.small_blind()
        choice = current_ante.challenge_query(player)
        match choice:
            case True:
                outcome = current_ante.challenge(player)
            case False:
                outcome = True
        if outcome:
            player.shop()
        elif not outcome:
            clear_screen()
            input('You lose.')
            file_handler.close_file()
            exit()
        current_ante = Blind(player.ante)
        current_ante.big_blind()
        choice = current_ante.challenge_query(player)
        match choice:
            case True:
                outcome = current_ante.challenge(player)
            case False:
                outcome = True
        if outcome:
            player.shop()

        elif not outcome:
            clear_screen()
            input('You lose.')
            file_handler.close_file()
            exit()
        current_ante = Blind(player.ante)
        current_ante.wall()
        choice = current_ante.challenge_query(player)
        match choice:
            case True:
                outcome = current_ante.challenge(player)
            case False:
                pass
        if outcome:
            player.ante += 1
            player.shop()

        elif not outcome:
            clear_screen()
            input('You lose.')
            file_handler.close_file()
            exit()
    clear_screen()
    input('You win!')
    file_handler.close_file()
