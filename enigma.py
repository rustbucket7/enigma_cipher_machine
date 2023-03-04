# from sys import exit


class Enigma:
    """
    Defines a class simulating the functionality of the German Enigma I and M3
    cipher machines used by the German Army and Air Force during WW2.

    Uses rotors 1-5 and reflectors A-C.
    """

    def __init__(self,
                 settings_rotor_choices: tuple,
                 settings_plugboard_pairings: tuple,
                 settings_starting_rotor_pos: tuple,
                 settings_ring: tuple,
                 settings_reflector: str):
        """ Define initial variable values of an Enigma object. """

        # grab initial settings when an Enigma object is initialized
        self.rotor_order = settings_rotor_choices  # tuple(1,2,3)
        self.settings_plugboard_pairings = settings_plugboard_pairings  # tuple(ab, cd, ...)
        self.starting_rotor_pos = settings_starting_rotor_pos  # XXX
        self.settings_ring = settings_ring  # XXX
        self.settings_reflector = settings_reflector  # X

        # input-output letter pairings for each rotor and the reflector
        self.rotor_reflector_wheel = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # rotor 1 to 5's output pairings organized as:
        # output (R-L), output (L-R, aka reverse output), turnover point
        self.rotor_options = [
            ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "UWYGADFPVZBECKMTHXSLRINQOJ", "Q"],
            ["AJDKSIRUXBLHWTMCQGZNPYFVOE", "AJPCZWRLFBDKOTYUQGENHXMIVS", "E"],
            ["BDFHJLCPRTXVZNYEIWGAKMUSQO", "TAGBPCSDQEUFVNZHYIXJWLRKOM", "V"],
            ["ESOVPZJAYQUIRHXLNFTGKDCMWB", "HZWVARTNLGUPXQCEJMBSKDYOIF", "J"],
            ["VZBRGITYUPSDNHLXAWMJQOFECK", "QCYLXWENFTZOSMVJUDKGIARPHB", "Z"]
        ]

        # reflectors A to C's output pairings
        self.reflector_options = {
            'A': "EJMZALYXVBWFCRQUONTSPIKHGD",
            'B': "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            'C': "FVPJIAOYEDRZXWGCTKUQSBNMHL"
        }

        # set rotors to default starting position from left to right (0 = A)
        # i.e. [left_rotor, middle_rotor, right_rotor]
        self.rotor_pos = [0, 0, 0]

        # setup plugboard and reflector based on initialized settings
        self.plugboard = self.set_plugboard()  # ex. {"EA": "GM", "GM":"EA"}
        self.reflector = self.set_reflector(self.settings_reflector)  # ex. "B"
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
    def set_plugboard(self) -> dict:
        """ Set plugboard based on received settings. """
        plugboard_final_settings = dict()

        for letter_pair in self.settings_plugboard_pairings:
            first_letter = letter_pair[0]
            second_letter = letter_pair[1]
            plugboard_final_settings[first_letter] = second_letter
            plugboard_final_settings[second_letter] = first_letter

        return plugboard_final_settings

    def set_reflector(self, reflector_to_use: str) -> str:
        """
        Set reflector variable to the desired reflector output pairings.
        """
        return self.reflector_options[reflector_to_use]

    def set_rotors(self) -> list:
        """
        Set the starting positions of the Enigma rotors and determine
        which rotor outputs to use as well as their ring setting alteration
        based on user settings.
        """
        rotor_outputs_to_use = []

        # set rotor starting positions
        for i in range(3):
            rotor_pos = self.starting_rotor_pos[i]
            starting_pos_i = self.rotor_reflector_wheel.index(rotor_pos)
            self.rotor_pos[i] = starting_pos_i

        # add required rotor output info to rotor_outputs_to_use[] based on
        # user-specified rotor_order
        for i in range(len(self.rotor_order)):
            curr_rotor = self.rotor_options[self.rotor_order[i] - 1].copy()
            curr_ring_setting = self.settings_ring[i]
            for j in range(2):
                curr_rotor[j] = self.ring_setting_rewiring(curr_rotor[j],
                                                           curr_ring_setting)

            rotor_outputs_to_use.append(curr_rotor)

        return rotor_outputs_to_use

    def ring_setting_rewiring(self, rotor_output_str: str, ring_letter: str):
        """
        Alters a rotor's output pairings based on desired ring setting letter.
        """
        ring_letter_i = self.rotor_reflector_wheel.index(ring_letter)
        dot_position = (rotor_output_str.index("A") + ring_letter_i) % 26
        shifted_str = ""

        # shift up each letters in rotor_output_str
        for i in range(len(rotor_output_str)):
            letter_i = self.rotor_reflector_wheel.index(rotor_output_str[i])
            shifted_str += self.rotor_reflector_wheel[(letter_i +
                                                       ring_letter_i) % 26]

        # rotate letters in shifted rotor_output_str until ring_letter is in
        # the index position of dot_position
        rotated_str = shifted_str
        while rotated_str[dot_position] != ring_letter:
            last_letter = rotated_str[len(rotated_str) - 1]
            all_other_letters = rotated_str[:len(rotated_str) - 1]
            rotated_str = last_letter + all_other_letters

        return rotated_str

    def advance_rotors(self):
        """
        Check if more than 1 rotor needs to move.
        Then move right rotor forward 1 step.
        """
        middle_rotor_step = False
        left_rotor_step = False

        # check if right rotor letter will cause middle rotor to turn
        rotor_letter = self.rotor_reflector_wheel[self.rotor_pos[2]]
        if rotor_letter in self.rotors_used[2][2]:
            middle_rotor_step = True

        # check if middle rotor letter will cause left rotor to turn
        # also determines when the middle rotor will turn on its own
        rotor_letter = self.rotor_reflector_wheel[self.rotor_pos[1]]
        if rotor_letter in self.rotors_used[1][2]:
            middle_rotor_step = True
            left_rotor_step = True

        # check if left rotor letter will cause it to turn itself
        rotor_letter = self.rotor_reflector_wheel[self.rotor_pos[0]]
        if rotor_letter in self.rotors_used[0][2]:
            left_rotor_step = True

        # step right rotor (always occurs)
        self.rotor_pos[2] = (self.rotor_pos[2] + 1) % 26

        # step the middle rotor if possible
        if middle_rotor_step is True:
            self.rotor_pos[1] = (self.rotor_pos[1] + 1) % 26

        # step the left rotor if possible
        if left_rotor_step is True:
            self.rotor_pos[0] = (self.rotor_pos[0] + 1) % 26

    def plugboard_cipher(self, letter: str) -> str:
        """
        Perform substitution cipher of a letter going through the plugboard.

        If a letter was not assigned a cipher pair, return itself.
        """
        try:
            return self.plugboard[letter]
        except KeyError:
            return letter

    def right_to_left_cipher(self,
                             letter: str,
                             prev_rotor_pos: int = 0,
                             curr_rotor_i: int = 2):
        """
        First set of letter substitutions from the input wheel to just before
        the reflector.
        """
        # Base case - when all rotors have been performed their ciphers
        if curr_rotor_i < 0:
            return letter

        # Find index of letter on input-side
        input_letter_i = self.rotor_reflector_wheel.index(letter)

        # calculate index of output letter
        curr_rotor_pos_i = self.rotor_pos[curr_rotor_i]

        output_letter_i = (input_letter_i +
                           curr_rotor_pos_i -
                           prev_rotor_pos) % 26
        output_letter = self.rotors_used[curr_rotor_i][0][output_letter_i]

        # recursive calls to go through each rotor
        return self.right_to_left_cipher(output_letter, curr_rotor_pos_i,
                                         curr_rotor_i - 1)

    def reflector_cipher(self, letter: str):
        """
        Perform substitution cipher of the output letter from the left rotor
        to the reflector.
        """
        input_letter_i = self.rotor_reflector_wheel.index(letter)
        prev_rotor_ptr = self.rotor_pos[0]  # only need to know left rotor pos
        reflector_letter_i = (input_letter_i - prev_rotor_ptr) % 26
        reflector_letter = self.reflector[reflector_letter_i]

        return reflector_letter

    def left_to_right_cipher(self,
                             letter: str,
                             prev_rotor_pos: int = 0,
                             curr_rotor_i: int = 0):
        """
        Second set of letter substitutions from the output of the reflector
        to the input wheel.
        """
        # Base case - when all rotors have been performed their ciphers
        # Now perform the cipher between right rotor and input wheel
        if curr_rotor_i > 2:
            # Find index of letter
            input_letter_i = self.rotor_reflector_wheel.index(letter)

            # calculate index of input letter
            letter_i = (input_letter_i - prev_rotor_pos) % 26
            letter = self.rotor_reflector_wheel[letter_i]

            return letter

        # Find index of letter
        input_letter_i = self.rotor_reflector_wheel.index(letter)

        # calculate index of input letter
        curr_rotor_pos = self.rotor_pos[curr_rotor_i]
        rev_output_i = (input_letter_i +
                        curr_rotor_pos -
                        prev_rotor_pos) % 26
        rev_output_letter = self.rotors_used[curr_rotor_i][1][rev_output_i]

        # recursive calls to go through each rotor
        return self.left_to_right_cipher(rev_output_letter, curr_rotor_pos,
                                         curr_rotor_i + 1)

    def encrypt_decrypt(self, input_text: str) -> str:
        """
        Perform encryption/decryption on the input_text.

        The "main" method in an Enigma object.
        """

        output_text = ""

        for letter in input_text:
            # advance rotor
            self.advance_rotors()
            # print("rotors advanced to:", self.rotor_pos)  # testing...

            # 1st plugboard substitution
            converted_letter = self.plugboard_cipher(letter)

            # 1st pass substitution through rotors
            converted_letter = self.right_to_left_cipher(converted_letter)

            # reflector substitution
            converted_letter = self.reflector_cipher(converted_letter)

            # 2nd pass substitution through rotors
            converted_letter = self.left_to_right_cipher(converted_letter)

            # 2nd plugboard substitution
            converted_letter = self.plugboard_cipher(converted_letter)
            # print()  # testing...

            # add converted_letter to output_text
            output_text += converted_letter

        return output_text


