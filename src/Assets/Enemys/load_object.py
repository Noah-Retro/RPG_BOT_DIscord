import json
from DatenKlassen.Enemy.Enemy import Enemy
from Objects.Items.load_objects import load_item

ENEMY_PATH = "RPG_BOT_Project\RPG_BOT_VSA\Objects\Enemys\enemys.json"

def load_enemy(enemy_name:str=None,level:int=None):
    f = open(ENEMY_PATH,"r")
    data =json.load(f)
    for e in data:
        li=[]
        if e == enemy_name or data[e]["level"]==level:
            for i in data[e]["drop"]:
                li.append(i)
            enemy = Enemy(_name=e,
            _level=data[e]["level"],
            _atk=data[e]["atk"],
            _def=data[e]["def"],
            _weapon=load_item(weapon=data[e]["weapon"]),
            _armor=load_item(armor=data[e]["armor"]),
            _drop=li,
            _spell=data[e]["spell"])
    return enemy or None   

def load_enemys():
    le=[]
    f = open(ENEMY_PATH,"r")
    data =json.load(f)
    for e in data:
        li=[]
        
        for i in data[e]["drop"]:
            li.append(i)
        enemy = Enemy(_name=e,
        _level=data[e]["level"],
        _atk=data[e]["atk"],
        _def=data[e]["def"],
        _weapon=load_item(weapon=data[e]["weapon"]),
        _armor=load_item(armor=data[e]["armor"]),
        _drop=li)
        le.append(enemy)
    return le

if __name__=="__main__":
    load_enemy()