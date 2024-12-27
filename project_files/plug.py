class Plugboard:
    def __init__(self, connections=None):
        self.connections = {}
        if connections:
            for k, v in connections.items():
                self.add_connection(k, v)
        else:
            self.clear()

    def add_connection(self, letter1, letter2):
        if letter1 != letter2:
            self.connections[letter1.upper()] = letter2.upper()
            self.connections[letter2.upper()] = letter1.upper()

    def clear(self):
        self.connections = {}

    def process(self, letter):
        return self.connections.get(letter.upper(), letter.upper())