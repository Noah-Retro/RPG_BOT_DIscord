from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Suggsestion:
    type_:str
    player:str
    data:str
    payed:bool=False
