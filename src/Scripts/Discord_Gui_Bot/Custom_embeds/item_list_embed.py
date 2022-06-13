from typing import List
from src.Scripts.Classes.Items.base_item import Base_Item
import nextcord

from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.items_pure_field import Items_pure_field

def item_list_embed(ctx,li):
    e = nextcord.Embed(title=f"Items",description="Zeigt dir alle Items, Waffen und Rüstungen an")
    for i in li:  
        e = Items_pure_field(e,i)       
    return e