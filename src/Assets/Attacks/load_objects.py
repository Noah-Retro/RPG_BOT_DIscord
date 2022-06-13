import json

from RPG_BOT_VSA.DatenKlassen.Attacks.Attack import Attack
from RPG_BOT_VSA.DatenKlassen.Attacks.Spell import Spell
import os

dirname = os.path.dirname(__file__)
ATTACKS_PATH = dirname+"\Attacks.json"
SPELLS_PATH = dirname+"\Spells.json"

def load_attack(name:str):
    f = open(ATTACKS_PATH)
    data = json.load(f)
    a = Attack(_atk=data[name]["atk"],_stamina=data[name]["stamina"])
    return a

def load_spell(name:str):
    f = open(SPELLS_PATH)
    data = json.load(f)
    s = Spell(_mana=data[name]["mana"],
              _atk=data[name]["atk"],
              _def=data[name]["def"],
              _health=data[name]["health"],
              _stamina=data[name]["stamina"])
    return s
    