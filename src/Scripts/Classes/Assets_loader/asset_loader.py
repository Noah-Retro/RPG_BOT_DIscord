import glob
import json
import os

from src.Scripts.Classes.Fight.fight import Fight
from src.Scripts.Classes.Bounty.bounty import Bounty
from src.Scripts.Classes.Enemy.enemy import Enemy
from src.Scripts.Classes.Items.Armors import *
from src.Scripts.Classes.Items.Artefacts import *
from src.Scripts.Classes.Items.base_item import *
from src.Scripts.Classes.Items.base_recepie import *
from src.Scripts.Classes.Items.Potions.potions import Potion
from src.Scripts.Classes.Items.Weapons import *
from src.Scripts.Classes.Market.base_market import Market
from src.Scripts.Classes.Trade.trade import Trade
from src.Scripts.Classes.Work.work import Work

ITEMS_PATH="src\\Assets\\Items\\items.json"
RECEPIE_PATH = "src\\Assets\\Items\\recepies.json"
CLASS_PATH = "src\\Assets\\Skills\\classes.json"
RACE_PATH = "src\\Assets\\Skills\\races.json"
BOUNTY_PATH = "src\\Assets\\Bountys\\bountys.json"
MARKET_PATH = "src\\Assets\\Markets\\markets.json"
GUILD_PATH = "src\\Assets\\Guild\\rewards.json"
WORK_PATH="src\\Assets\\Work\\work.json"
ENEMY_PATH="src\\Assets\\Enemys\\enemys.json"
FIGHT_PATH="src\\Assets\\Fights\\fights.json"

