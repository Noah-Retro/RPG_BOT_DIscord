from dataclasses import dataclass
from typing import List

from src.Scripts.Classes.Activity.activity import Activity

@dataclass
class Fight(Activity):
    enemys:List=None
    exp:int=0