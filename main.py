"""
For running enigma.py through an IDE
"""

from enigma import *

if __name__ == '__main__':
    rotor_choices = (2, 4, 5)
    plugboard_pairings = ["AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"]
    initial_rotor_settings = ['B', 'L', 'A']  # ordering is left-middle-right rotors
    ring_settings = ['B', 'U', 'L']  # ordering is left-middle-right rotors
    reflector = 'B'

    user_input = input("Enter a string of letters and spaces only: ")
    # user_input = "  "

    output_text = enigma_run(rotor_choices, plugboard_pairings, initial_rotor_settings, ring_settings, reflector, user_input)
    print(output_text)
    input("...Press any key to end the program...")