class Asset_Loader():
    '''
    This class is used to load all assets in the json files
    '''

    def load_item(self,name:str,quantity:int=None):
        '''
        load_item(name:str->Item_name,quantity:int(optional))

        loads an item from the json files with given name and quantity
        returns(Item or Weapon or Armor)
        '''
        with open(ITEMS_PATH,encoding="utf-8") as text:
            data = json.load(text)
            for k, vals in data.items():
                for v in vals:
                    i = globals()[k](**v)
                    if i.name == name:
                        if quantity:
                            i.quantity = quantity
                        return i
    
    def load_items(self):
        '''
        returns all items declared in the json files

        return item or weapon or armor
        '''
        l = []
        with open(ITEMS_PATH,encoding="utf-8") as text:
            data = json.load(text)
            for k, vals in data.items():
                for v in vals:
                    l.append(globals()[k](**v))
            return l


    def load_recepie(self,name:str):
        '''
        load_recepie(name:str->item to be crafted)

        loads an recepie for the item name given

        returns base_recepie
        '''
        with open(RECEPIE_PATH,encoding="utf-8") as text:
            data = json.load(text)
            it=[]
            for k,vals in data.items():
                for i in vals:
                    if name == i["Item"]:
                        for val in i["Items"]:
                            it.append(self.load_item(val["Name"],quantity=val["Quantity"])) 
                        return Base_Recepie(item=self.load_item(i["Item"]),skill=i["skill"],items=it)

    def load_all_recepies(self):
        '''
        loads all recepies
        return List[Base_Recepie]
        '''
        r = []
        with open(RECEPIE_PATH,encoding="utf-8") as text:
            data = json.load(text)
            for k,vals in data.items():
                for i in vals:
                    it=[]
                    for val in i["Items"]:
                        it.append(self.load_item(val["Name"],quantity=val["Quantity"])) 
                    r.append(Base_Recepie(item=self.load_item(i["Item"]),skill=i["skill"],items=it))
            return r
                    
    def load_stats(self,c:str,r:str)->dict:
        '''
        loads stats from given class and race name

        returns dict->{
            deff:
            atk:
            stamina:
            trading:
            sneak:
            cook:
            health:
            mana:
            craft:
            knowledge:
        }
        '''
        fc = open(CLASS_PATH,encoding="utf-8")
        fr = open(RACE_PATH,encoding="utf-8")
        classes = json.load(fc)
        rassen = json.load(fr)
        _c=classes[c]
        _r=rassen[r]
        return {
            "deff"       :_c["deff"]+_r["deff"],
            "atk"       :_c["atk"]+_r["atk"],
            "stamina"   :_c["stamina"]+_r["stamina"],
            "trading"   :_c["trading"]+_r["trading"],
            "sneak"     :_c["sneak"]+_r["sneak"],
            "cook"      :_c["cook"]+_r["cook"],
            "health"    :_c["health"]+_r["health"],
            "mana"      :_c["mana"]+_r["mana"],
            "craft"     :_c["craft"]+_r["craft"],
            "knowledge" :_c["knowledge"]+_r["knowledge"]
        }

    def load_races(self)->dict:
        fr = open(RACE_PATH,encoding="utf-8")
        race = json.load(fr)
        return race

    def load_p_classes(self)->dict:
        f = open(CLASS_PATH,encoding="utf-8")
        r = json.load(f)
        return r

    def load_p_class(self,class_name:str)->str:
        f = open(CLASS_PATH,encoding="utf-8")
        r = json.load(f)
        return r[class_name]

    def load_bounty(self,bounty_name:str):
        '''
        loads a bounty with given name from the json file

        return Bounty
        '''
        with open(BOUNTY_PATH) as text:
            data = json.load(text)
            for k, vals in data.items():
                for v in vals:
                    i = globals()[k](**v)
                    if i.name == bounty_name:
                        l=[]
                        for r in i.reward_items:
                            l.append(self.load_item(name=r[0],quantity=r[1]))
                        i.reward_items=l                    
                        return i
    
    def load_market(self,market_name:str)->Market:
        '''
        loads a market with the given name

        return Market
        '''
        with open(MARKET_PATH,encoding="utf-8") as text:
            data = json.load(text)
            for k, vals in data.items():
                for v in vals:
                    i = globals()[k](**v)
                    if i.name == market_name:
                        tr,bo=[],[]
                        for t in i.trades:
                            tr.append(Trade(item=self.load_item(t["item"],quantity=t["quantity"]),price=t["price"]))
                        for b in i.bountys:
                            bo.append(self.load_bounty(b))
                        i.bountys,i.trades = bo,tr
                        return i

    def load_markets(self)->List[Market]:
        '''
        loads a market with the given name

        return Market
        '''
        li=[]
        with open(MARKET_PATH,encoding="utf-8") as text:
            data = json.load(text)
            for k, vals in data.items():
                for v in vals:
                    i = globals()[k](**v)
                    tr,bo=[],[]
                    for t in i.trades:
                        tr.append(Trade(item=self.load_item(t["item"],quantity=t["quantity"]),price=t["price"]))
                    for b in i.bountys:
                        bo.append(self.load_bounty(b))
                    i.bountys,i.trades = bo,tr
                    li.append(i)
        return li

    def load_rewards(self):
        r=[]
        with open(GUILD_PATH) as text:
            data = json.load(text)
            for k, vals in data.items():
                for i in vals:
                    r.append([i["level"],i["item"]])
        return r

    def load_works(self):
        i = []
        with open(WORK_PATH,encoding="utf-8") as text:
            data = json.load(text)
            for k, vals in data.items():
                for v in vals:
                    i.append(globals()[k](**v))   
        return i

    def load_work(self,name):
        i = []
        with open(WORK_PATH,encoding="utf-8") as text:
            data = json.load(text)
            for k, vals in data.items():
                for v in vals:
                    i.append(globals()[k](**v))   
        for j in i:
            if j.name == name:
                return j

    def load_enemy(self,name):
        with open(ENEMY_PATH,encoding="utf-8") as text:
            data = json.load(text)
            for k, vals in data.items():
                for v in vals:
                    i = globals()[k](**v)
                    if i.name == name:
                        return i
        return None

    def load_fight(self,name):
        el=[]
        with open(FIGHT_PATH,encoding="utf-8") as text:
            data = json.load(text)
            for k, vals in data.items():
                for v in vals:
                    i = globals()[k](**v)
                    if i.name == name:
                        for e in i.enemys:
                            el.append(self.load_enemy(e))
                        i.enemys=el
                        return i
        return None


