import dataclasses
from src.Scripts.Classes.Items.base_item import Base_Item

@dataclasses.dataclass
class Armor(Base_Item):
    deff:float=0