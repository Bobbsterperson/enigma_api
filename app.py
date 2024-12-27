from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from constants import *
from reflect import Reflector
from plug import Plugboard
from rot import Rotor
from enigma import EnigmaMachine

app = FastAPI()

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
    r1 = config.get("r1")
    r2 = config.get("r2")
    r3 = config.get("r3")
    plugboard = config.get("plugboard")
    plugboard_dict = {pair.split(':')[0]: pair.split(':')[1] for pair in plugboard.split(' / ')}
    plugboard_instance = Plugboard(plugboard_dict)
    rotor1 = Rotor(rot1, r1)
    rotor2 = Rotor(rot2, r2)
    rotor3 = Rotor(rot3, r3)
    reflector = Reflector(ref)
    enigma = EnigmaMachine([rotor1, rotor2, rotor3], reflector, plugboard_instance)
    encrypted_message = enigma.process_message(message)
    return templates.TemplateResponse("result.html", {"request": request, "encrypted_message": encrypted_message})
