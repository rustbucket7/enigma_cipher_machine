class Reflector:
    """
    Defines a class simulating the function of an Enigma reflector. The reflector acts like another rotor that takes
    in a letter as input from the left rotor and outputs the another letter back to the left rotor for another
    round of substitutions.
    """

    def __init__(self, settings_reflector: str):
        """ Set reflector variable to the desired reflector output pairings. """

        self.reflector_options = {
            'A': "EJMZALYXVBWFCRQUONTSPIKHGD",
            'B': "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            'C': "FVPJIAOYEDRZXWGCTKUQSBNMHL"
        }

        self.reflector_chosen = self.reflector_options[settings_reflector]

    def get_reflector_letter_at_i(self, i) -> str:
        """ Return the reflector letter at the desired index. """

        return self.reflector_chosen[i]

    def reflector_cipher(self, left_rotor_letter: str, left_rotor_pos_i: int) -> str:
        """ Perform substitution cipher of the output letter from the left rotor to the reflector. """

        input_letter_i = ord(left_rotor_letter) - 65
        reflector_letter_i = (input_letter_i - left_rotor_pos_i) % 26
        reflector_letter = self.get_reflector_letter_at_i(reflector_letter_i)

        return reflector_letter
