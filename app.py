from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from constants import *
from reflect import Reflector
from plug import Plugboard
from rot import Rotor
from enigma import EnigmaMachine

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class EnigmaConfig(BaseModel):
    message: str
    r1: int
    r2: int
    r3: int
    plugboard: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/action/", response_class=HTMLResponse)
async def action_page(request: Request):
    return templates.TemplateResponse("action.html", {"request": request})

@app.post("/encrypt/")
async def encrypt_message(config: EnigmaConfig):
    plugboard = Plugboard({pair.split(':')[0]: pair.split(':')[1] for pair in config.plugboard.split(' / ')})
    rotor1 = Rotor(rot1, config.r1)
    rotor2 = Rotor(rot2, config.r2)
    rotor3 = Rotor(rot3, config.r3)
    reflector = Reflector(ref)
    enigma = EnigmaMachine([rotor1, rotor2, rotor3], reflector, plugboard)
    encrypted_message = enigma.process_message(config.message)
    return {"encrypted_message": encrypted_message}

@app.get("/result/")
async def result_page(request: Request, encrypted_message: str):
    return templates.TemplateResponse("result.html", {"request": request, "encrypted_message": encrypted_message})

