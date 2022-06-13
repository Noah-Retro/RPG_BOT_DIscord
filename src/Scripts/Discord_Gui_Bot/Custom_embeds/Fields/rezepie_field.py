from typing import List
from  src.Scripts.Classes.Items.base_recepie import Base_Recepie
import nextcord

def Rezepie_field(e:nextcord.Embed,rezepies:List[Base_Recepie],name:str=None):
    for r in rezepies:
        s=""
        for i in r.items:
            s+=f'{i.quantity}x{i.name}\n'
        e.add_field(name=r.item.name or name,value=s+f'Craft Skill: {r.skill}')
        if r.item.img !="":
            e.set_thumbnail(url=r.item.img)
    return e