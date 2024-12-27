from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from constants import ref, rot1, rot2, rot3, rot4, rot5
from reflect import Reflector
from plug import Plugboard
from rot import Rotor
from enigma import EnigmaMachine

app = FastAPI()

rotor_map = {
    "r1": rot1,
    "r2": rot2,
    "r3": rot3,
    "r4": rot4,
    "r5": rot5,
}
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/action/", response_class=HTMLResponse)
async def action_page(request: Request):
    return templates.TemplateResponse("action.html", {"request": request})

@app.post("/encrypt/", response_class=HTMLResponse)
async def encrypt_message(request: Request):
    form_data = await request.form()
    config_text = form_data.get('config')
    try:
        config = json.loads(config_text)
    except json.JSONDecodeError:
        return HTMLResponse("Invalid JSON format.", status_code=400)    
    message = config.get("message")
    plugboard = config.get("plugboard")
    rotor_keys = [key for key in config if key.startswith("r")]
    if len(rotor_keys) != 3:
        return HTMLResponse("Exactly three rotors must be specified.", status_code=400)
    try:
        selected_rotors = [
            Rotor(rotor_map[rotor_key], config[rotor_key]) for rotor_key in rotor_keys
        ]
    except KeyError:
        return HTMLResponse("Invalid rotor specified in configuration.", status_code=400)
    plugboard_dict = {pair.split(':')[0]: pair.split(':')[1] for pair in plugboard.split(' / ')}
    plugboard_instance = Plugboard(plugboard_dict)
    reflector = Reflector(ref)
    enigma = EnigmaMachine(selected_rotors, reflector, plugboard_instance)
    encrypted_message = enigma.process_message(message)
    return templates.TemplateResponse("result.html", {"request": request, "encrypted_message": encrypted_message})
