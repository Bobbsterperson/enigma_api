from constants import alphabet

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring
        self.alphabet = alphabet

    def reflect(self, letter):
        index = self.alphabet.index(letter)
        return self.wiring[index]