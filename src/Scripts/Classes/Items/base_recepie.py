import dataclasses
from typing import Any, List
from src.Scripts.Classes.Items.base_item import Base_Item

@dataclasses.dataclass
class Base_Recepie():
    item:Any=None
    items:List[Any]=None
    skill:int=0