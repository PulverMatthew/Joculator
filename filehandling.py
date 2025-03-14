"""Module randomizes seed to be implemented by the save file."""
import random
class FileHandler:
    """
    File handler class for Joculator. The concept behind this file handling system is the following:
    1. Specified text file is opened if found, created if not.
    2. Data is kept in memory as long as the FileHandler is used. File is read on init.
    3. Whenever data is needed from the FileHandler object, can be read from memory. 
    4. Whenever data must be updated, can be stored in memory and updated at program close. 

    tl;dr: Try to read file/create file. Handle IO in memory as much as possible.
    """
    def __init__(self, name):
        """
        Initiates a file. If the file is not found of the given name, make a new one.

        Parameters:
        name (str): Name of the file to be read or created with file extension included.
        """
        self.name = name
        try:
            with open(name, 'r', encoding='utf-8') as file:
                self.data = file.readlines()
        except FileNotFoundError:
            seed_input = random.random()
            self.data = [
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
            self.write_file(self.data)

    # Returns the value of the specified line in file.
    def read_file(self, index):
        """
        Reads a formatting stripped version of a given line of the specified FileHandler.

        Parameters:
        index (int): Integer representing the index of the file, or the line.

        Returns:
        selected_data (str): String of the given file line stripped of formatting.
        """
        selected_data = str(self.data[index]).strip()
        return selected_data

    def write_file(self, data):
        """
        Saves a given file configuration in memory, to be updated to file later.

        Parameters:
        data (lst): A list containing every piece of data in the given file.
        """
        self.data = data
    def close_file(self):
        """
        Writes to the file with current data in memory. Meant to be used on quit. 
        """
        # Whenever you close the game, write the existing data from memory into file.
        with open(self.name, 'w', encoding='utf-8') as file:
            file.writelines(self.data)
