from plugboard import *
from reflector import *
from rotor import *


class Enigma:
    """
    Defines a class simulating the functionality of the German Enigma I and M3
    cipher machines used by the German Army and Air Force during WW2.

    Uses rotors 1-5 and reflectors A-C.
    """

    def __init__(self,
                 settings_rotor_choices: tuple,  # (1, 2, 3)
                 settings_plugboard_pairings: tuple,  # tuple(ab, cd, ...)
                 settings_starting_rotor_pos: tuple,  # ('X', 'X', 'X')
                 settings_ring: tuple,  # ('X', 'X', 'X')
                 settings_reflector: str):  # 'X'

        """ Define initial variable values of an Enigma object. """

        # grab initial settings when an Enigma object is initialized
        self.rotor_order = settings_rotor_choices  # tuple(1,2,3)
        self.starting_rotor_pos = settings_starting_rotor_pos  # ('X', 'X', 'X')
        self.settings_ring = settings_ring  # ('X', 'X', 'X')

        # setup plugboard and reflector based on initialized settings
        self.plugboard = Plugboard(settings_plugboard_pairings)  # ex. {"EA": "GM", "GM":"EA"}
        self.reflector = Reflector(settings_reflector)  # ex. "B"
        self.rotors_used = self.set_rotors()  # ex. [3,1,5]

    # # test methods here
    # def get_rotor_order(self):
    #     """ Testing Only: Output 3 chosen rotors. """
    #     return self.rotor_order
    #
    # def get_settings_ring(self):
    #     """ Testing Only: Output ring settings received. """
    #     return self.settings_ring
    #
    # def get_settings_plugboard(self):
    #     """ Testing Only: Output plugboard settings received. """
    #     return self.settings_plugboard
    #
    # def get_starting_rotor_pos(self):
    #     """ Testing Only: Output initial rotor position received. """
    #     return self.starting_rotor_pos
    #
    # def get_plugboard(self):
    #     """ Testing Only: Output final plugboard settings. """
    #     return self.plugboard
    #
    # def get_reflector(self):
    #     """ Testing Only: Output reflector pairings. """
    #     return self.reflector

    # enigma machine methods here
    def set_rotors(self) -> list:
        """ Set the starting positions of the Enigma rotors and determine which rotor outputs to use as well as their
        ring setting alteration based on user settings. """

        rotor_outputs_to_use = []

        # configure each chosen rotor based on desired starting position and ring setting letter
        for i in range(3):
            new_rotor = Rotor(rotor_chosen=self.rotor_order[i],
                              starting_rotor_pos_letter=self.starting_rotor_pos[i],
                              ring_setting_letter=self.settings_ring[i])
            rotor_outputs_to_use.append(new_rotor)

        return rotor_outputs_to_use  # list of 3 Rotor objects

    def advance_rotors(self):
        """ Check if more than 1 rotor needs to move. Then move right rotor forward 1 step. """

        middle_rotor_step = self.rotors_used[2].check_to_step_adjacent_rotor()
        left_rotor_step = self.rotors_used[1].check_to_step_adjacent_rotor()

        # step right rotor (always occurs)
        self.rotors_used[2].step_rotor()

        # step the middle rotor if possible
        if middle_rotor_step is True:
            self.rotors_used[1].step_rotor()

        # step the left rotor if possible
        if left_rotor_step is True:
            self.rotors_used[0].step_rotor()

    def right_to_left_cipher(self, letter: str, prev_rotor_pos: int = 0, curr_rotor_i: int = 2) -> str:
        """ First set of letter substitutions from the input wheel to just before the reflector. """

        # Base case - when all rotors have been performed their ciphers
        if curr_rotor_i < 0:
            return letter

        # Find index of letter on input-side
        input_letter_i = ord(letter) - 65

        # calculate index of output letter
        curr_rotor_pos_i = self.rotors_used[curr_rotor_i].get_rotor_pos_i()

        output_letter_i = (input_letter_i + curr_rotor_pos_i - prev_rotor_pos) % 26
        output_letter = self.rotors_used[curr_rotor_i].get_output_letter(reg0_or_rev1=0, output_letter_i=output_letter_i)

        # recursive calls to go through each rotor
        return self.right_to_left_cipher(output_letter, curr_rotor_pos_i, curr_rotor_i - 1)

    def left_to_right_cipher(self, letter: str, prev_rotor_pos: int = 0, curr_rotor_i: int = 0) -> str:
        """ Second set of letter substitutions from the output of the reflector to the input wheel. """

        # Base case - when all rotors have been performed their ciphers
        # Now perform the cipher between right rotor and input wheel
        if curr_rotor_i > 2:
            # Find index of letter
            input_letter_i = ord(letter) - 65

            # calculate index of input letter
            letter_i = (input_letter_i - prev_rotor_pos) % 26
            letter = chr(letter_i + 65)

            return letter

        # Find index of letter
        input_letter_i = ord(letter) - 65

        # calculate index of input letter
        curr_rotor_pos = self.rotors_used[curr_rotor_i].get_rotor_pos_i()
        rev_output_i = (input_letter_i + curr_rotor_pos - prev_rotor_pos) % 26
        rev_output_letter = self.rotors_used[curr_rotor_i].get_output_letter(reg0_or_rev1=1, output_letter_i=rev_output_i)

        # recursive calls to go through each rotor
        return self.left_to_right_cipher(rev_output_letter, curr_rotor_pos, curr_rotor_i + 1)

    def encrypt_decrypt(self, input_text: str) -> str:
        """
        Perform encryption/decryption on the input_text.

        The "main" method in an Enigma object.
        """

        output_text = ""

        for letter in input_text:
            # advance rotor
            self.advance_rotors()

            # 1st plugboard substitution
            converted_letter = self.plugboard.plugboard_cipher(letter=letter)

            # 1st pass substitution through rotors
            converted_letter = self.right_to_left_cipher(converted_letter)

            # reflector substitution
            converted_letter = self.reflector.reflector_cipher(left_rotor_letter=converted_letter,
                                                               left_rotor_pos_i=self.rotors_used[0].get_rotor_pos_i())

            # 2nd pass substitution through rotors
            converted_letter = self.left_to_right_cipher(converted_letter)

            # 2nd plugboard substitution
            converted_letter = self.plugboard.plugboard_cipher(converted_letter)

            # add converted_letter to output_text
            output_text += converted_letter

        return output_text


