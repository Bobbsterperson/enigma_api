from project_files.constants import alphabet

class Rotor:
    def __init__(self, wiring, notch, ring_setting=0):
        self.alphabet = alphabet
        self.wiring = wiring
        self.notch = notch
        self.ring_setting = ring_setting
        self.offset = 0

    def rotate(self):
        self.offset = (self.offset + 1) % 26
        return self.alphabet[self.offset] == self.notch

    def reset(self):
        self.offset = 0

    def set_position(self, position):
        if 0 <= position < 26:
            self.offset = position
        else:
            raise ValueError("rotor position must be between 0 and 25")

    def forward(self, letter):
        index = (self.alphabet.index(letter) + self.offset - self.ring_setting) % 26
        encoded_letter = self.wiring[index]
        return self.alphabet[(self.alphabet.index(encoded_letter) - self.offset + self.ring_setting) % 26]

    def backward(self, letter):
        index = (self.alphabet.index(letter) + self.offset - self.ring_setting) % 26
        decoded_letter = self.alphabet[self.wiring.index(self.alphabet[index])]
        return self.alphabet[(self.alphabet.index(decoded_letter) - self.offset + self.ring_setting) % 26]