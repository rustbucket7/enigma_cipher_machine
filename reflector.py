class Reflector:
    """

    """

    def __init__(self, settings_reflector: str):
        """
        Set reflector variable to the desired reflector output pairings.
        """
        self.reflector_options = {
            'A': "EJMZALYXVBWFCRQUONTSPIKHGD",
            'B': "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            'C': "FVPJIAOYEDRZXWGCTKUQSBNMHL"
        }

        self.reflector_chosen = self.reflector_options[settings_reflector]

    def get_reflector_i(self, i):
        """

        """
        return self.reflector_chosen[i]
