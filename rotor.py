class Rotor:
    """
    Defines a class simulating the function of an Enigma rotor. Takes in a letter as input and outputs another letter
    to fed into another rotor, the reflector, or the input wheel.
    """

    def __init__(self, rotor_chosen: int, starting_rotor_pos_letter: str, ring_setting_letter: str):
        """
        Set the starting positions of the Enigma rotors and determine which rotor outputs to use as well as their
        ring setting alteration based on user settings.
        """

        # rotor 1 to 5's output pairings organized as:
        # output (R-L), output (L-R, aka reverse output), turnover point
        self.rotor_options = {
            1: ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "UWYGADFPVZBECKMTHXSLRINQOJ", 'Q'],
            2: ["AJDKSIRUXBLHWTMCQGZNPYFVOE", "AJPCZWRLFBDKOTYUQGENHXMIVS", 'E'],
            3: ["BDFHJLCPRTXVZNYEIWGAKMUSQO", "TAGBPCSDQEUFVNZHYIXJWLRKOM", 'V'],
            4: ["ESOVPZJAYQUIRHXLNFTGKDCMWB", "HZWVARTNLGUPXQCEJMBSKDYOIF", 'J'],
            5: ["VZBRGITYUPSDNHLXAWMJQOFECK", "QCYLXWENFTZOSMVJUDKGIARPHB", 'Z']
        }

        # set the rotor to the appropriate starting position and select the rotor output strings
        self.curr_rotor_pos_letter = starting_rotor_pos_letter
        self.rotor_outputs = self.rotor_options[rotor_chosen]

        # rewire both output and reverse output of the rotor based on ring setting letter
        for i in range(2):
            self.rotor_outputs[i] = self.ring_setting_rewiring(rotor_output_str=self.rotor_outputs[i],
                                                               ring_letter=ring_setting_letter)

    def ring_setting_rewiring(self, rotor_output_str: str, ring_letter: str) -> str:
        """ Alters a rotor's output pairings based on desired ring setting letter. """

        ring_letter_i = ord(ring_letter) - 65
        dot_position = (rotor_output_str.index("A") + ring_letter_i) % 26
        shifted_str = ""

        # shift up each letter in rotor_output_str
        for i in range(len(rotor_output_str)):
            letter_i = ord(rotor_output_str[i]) - 65
            shifted_str += chr(((letter_i + ring_letter_i) % 26) + 65)

        # rotate letters in shifted rotor_output_str until ring_letter is in the index position of dot_position
        rotated_str = shifted_str
        while rotated_str[dot_position] != ring_letter:
            last_letter = rotated_str[-1]
            all_other_letters = rotated_str[:len(rotated_str) - 1]
            rotated_str = last_letter + all_other_letters

        return rotated_str

    def get_output_letter(self, reg0_or_rev1: int, output_letter_i: int) -> str:
        """ Outputs a letter, from the regular or reserve output strings, at the desired index. """
        reg_or_rev = self.rotor_outputs[reg0_or_rev1]  # 0 is regular output, 1 is reverse output

        return reg_or_rev[output_letter_i]

    def get_rotor_pos_i(self) -> int:
        """ Output the rotor's current letter position by its ordinal value (ex. 'A' is 0, 'Z' is 25). """
        return ord(self.curr_rotor_pos_letter) - 65

    def check_to_step_adjacent_rotor(self) -> bool:
        """
        Returns a bool value based on whether stepping up the rotor will cause the adjacent rotor to step up as well
        using the rotor's "turnover point".
        """
        return self.curr_rotor_pos_letter == self.rotor_outputs[2]

    def step_rotor(self):
        """ Turn the rotor forward 1 step/position. """
        curr_rotor_pos_i = (self.get_rotor_pos_i() + 1) % 26
        self.curr_rotor_pos_letter = chr(curr_rotor_pos_i + 65)
