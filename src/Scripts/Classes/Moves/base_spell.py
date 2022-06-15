from dataclasses import dataclass

@dataclass
class Spell():
    name:str=None
    type:str=None
    knowledge:int=None
    mana:int=None
    atk:int=None
    deff:int=None
    health:int=None
    stamina:int=None