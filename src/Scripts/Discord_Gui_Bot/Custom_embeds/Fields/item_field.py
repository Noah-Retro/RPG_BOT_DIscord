import nextcord
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Classes.Items.Armors.armor import Armor
from src.Scripts.Classes.Items.base_item import Base_Item
from src.Scripts.Classes.Items.Weapons.weapon import Weapon
from src.Scripts.Classes.Items.Artefacts.artefact import Artefact

def Item_field(e:nextcord.Embed,p:Player)->nextcord.Embed:
    s="Kein Item vorhanden"
    if p.items != [] and p.items != None:
        s = ""
        for i in p.items:
            if isinstance(i,Weapon) or issubclass(type(i),Weapon):
                s += f'Waffe: {i.quantity}x{i.name} {i.value}$ atk{i.atk if i.atk != None else ""}\n'
            elif isinstance(i,Armor)or issubclass(type(i),Armor):
                s += f'Rüstung: {i.quantity}x{i.name} {i.value }$ def{i.deff if i.deff != None else ""}\n'
            elif isinstance(i,Artefact) or issubclass(type(i),Artefact):
                e.add_field(name="Artefakt",value=f'{i.quantity}x{i.name} {i.value}$ def:{i.deff} atk:{i.atk} stamina:{i.stamina} mana:{i.mana}',inline=False)
            elif isinstance(i,Base_Item):
                s += f'Item: {i.quantity}x{i.name} {i.value}$\n'

    e.add_field(name="Items",value=s,inline=False)
    return e