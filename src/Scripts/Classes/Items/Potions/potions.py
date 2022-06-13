from dataclasses import dataclass
from src.Scripts.Classes.Items.base_item import Base_Item

@dataclass
class Potion(Base_Item):
    health:float=0
    mana:float=0
    stamina:float=0
    