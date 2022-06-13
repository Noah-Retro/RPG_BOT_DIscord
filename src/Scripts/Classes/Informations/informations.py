import dataclasses
"""V1.0.0
Authors: Noah Schneider
Date: 13.12.21
Description: Descriptions of an character (None Game relavant)  
"""
@dataclasses.dataclass
class Informations():
    """Descriptions of an character (None Game relavant)
    """
    story:str=""
    looks:str=""
    img:str=""
    gender:str=""
    race:str=""
    p_class:str=""
    working:bool=False
    age:int=0
    height:float=0
    specials:str=""
    guild:str=""

    def work(self):
        self.working = True

    def pause(self):
        self.working = False
