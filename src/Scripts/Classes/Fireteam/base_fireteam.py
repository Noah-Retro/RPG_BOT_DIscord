from dataclasses import dataclass
from typing import Any, List

from nextcord import Embed
import nextcord
from src.Scripts.Classes.Activity.activity import Activity
from src.Scripts.Classes.HealthBar.healthbar import HelthBar
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Classes.Database.db import DB

@dataclass
class Base_Fireteam():
    '''
    Fireteam to be used in an battle 
    The bufs count for the entire fireteam
    '''
    players:List[Any]=None
    bufs:List[Any]=None
    base_level:int=0
    max_players:int=6
    fight:Any=None
    activity:Activity=None


    @property
    def embed(self):
        if len(self.players) <= 0:
            return None
        e = Embed(title=self.players[0].name)
        e.description = "Hier siehst du alle Spieler"
        for i in self.players:
            e.add_field(name = i.name,value=f"""
                {HelthBar.healthbar(i.health-i.damage,i.health)} Helath
                {HelthBar.healthbar(i.mana-i.mana_used,i.mana)} Mana
                {HelthBar.healthbar(i.stamina-i.stamina_used,i.stamina)} Stamina
            """)      
        return e  

    def setup(self):
        '''
        gets the average level of all player

        return None
        '''
        level = 0
        i= 0
        for player in self.players:
            i+= 1
            level += player.level
        self.base_level = level /i

    @property
    def is_ready(self):
        '''
        controlles if all player have a action selected

        return Bool
        '''
        for i in self.players:
            i.next_move == None
            return False
        return True

    def turn_end(self):
        '''
        completes the turn for this fireteam
        '''
        pass

    def join(self,player:Player):
        for p in self.players:
            if p.name == player.name:
                return False
        if len(self.players) < self.max_players:
            self.players.append(player)
            return True
        return False

    def leave(self,player:str):
        for p in self.players:
            if p.name == player:
                self.players.remove(p)
    


