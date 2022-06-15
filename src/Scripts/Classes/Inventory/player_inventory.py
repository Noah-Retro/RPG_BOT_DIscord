import dataclasses
from random import random
from typing import Any, List
from src.Scripts.Classes.Moves.base_spell import Spell

from src.Scripts.Classes.Bounty.bounty import Bounty
from src.Scripts.Classes.Inventory.base_inventory import Base_Inventory
from src.Scripts.Classes.Items.Armors.armor import Armor
from src.Scripts.Classes.Items.Artefacts.artefact import Artefact
from src.Scripts.Classes.Items.base_recepie import Base_Recepie
from src.Scripts.Classes.Items.Weapons.weapon import Weapon
from src.Scripts.Classes.Trade.trade import Trade

"""
V1.0.0
Authors: Noah Schneider
Date: 13.12.21
Description: DB Class to load and store player objekts    
"""

@dataclasses.dataclass
class Player_Inventory(Base_Inventory):  
    weapon:Any=None
    armor:Any=None
    artefact:Artefact=None
    spells:List[Spell]=None

    def craft_item(self,recepie:Base_Recepie):
        '''
        craft_item(recepie:Base_Recepie->Bool

        craft an item with the given recepie if succesfull -> true else false
        subtracts material needed

        return Bool
        '''
        found = False
        for i in recepie.items:
            for ii in self.items:
                if i.name == ii.name and i.quantity > ii.quantity:
                    return False
                if i.name == ii.name:
                    found = True
        if not found:
            return False
        for i in recepie.items:
            self.remove_item(i.name,i.quantity)
        self.add_item(recepie.item)
        return True


    def equip_weapon(self,item:Weapon):
        if self.weapon != None:
            self.unequip_weapon()
        if isinstance(item,Weapon) or issubclass(type(item),Weapon):
            self.weapon = item
            if self.remove_item(item.name,1):
                return True
        return False
    
    def unequip_weapon(self)-> Weapon:
        w = self.weapon
        self.weapon = None
        self.add_item(w)

    def equip_armor(self,item:Armor):
        if self.armor != None:
            self.unequip_armor()
        if isinstance(item,Armor) or issubclass(type(item),Armor):
            self.armor = item
            if self.remove_item(item.name,1):
                return True
        return False

    def unequip_armor(self)->bool:
        a = self.armor
        self.armor=None
        self.add_item(a) 
        return True

    def equip_artefact(self,artefact:Artefact):
        if self.artefact != None:
            self.unequip_artefact()
        if isinstance(artefact,Artefact) or issubclass(type(artefact),Artefact):
            artefact.quantity = 1
            self.remove_item(artefact.name,1)
            self.artefact = artefact
            return True

    def unequip_artefact(self):
        a = self.artefact
        a.quantity = 1
        self.artefact = None
        self.add_item(a)
        return True

    def open_trade(self,trade:Trade)->bool:
        if self.trades == None:
            self.trades=[]
        if self.remove_item(trade.item.name,trade.item.quantity):
            self.trades.append(trade)
            return True
        return False
        
    def remove_bounty(self,bounty:Bounty):
        for b in self.bountys:
            if b.name == bounty.name:
                self.bountys.remove(b)
    
    def remove_trade(self,trade:Trade):
        self.add_item(trade.item)
        self.trades.remove(trade)

    def complete_bounty(self,p):
        for b in self.bountys:
            if b.is_completed:
                for i in b.reward_items:
                    self.add_item(i)
                self.add_money(b.reward_money)
                p.add_exp(b.exp)
                return True

        