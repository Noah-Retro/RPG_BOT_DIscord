import dataclasses
from src.Scripts.Classes.Items.base_item import Base_Item

@dataclasses.dataclass
class Artefact(Base_Item):
    atk:int=0
    deff:int=0
    stamina:int=0
    mana:int=0