##############################################################################
# Enigma setting checks
##############################################################################
def check_rotor_choices(rotor_choices: tuple) -> bool:
    """
    Check if rotor_choices are valid.

    :param rotor_choices: tuple[int]
    :return: bool
    """

    # if 3 rotors were not chosen, return False
    if len(rotor_choices) != 3:
        return False

    rotors_used = set()
    for rotor in rotor_choices:
        # if rotor is not an int, return False
        if not isinstance(rotor, int):
            return False

        # if rotor is not numbered 1-5, return False
        elif rotor < 1 or rotor > 5:
            return False

        # else if a rotor repeats, return False
        elif rotor in rotors_used:
            return False

        else:
            rotors_used.add(rotor)

    # if rotor_choices are all valid, return True
    return True


def check_plugboard_pairings(plugboard_pairings: list) -> bool:
    """
    Check if plugboard_pairings are valid.

    :param plugboard_pairings: list[str]
    :return: bool
    """

    plugboard_pairings_checker = {}
    for pairing in plugboard_pairings:
        # if pairing is not a str, return False
        if not isinstance(pairing, str):
            return False

        # if pairing letters are not a letter, return False
        elif pairing[0].isalpha() is False or pairing[1].isalpha() is False:
            return False

        # if both letters in the pairing are the same, return False
        elif pairing[0] == pairing[1]:
            return False

        # if either pairing letter has not been seen yet, add it to plugboard_pairings_checker,
        # otherwise, return False
        if pairing[0] not in plugboard_pairings_checker and pairing[1] not in plugboard_pairings_checker:
            plugboard_pairings_checker[pairing[0]] = pairing[1]
            plugboard_pairings_checker[pairing[1]] = pairing[0]
        else:
            return False

    # if plugboard_pairings are all valid, return True
    return True


def check_rotor_ring_settings(rotor_ring_settings: list) -> bool:
    """
    Check if rotor or ring settings are valid. Also convert them from an int
    to their corresponding ASCII letters if needed.

    :param rotor_ring_settings: list
    :return: bool
    """

    # if 3 rotor rings were not set, return False
    if len(rotor_ring_settings) != 3:
        return False

    # check each element to see if it is a valid element, and convert any int
    # to their ASCII letters
    for i in range(len(rotor_ring_settings)):
        rotor_ring_el = rotor_ring_settings[i]

        # if rotor_ring_el is a str, check if it's a letter
        # if not, return False
        if isinstance(rotor_ring_el, str) and len(rotor_ring_el) == 1:
            if not rotor_ring_el.isalpha():
                return False

        # else if rotor_ring_el is an int and between 1-26
        # convert it to a capital letter
        elif isinstance(rotor_ring_el, int) and 1 <= rotor_ring_el <= 26:
            rotor_ring_settings[i] = chr(rotor_ring_el + 64)  # take advantage of list mutability
        else:
            return False

    # at this point, nothing invalid found with rotor or ring settings, return True
    return True


def check_reflector(reflector: str) -> bool:
    """
    Check if reflector is valid.

    :param reflector: str
    :return: bool
    """

    # if exactly 1 reflector was not chosen, return False
    if len(reflector) != 1:
        return False

    # if reflector is not a str or is not a letter, return False
    if not isinstance(reflector, str) or reflector.isalpha() is False:
        return False

    # if reflect is not 'A', 'B', or 'C', return False
    if reflector.upper() not in ('A', 'B', 'C'):
        return False

    # if reflector is valid, return True
    return True