##############################################################################
# Enigma setting checks
##############################################################################
def check_rotor_choices(rotor_choices: tuple):
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


def check_plugboard_pairings(plugboard_pairings: list):
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


def check_rotor_ring_settings(rotor_ring_settings: list):
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

    # at this point, nothing invalid found with rotor or ring settings,
    # return True
    return True


def check_reflector(reflector: str):
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


def sanitize_enigma_settings(rotor_choices: tuple,
                             plugboard_pairings: list,
                             initial_rotor_settings: list,
                             ring_settings: list,
                             reflector: str):
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
def sanitize_input_text(input_text: str):
    """
    Check input_text for invalid characters and only output uppercase letters
    without any empty spaces.

    :return: str
    """
    sanitized_text = ""

    for i in range(len(input_text)):
        letter = input_text[i]

        # if an incorrect character is found, display an error message
        # and exit the program
        if not letter.isalpha() and letter != " ":
            error_str = "Invalid character: " + letter + ', ' + \
                     "Found at index: " + str(i)
            exit(error_str)

        # or if an empty space is found, skip it
        elif letter == " ":
            continue

        # if not a bad letter, add letter to sanitized_text
        sanitized_text += letter.upper()

    # otherwise, if no bad inputs found, return sanitized_text
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


def enigma_run(rotor_choices: tuple,
               plugboard_pairings: list,
               initial_rotor_settings: list,
               ring_settings: list,
               reflector: str,
               input_str: str = None):
    """
    Main program function:

    1) Check if Enigma settings are valid
    2) Finalize formatting of Enigma settings
    3) Check if an input string was received
    4) Send input string to sanitize_input_text()
    5) Perform encrypt_decrypt() on sanitized text
    6) Output the ciphertext
    """

    # if Enigma settings are valid, ask user for input text
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

        # if input_str was invalid, return string saying so
        if input_str is None or input_str.isalpha() is False:
            return "Bad input string. Letters only."

        # otherwise, ready input_str to feed into enigma_machine
        else:
            text = sanitize_input_text(input_str)

        # run enigma_machine, return encrypted/decrypted text
        return enigma_machine.encrypt_decrypt(text)

    else:
        return "Bad Enigma settings"


if __name__ == '__main__':
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
