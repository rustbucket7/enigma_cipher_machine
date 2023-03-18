class Plugboard:
    """
    Defines a class simulating the function of an Enigma plugboard. The plugboard swaps an input letter with its
    assigned pair when the Enigma machine was initially set up.
    """

    def __init__(self, settings_plugboard_pairings: tuple):
        """ Set plugboard based on received settings. """

        self.plugboard = dict()

        for letter_pair in settings_plugboard_pairings:
            first_letter = letter_pair[0]
            second_letter = letter_pair[1]
            self.plugboard[first_letter] = second_letter
            self.plugboard[second_letter] = first_letter

    def plugboard_cipher(self, letter: str) -> str:
        """
        Perform substitution cipher of a letter going through the plugboard.

        If a letter was not assigned a cipher pair, return itself.
        """
        try:
            return self.plugboard[letter]
        except KeyError:
            return letter
