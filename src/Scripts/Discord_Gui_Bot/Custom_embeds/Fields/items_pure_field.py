from typing import Any

from src.Scripts.Classes.Items.Armors.armor import Armor
from src.Scripts.Classes.Items.Artefacts.artefact import Artefact
from src.Scripts.Classes.Items.base_item import Base_Item
from src.Scripts.Classes.Items.Weapons.weapon import Weapon

def Items_pure_field(e,item:Any):
    if isinstance(item,Weapon) or issubclass(type(item),Weapon):
        e.add_field(name=item.name,value=f'Waffe: {item.name} {item.value}$ atk{item.atk}',inline=False)
    elif isinstance(item,Armor) or issubclass(type(item),Armor):
        e.add_field(name=item.name,value=f'Rüstung: {item.name} {item.value}$ def{item.deff}',inline=False)
    elif isinstance(item,Artefact) or issubclass(type(item),Artefact):
        e.add_field(name=item.name,value=f'Artefakt: {item.name} {item.value}$ def:{item.deff} atk:{item.atk} stamina:{item.stamina} mana:{item.mana}',inline=False)
    elif isinstance(item,Base_Item) or issubclass(type(item),Base_Item):
        e.add_field(name=item.name,value=f'Item: {item.name} {item.value}$',inline=False)
    else:
        e.add_field(name="*")
    return e
    