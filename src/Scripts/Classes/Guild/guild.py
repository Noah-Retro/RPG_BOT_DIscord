from typing import List,Any
from dataclasses import dataclass
from src.Scripts.Classes.Events.event_manager import Event_Manager
from docs.conf import LEVEL_UP_EXP

import nextcord


@dataclass
class Guild:
    name:str
    players:List[str]
    leader:str
    exp:float
    emblem:str
    house:str
    voicechannel:str
    textchannel:str
    category:str
    level:int=1
    color:Any=0
    
    def add_exp(self,exp):
        self.nextlevel=LEVEL_UP_EXP**self.level*25
        self.exp += exp
        if self.exp >= self.nextlevel:
            self.level += 1
            self.exp=0
            self.nextlevel=LEVEL_UP_EXP**self.level*25
            Event_Manager.on_guild_level_up(self.name,self.level)

    def get_player_names_str(self)->str:
        s = ""
        for p in self.players:
            s+=p+","
        return s

    def get_player_names(self):
        for p in self.players:
            yield p

    def add_player(self,player_name:str)->bool:
        if player_name in self.players:
            return False
        self.players.append(player_name)  
        return True      

    def remove_player(self,player_name:str):
        if player_name in self.players:
            self.players.remove(player_name)

    @property
    def is_beautifyable(self)->bool:
        if " " in self.players:
            self.players.remove(" ")
        if len(self.players)>25:
            return False
        return True

    @property
    def embed(self)->nextcord.Embed:
        print(self)
        
        e = nextcord.Embed(title=self.name,color=int(self.color) if self.color != None else 0)
        e.set_thumbnail(url=self.emblem)
        e.set_image(url=self.house)
        e.add_field(name="Members",value=f"**Leader:** {self.leader}\n**Members:**\n {self.get_player_names_str()}")
        return e

    @property
    def voicechannel_id(self)->int:
        return int(self.voicechannel)

    @property
    def textchannel_id(self)->int:
        return int(self.textchannel)
    
    @property
    def category_id(self)->int:
        return int(self.category)
        