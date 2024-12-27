from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from enigma import EnigmaMachine
from constants import *
from plug import Plugboard
from rot import Rotor
from reflect import Reflector

app = FastAPI()

templates = Jinja2Templates(directory="templates")
plugboard = Plugboard({'A': 'B', 'C': 'D'})
rotor1 = Rotor(rot1, "Q")
rotor2 = Rotor(rot2, "E")
rotor3 = Rotor(rot3, "V")
reflector = Reflector(ref)
enigma = EnigmaMachine([rotor1, rotor2, rotor3], reflector, plugboard)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Render the main page with Enigma controls."""
    settings = enigma.get_settings()
    return templates.TemplateResponse("index.html", {"request": request, "settings": settings})

@app.post("/set_rotor_position/")
def set_rotor_position(rotor_id: str = Form(...), position: int = Form(...)):
    """Set rotor position."""
    if rotor_id == "r1":
        rotor1.set_position(position)
    elif rotor_id == "r2":
        rotor2.set_position(position)
    elif rotor_id == "r3":
        rotor3.set_position(position)
    enigma.save_state()
    return {"message": f"Rotor {rotor_id} set to position {position}"}

@app.post("/set_plugboard/")
def set_plugboard(letter1: str = Form(...), letter2: str = Form(...)):
    """Set plugboard connection."""
    plugboard.add_connection(letter1, letter2)
    enigma.save_state()
    return {"message": f"Plugboard connection added: {letter1.upper()} <-> {letter2.upper()}"}

@app.post("/encrypt/")
def encrypt_message(message: str = Form(...)):
    """Encrypt a message."""
    enigma.save_state()
    encrypted_message = enigma.process_message(message)
    return {"encrypted_message": encrypted_message}

@app.post("/decrypt/")
def decrypt_message(message: str = Form(...)):
    """Decrypt a message."""
    enigma.load_state()
    decrypted_message = enigma.process_message(message)
    return {"decrypted_message": decrypted_message}

@app.post("/reset/")
def reset_machine():
    """Reset Enigma machine."""
    enigma.reset()
    return {"message": "Enigma machine has been reset to default settings."}

@app.post("/save/")
def save_state():
    """Save Enigma machine state."""
    enigma.save_state()
    return {"message": "State saved."}

@app.post("/load/")
def load_state():
    """Load Enigma machine state."""
    enigma.load_state()
    return {"message": "State loaded."}
