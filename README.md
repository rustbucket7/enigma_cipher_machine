﻿# Enigma Cipher Machine
This project is a Python 3 implementation of the Enigma 1/M3 cipher machine used by the German Army and Air Force to encrypt/decrypt their communication to various parts of Europe before and during World War 2.

## Description
This implementation of Enigma makes use of rotors 1 to 5 and reflectors A, B, and C.

The application will encrypt a user's message by performing multiple substitution ciphers through the Enigma machine's various components: a plugboard, three moving rotors, and a reflector. At each component, an input letter will be changed to some other letter which the next component will then use as its input. A letter typed by the user will never be returned as itself after going through the entire encrypting/decrypting process.

The encrypt/decrypt process looks like this:
- User types a message ->
- message will be changed once at the plugboard ->
- changed message will be changed once at each of the three rotors (three changes)->
- another change will be made at the reflector ->
- the message will be changed once more through the three rotors (three changes) ->
- one last change at the plugboard again ->
- output
- DONE

Altogether, each letter in the input message can be changed up to 9 times.

## How to Use (TO BE CHANGED)
To encrypt a message:
- Setup Enigma machine
- Run the program
- Type in your message
- Press Enter
- Copy the output

To decrypt a message:
- Setup Enigma machine to the same settings as you did for encryption
- Run the program
- Type in your encrypted message
- Press Enter
- Copy the output

Setting up the Enigma machine:
1. Open the enigma.py file in an IDE or text editor
2. Scroll down to the bottom of the file where `if __name__ == '__main__':` is found
3. Change the following settings to suit your encryption/decryption needs:
- rotor_choices: the order of your rotors from left to right. Requires three rotors to be used. Ex. [2, 1, 3].
- plugboard: the pairs of letters that will get swapped at the plugboard. Ex. ["GZ", "YQ", "OP", "LA"].
- initial_rotor_settings: sets the starting position of each rotor. Ex. "RAO".
- ring_settings: sets the desired ciphering for each rotor. Ex. "BMX".
- reflector: choose which reflector to use. Ex. "A".
4. Run the program using Python 3 to begin encrypting/decrypting a message

## Helpful Links
[How the Enigma Works](https://www.youtube.com/watch?v=ybkkiGtJmkM)

[Enigma 1 article](https://cryptomuseum.com/crypto/enigma/i/index.htm)

[Paper Enigma](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/paperEnigma.pdf)

[Neat Enigma emulator and messages](https://www.101computing.net/enigma/)

[Another great Enigma emulator that traces a letter's changes](https://people.physik.hu-berlin.de/~palloks/js/enigma/enigma-u_v26_en.html)

[Sample Messages](http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages)

[Decrypts of Sample Messages](http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Decrypts)