def sanitize_enigma_settings(rotor_choices: tuple, plugboard_pairings: list, initial_rotor_settings: list,
                             ring_settings: list, reflector: str) -> bool:
    """
    Check if Enigma settings are valid.

    :param rotor_choices: tuple
    :param plugboard_pairings: list
    :param initial_rotor_settings: list
    :param ring_settings: list
    :param reflector: str
    :return: bool
    """

    # check rotor_choices
    if not check_rotor_choices(rotor_choices):
        return False

    # check plugboard_pairings
    elif not check_plugboard_pairings(plugboard_pairings):
        return False

    # check initial_rotor_settings
    elif not check_rotor_ring_settings(initial_rotor_settings):
        return False

    # check ring_settings
    elif not check_rotor_ring_settings(ring_settings):
        return False

    # check reflector
    elif not check_reflector(reflector):
        return False

    # if no checks failed, then Enigma settings must be correct, return True
    return True


##############################################################################
# User input sanitization and check
##############################################################################
def sanitize_input_text(input_text: str) -> str or bool:
    """
    Check input_text for invalid characters and only output uppercase letters
    without any empty spaces.

    :return: str or bool
    """
    # if no input_text received, return False
    if input_text is None:
        return False

    # remove all spaces from input_str
    input_text = "".join(input_text.split())

    # if after removing all empty spaces, there is no message left, return False
    if len(input_text) == 0:
        return False

    sanitized_text = ""

    # check every character in input_text for any invalid characters
    for i in range(len(input_text)):
        letter = input_text[i]

        # if an incorrect character is found, return False
        if letter.isalpha() is False:
            return False

        # if not a bad character, capitalize it and add it to sanitized_text
        sanitized_text += letter.upper()

    # if no bad characters found, return sanitized_text
    return sanitized_text


# def cipher_print(input_str: str):
#     """
#     Print out the Enigma ciphertext in chunks of 5 letters
#     and 3 chunks per line.
#     """
#     output_line = ""
#
#     for i in range(len(input_str)):
#         curr_letter = input_str[i]
#
#         # print every 15 letters and clear the output_line for 15 more letters
#         if i > 0 and i % 15 == 0:
#             print(output_line)
#             output_line = ""
#
#         # add a space for every 5th letter
#         elif i > 0 and i % 5 == 0:
#             output_line += " "
#
#         output_line += curr_letter
#
#     print(output_line)


def enigma_run(rotor_choices: tuple, plugboard_pairings: list, initial_rotor_settings: list, ring_settings: list,
               reflector: str, input_str: str = None) -> str:
    """
    Main program function:

    1) Check if input string is valid
    2) Send input string to sanitize_input_text()
    3) Check if Enigma settings are valid
    4) Finalize formatting of Enigma settings
    5) Initialize an Enigma machine
    6) Perform encrypt_decrypt() on sanitized text
    7) Output the ciphertext
    """

    # check if input_str is valid, if it is invalid, return a message saying input is bad
    text = sanitize_input_text(input_str)

    if text is False:
        return "Bad input string. Letters only."

    # if Enigma settings are valid
    # if they are, initialize an enigma_machine
    if sanitize_enigma_settings(rotor_choices, plugboard_pairings, initial_rotor_settings,
                         ring_settings, reflector):

        # finalize formatting of Enigma settings
        for i in range(len(plugboard_pairings)):
            # uppercase each letter in plugboard_pairings
            plugboard_pairings[i] = plugboard_pairings[i].upper()

        # make lists as tuples
        plugboard_pairings = tuple(plugboard_pairings)
        initial_rotor_settings = tuple(initial_rotor_settings)
        ring_settings = tuple(ring_settings)

        # uppercase the reflector letter
        reflector = reflector.upper()

        # initialize an Enigma machine
        enigma_machine = Enigma(rotor_choices, plugboard_pairings, initial_rotor_settings,
                         ring_settings, reflector)

    # otherwise, we have bad Enigma settings
    else:
        return "Bad Enigma settings"

    # finally, run enigma_machine, return encrypted/decrypted text
    return enigma_machine.encrypt_decrypt(text)


if __name__ == '__main__':
    """ For running the program through an IDE """

    rotor_choices = (2, 4, 5)
    plugboard_pairings = ["AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"]
    initial_rotor_settings = ["B", "L", "A"]  # ordering is left-middle-right rotors
    ring_settings = ["B", "U", "L"]  # ordering is left-middle-right rotors
    reflector = 'B'

    user_input = sanitize_input_text(input("Enter a string of letters and spaces only: "))
    # user_input = "  "

    print(enigma_run(rotor_choices, plugboard_pairings, initial_rotor_settings,
                     ring_settings, reflector, user_input))
    input("...Press any key to end the program...")
