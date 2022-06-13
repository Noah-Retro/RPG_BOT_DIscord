
from dataclasses import dataclass


@dataclass
class Damage:
    source:str
    value:int
    spell:bool
    target:str=None
    pass