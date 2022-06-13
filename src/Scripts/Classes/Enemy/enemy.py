from dataclasses import dataclass
from typing import Any, List


@dataclass
class Enemy:
    name:str
    level:int
    atk:int
    _def:int
    weapon:Any
    armor:Any
    drop:List
    spell:Any