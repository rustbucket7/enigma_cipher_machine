import unittest
from enigma import *

"""
Message Sources

Encrypted messages found here:
http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages

Decrypted messages found here:
http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Decrypts
"""


class TestEnigma(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     # based on German Enigma settings for April 7, 1940
    #     rotor_choices = (1, 2, 3)
    #     ring_setting = "WNM"
    #     plugboard_settings = ("HK", "CN", "IO", "FY", "JM", "LW")
    #     initial_rotor_settings = "RAO"
    #     reflector = 'B'
    #     cls.enigma1 = Enigma(rotor_choices, plugboard_settings,
    #                          initial_rotor_settings, ring_setting, reflector)
    #
    # @classmethod
    # def tearDownClass(cls) -> None:
    #     cls.enigma1 = None

    def test_msg_1_decrypt(self):
        """
        Enigma Instruction Manual, 1930

        This message is taken from a German army instruction manual for the
        Enigma I (interoperable with the later navy machine, Enigma M3).
        """
        rotor_choices = (2, 1, 3)
        plugboard_pairings = ["AM", "FI", "NV", "PS", "TU", "WZ"]
        initial_rotor_settings = ['A', 'B', 'L']
        ring_settings = [24, 13, 22]
        reflector = 'A'
        encrypted_msg = "GCDSEAHUGWTQGRKVLFGXUCALXVYMIGMMNMFDXTGNVHVRMMEVOUYFZSLRHDRRXFJWCFHUHMUNZEFRDISIKBGPMYVXUZ"
        decrypted_msg = "FEINDLIQEINFANTERIEKOLONNEBEOBAQTETXANFANGSUEDAUSGANGBAERWALDEXENDEDREIKMOSTWAERTSNEUSTADT"

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, encrypted_msg), decrypted_msg)

    def test_msg_2_decrypt(self):
        """
        Operation Barbarossa, 1941 Part 1

        Sent from the Russian front on 7th July 1941. The message is in two
        parts:
        """
        rotor_choices = (2, 4, 5)
        plugboard_pairings = ["AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"]
        initial_rotor_settings = ['B', 'L', 'A']
        ring_settings = [2, 21, 12]
        reflector = 'B'
        encrypted_msg = "EDPUDNRGYSZRCXNUYTPOMRMBOFKTBZREZKMLXLVEFGUEYSIOZVEQMIKUBPMMYLKLTTDEISMDICAGYKUACTCDOMOHWXMUUIAUBSTSLRNBZSZWNRFXWFYSSXJZVIJHIDISHPRKLKAYUPADTXQSPINQMATLPIFSVKDASCTACDPBOPVHJK"
        decrypted_msg = "AUFKLXABTEILUNGXVONXKURTINOWAXKURTINOWAXNORDWESTLXSEBEZXSEBEZXUAFFLIEGERSTRASZERIQTUNGXDUBROWKIXDUBROWKIXOPOTSCHKAXOPOTSCHKAXUMXEINSAQTDREINULLXUHRANGETRETENXANGRIFFXINFXRGTX"

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, encrypted_msg), decrypted_msg)

    def test_msg_3_decrypt(self):
        """
        Operation Barbarossa, 1941 Part 2

        Sent from the Russian front on 7th July 1941. The message is in two
        parts:
        """
        rotor_choices = (2, 4, 5)
        plugboard_pairings = ["AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"]
        initial_rotor_settings = ['L', 'S', 'D']
        ring_settings = [2, 21, 12]
        reflector = 'B'
        encrypted_msg = "SFBWDNJUSEGQOBHKRTAREEZMWKPPRBXOHDROEQGBBGTQVPGVKBVVGBIMHUSZYDAJQIROAXSSSNREHYGGRPISEZBOVMQIEMMZCYSGQDGRERVBILEKXYQIRGIRQNRDNVRXCYYTNJR"
        decrypted_msg = "DREIGEHTLANGSAMABERSIQERVORWAERTSXEINSSIEBENNULLSEQSXUHRXROEMXEINSXINFRGTXDREIXAUFFLIEGERSTRASZEMITANFANGXEINSSEQSXKMXKMXOSTWXKAMENECXK"

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, encrypted_msg), decrypted_msg)

    def test_msg_4_bad_input(self):
        """
        Bad input string (empty string)
        """
        rotor_choices = (2, 4, 5)
        plugboard_pairings = ["AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"]
        initial_rotor_settings = ['L', 'S', 'D']
        ring_settings = [2, 21, 12]
        reflector = 'B'
        input_str = ""
        error_msg = "Bad input string. Letters only."

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)

    def test_msg_4a_bad_input(self):
        """
        Bad input string (only empty spaces)
        """
        rotor_choices = (2, 4, 5)
        plugboard_pairings = ["AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"]
        initial_rotor_settings = ['L', 'S', 'D']
        ring_settings = [2, 21, 12]
        reflector = 'B'
        input_str = "   "
        error_msg = "Bad input string. Letters only."

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)

    def test_msg_4b_bad_input(self):
        """
        Bad input string (not strictly using letters)
        """
        rotor_choices = (2, 4, 5)
        plugboard_pairings = ["AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"]
        initial_rotor_settings = ['L', 'S', 'D']
        ring_settings = [2, 21, 12]
        reflector = 'B'
        input_str = "12A@#H"
        error_msg = "Bad input string. Letters only."

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)

    def test_msg_4c_bad_input(self):
        """
        Bad input string (not strictly using letters)
        """
        rotor_choices = (2, 4, 5)
        plugboard_pairings = ["AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"]
        initial_rotor_settings = ['L', 'S', 'D']
        ring_settings = [2, 21, 12]
        reflector = 'B'
        input_str = " A   2   ^^^"
        error_msg = "Bad input string. Letters only."

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)

    def test_msg_5_bad_settings(self):
        """
        Bad settings (missing rotor)
        """
        rotor_choices = (2, 1)
        plugboard_pairings = ["AM", "FI", "NV", "PS", "TU", "WZ"]
        initial_rotor_settings = ['A', 'B', 'L']
        ring_settings = [24, 13, 22]
        reflector = 'A'
        input_str = "aaa"
        error_msg = "Bad Enigma settings"

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)

    def test_msg_5a_bad_settings(self):
        """
        Bad settings (too many rotors)
        """
        rotor_choices = (2, 1, 3, 4)
        plugboard_pairings = ["AM", "FI", "NV", "PS", "TU", "WZ"]
        initial_rotor_settings = ['A', 'B', 'L']
        ring_settings = [24, 13, 22]
        reflector = 'A'
        input_str = "aaa"
        error_msg = "Bad Enigma settings"

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)

    def test_msg_6_bad_settings(self):
        """
        Bad settings (duplicate plugboard letter Z)
        """
        rotor_choices = (2, 1, 3)
        plugboard_pairings = ["AM", "FI", "NV", "PS", "TU", "WZ", "ZG"]
        initial_rotor_settings = ['A', 'B', 'L']
        ring_settings = [24, 13, 22]
        reflector = 'A'
        input_str = "aaa"
        error_msg = "Bad Enigma settings"

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)

    def test_msg_7_bad_settings(self):
        """
        Bad settings (missing initial rotor setting)
        """
        rotor_choices = (2, 1, 3)
        plugboard_pairings = ["AM", "FI", "NV", "PS", "TU", "WZ"]
        initial_rotor_settings = ['A', 'B']
        ring_settings = [24, 13, 22]
        reflector = 'A'
        input_str = "aaa"
        error_msg = "Bad Enigma settings"

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)

    def test_msg_7a_bad_settings(self):
        """
        Bad settings (too many initial rotor setting)
        """
        rotor_choices = (2, 1, 3)
        plugboard_pairings = ["AM", "FI", "NV", "PS", "TU", "WZ"]
        initial_rotor_settings = ['A', 'B', 'L', 'Z']
        ring_settings = [24, 13, 22]
        reflector = 'A'
        input_str = "aaa"
        error_msg = "Bad Enigma settings"

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)

    def test_msg_8_bad_settings(self):
        """
        Bad settings (missing ring setting)
        """
        rotor_choices = (2, 1, 3)
        plugboard_pairings = ["AM", "FI", "NV", "PS", "TU", "WZ"]
        initial_rotor_settings = ['A', 'B', 'L']
        ring_settings = [24, 13]
        reflector = 'A'
        input_str = "aaa"
        error_msg = "Bad Enigma settings"

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)

    def test_msg_8a_bad_settings(self):
        """
        Bad settings (too many ring setting)
        """
        rotor_choices = (2, 1, 3)
        plugboard_pairings = ["AM", "FI", "NV", "PS", "TU", "WZ"]
        initial_rotor_settings = ['A', 'B', 'L']
        ring_settings = [24, 13, 22, 20]
        reflector = 'A'
        input_str = "aaa"
        error_msg = "Bad Enigma settings"

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)

    def test_msg_9_bad_settings(self):
        """
        Bad settings (incorrect reflector choice)
        """
        rotor_choices = (2, 1, 3)
        plugboard_pairings = ["AM", "FI", "NV", "PS", "TU", "WZ"]
        initial_rotor_settings = ['A', 'B', 'L']
        ring_settings = [24, 13, 22]
        reflector = 'Z'
        input_str = "aaa"
        error_msg = "Bad Enigma settings"

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)

    def test_msg_9a_bad_settings(self):
        """
        Bad settings (another incorrect reflector choice)
        """
        rotor_choices = (2, 1, 3)
        plugboard_pairings = ["AM", "FI", "NV", "PS", "TU", "WZ"]
        initial_rotor_settings = ['A', 'B', 'L']
        ring_settings = [24, 13, 22]
        reflector = 'ZB'
        input_str = "aaa"
        error_msg = "Bad Enigma settings"

        self.assertEqual(enigma_run(rotor_choices, plugboard_pairings,
                                    initial_rotor_settings, ring_settings,
                                    reflector, input_str), error_msg)


if __name__ == '__main__':
    unittest.main()
