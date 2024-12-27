from constants import alphabet

class EnigmaMachine:

    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard
        self.saved_state = None
        self.previous_state = []

    def save_state(self):
        self.saved_state = {
            "rotors": [rotor.offset for rotor in self.rotors],
            "plugboard": self.plugboard.connections.copy(),
        }
        # self.previous_state.append(self.saved_state)

    def load_state(self):
        if self.saved_state:
            for rotor, offset in zip(self.rotors, self.saved_state["rotors"]):
                rotor.set_position(offset)
            self.plugboard.connections = self.saved_state["plugboard"].copy()

    def reset(self):
        for rotor in self.rotors:
            rotor.reset()
        self.plugboard.clear()

    def process_character(self, char):
        if char not in alphabet:
            return char
        char = self.plugboard.process(char)
        for rotor in reversed(self.rotors):
            char = rotor.forward(char)
        char = self.reflector.reflect(char)
        for rotor in self.rotors:
            char = rotor.backward(char)
        char = self.plugboard.process(char)
        rotate_next = True
        for rotor in reversed(self.rotors):
            if rotate_next:
                rotate_next = rotor.rotate()
            else:
                break
        return char

    def process_message(self, message):
        return ''.join(self.process_character(char) for char in message.upper())
    
    def get_settings(self):
        rotor_positions = [rotor.offset for rotor in self.rotors]
        plugboard_settings = self.plugboard.connections
        return f"rotor positions: {rotor_positions}, plugboard settings: {plugboard_settings}"