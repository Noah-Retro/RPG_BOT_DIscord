import dataclasses
import time
from typing import Any, List
import nextcord
from src.Scripts.Classes.Damagable.damagable import Damagable
from src.Scripts.Classes.Events.event_manager import Event_Manager
from src.Scripts.Classes.Informations.informations import Informations
from src.Scripts.Classes.Inventory.player_inventory import Player_Inventory
from src.Scripts.Classes.Items.base_item import Base_Item
from src.Scripts.Classes.Items.base_recepie import Base_Recepie
from src.Scripts.Classes.Items.Potions.potions import Potion
from src.Scripts.Classes.Stats.player_stat import Stat
from src.Scripts.Classes.Work.work import Work


@dataclasses.dataclass
class Player(Informations,Player_Inventory,Stat,Damagable):
    name:str=""
    character_name:str=""
    id:int=0
    color:nextcord.Color=None
    work:Work=None
    mana_used:int=0
    stamina_used:int=0
    fireteam:Any=None
    moves:List[Any]=None
    next_move:Any=None
    poststelle:List[Base_Item]=None
    
    def craft_item(self, recepie: Base_Recepie):
        if self.craft < recepie.skill:
            return False
        return super().craft_item(recepie)

    def add_exp(self, amount):
        if self.guild != None and self.guild != "":
            Event_Manager.on_exp_gain(self.guild,amount)
        return super().add_exp(amount)

    def add_item(self, item: Base_Item):
        if super().add_item(item):
            return
        if self.poststelle == None:
            self.poststelle = [item]
            return
        for i in self.poststelle:
            if i.name == item.name:
                i.quantity += item.quantity
                return
        self.poststelle.append(item)

    def attack(self,level,buff):
        '''
        returns the atk value of the atk chosen
        '''
        pass

    def spell(self,spell):
        '''
        returns the buff of an spell or atk
        '''
        pass
        

    def heal(self,item:Potion):
        if not self.remove_item(item.name,1):
            return False
        if item.mana <1:
            self.mana_used -= self.mana * item.mana
        else:
            self.mana_used -= item.mana
        if item.stamina <1:
            self.stamina_used -= self.stamina * item.stamina
        else:
            self.stamina_used -= item.stamina
        if item.health<1:
            self.damage -= self.health*item.health
        else:
            self.damage -= item.health
        if self.damage < 0:
            self.damage = 0
        if self.mana_used <0:
            self.mana_used = 0
        if self.stamina_used<0:
            self.stamina_used=0
        return True

    def start_work(self,work:Work):
        if self.working:
            return
        self.working = True
        self.work=work
        self.work.starttime = time.time()/60

    def stop_work(self):
        self.work.endtime = time.time()/60
        rew=self.work.reward()
        from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader
        al = Asset_Loader()
        for i in rew:
            self.add_item(al.load_item(i,1))
        self.working = False
        self.work = None
        return rew

    def add_stats(self,**kwargs):
        for key in kwargs:
            self.__setattr__(key,kwargs[key])
