from dataclasses import dataclass
from random import random,choice
from typing import Any, Dict, List

from nextcord import Embed
import nextcord
from src.Scripts.Classes.Fight.fight import Fight
from src.Scripts.Classes.Activity.activity import Activity
from src.Scripts.Classes.HealthBar.healthbar import HelthBar
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Classes.Database.db import DB
from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader

@dataclass
class Base_Fireteam():
    '''
    Fireteam to be used in an battle 
    The bufs count for the entire fireteam
    '''
    players:List[Player]=None
    bufs:List[Any]=None
    base_level:int=0
    max_players:int=6
    fight:Fight=None
    activity:Activity=None

    def close(self):
        db = DB()
        for player in self.players:
            player.next_move=""
            db.store_player(player)

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
    
    def atack(self):
        drops=[]
        for p in self.players:
            if p.next_move=="":
                continue
            if p.next_move.split(":")[0] == "attack":
                if p.stamina - p.stamina_used <= 0:
                    p.next_move="Du hast zuwenig Stamina"
                    continue
                atackvalue=p.atk
                if p.weapon != None:
                    atackvalue += p.weapon.atk
                p.stamina_used += atackvalue
                e = self.fight.enemys[int(p.next_move.split(":")[2])]
                if e.name!=p.next_move.split(":")[1]:
                    p.next_move="Dein Ziel wurde schon getötet"
                    continue
                e.health -= atackvalue - e._def - (e.weapon["stat"])
                if e.health <=0:
                    items=self.generate_drops(e.drop)
                    if items!= []:
                        drops.append(*items)
                    print(*items)
                    self.fight.enemys.remove(e)
                print(f"Player {p.name} did attack and did {atackvalue} Damage to {e.name}")

        for player in self.players:
            for d in drops:
                player.add_item(d)

        if len(self.fight.enemys)==0:
            self.close()
            return True,True
        for e in self.fight.enemys:
            target=choice(self.players)
            atkval=e.atk + e.weapon["stat"] - target.deff -( target.armor.deff if target.armor else 0 )
            if atkval >0:
                target.damage += atkval         
            if target.health - target.damage <= 0:
                self.players.remove(target)
                db=DB()
                db.store_player(target)
            print(F"{e.name} hat {target.name} mit {(e.atk + e.weapon['stat'] - target.deff -( target.armor.deff if target.armor else 0 ))} angegrifen")
        if len(self.players)==0:
            self.close()
            return True,False
        return False,None

    def generate_drops(self,d:List):
        drops=[]
        for i in d:
            if random() < i["dropchance"]:
                al = Asset_Loader()
                print(i)
                drops.append(al.load_item(name=i["item"]))
            
        return drops