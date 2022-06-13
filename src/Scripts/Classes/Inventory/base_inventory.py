from typing import List
import dataclasses
from src.Scripts.Classes.Items.base_item import Base_Item
from src.Scripts.Classes.Trade.trade import Trade
from src.Scripts.Classes.Bounty.bounty import Bounty
"""
V1.0.0
Authors: Noah Schneider
Date: 13.12.21
Description: Base Inventory for all characters, markets, etc.    
"""
@dataclasses.dataclass
class Base_Inventory:
    items:List[Base_Item]=None
    trades:List[Trade]=None
    bountys:List[Bounty]=None
    money:float=0
    

    def sub_money(self,amount)->bool:
        if self.money - amount >= 0:
            self.money -= amount
            return True
        return False

    def add_money(self,amount)->bool:
        self.money += amount
        return True

    def add_bounty(self,bounty:Bounty):
        if self.bountys == None:
            self.bountys = [bounty]
            return True
        if len(self.bountys)>=25:
            return False
        for b in self.bountys:
            if b.name == bounty.name:
                return False
        self.bountys.append(bounty)



    def remove_bounty(self,bounty:Bounty):
        self.bountys.remove(bounty)

    def remove_item(self,item_name,quantity):
        for i in self.items:
            if i.name == item_name:
                if i.remove_quantity(quantity):
                    if i.quantity <= 0:
                        self.items.remove(i)
                    return True
        return False

    def add_item(self,item:Base_Item):
        if self.bountys != None:
            for b in self.bountys:
                b.got_item(item.name,item.quantity)
        
        if self.items==None:
            self.items=[item]
            return True
        for i in self.items:
            if i.name == item.name:
                i.add_quantity(item.quantity)
                return True
        if len(self.items)>24:
            return False
        self.items.append(item)
        return True

    