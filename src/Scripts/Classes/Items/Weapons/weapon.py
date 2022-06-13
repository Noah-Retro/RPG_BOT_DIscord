from dataclasses import dataclass
from src.Scripts.Classes.Items.base_item import Base_Item

@dataclass
class Weapon(Base_Item):
    atk:float=0
    