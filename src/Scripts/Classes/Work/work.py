
from dataclasses import dataclass
from typing import Any, List
from random import random

from src.Scripts.Classes.Activity.activity import Activity

@dataclass
class Work(Activity):
    name:str=""
    items:Any=None
    level:int=1
    starttime:float=0
    endtime:float=0

    def reward(self)->List:
        timeworked = self.endtime - self.starttime
        r = []
        for _ in range(int(timeworked)):
            for i in self.items:
                if i["drop_chance"] > random():
                    r.append(i["name"])
        return r