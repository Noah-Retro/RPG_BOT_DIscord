import dataclasses
import json
from typing import overload


    
@dataclasses.dataclass
class Base_Item():
    name:str
    value:float  
    description:str
    img:str=None
    quantity:int=1

    def remove_quantity(self,quantity:int):
        """Removes an item if quantity is less than 0 it does not remove it and returns False

        Args:
            quantity (int): [description]

        Returns:
            [bool]: if item was removed and quantity is >= 0 True
        """
        self.quantity -= quantity
        if self.quantity >= 0:
            return True
        if self.quantity < 0:
            self.quantity += quantity
            return False

    def add_quantity(self,quantity:int):
        self.quantity += quantity
        return True


    @overload
    def __eq__(self, __o: object) -> bool:
        return self.name == __o.name

    def __eq__(self,__o:str)->bool:
        return self.name == __o
            