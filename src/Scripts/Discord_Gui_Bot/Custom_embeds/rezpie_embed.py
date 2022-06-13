import nextcord

from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.rezepie_field import Rezepie_field
from typing import List
from src.Scripts.Classes.Items.base_recepie import Base_Recepie

def Rezept_embed(rezepies:List[Base_Recepie],name:str=None):  
    e = nextcord.Embed(title="Rezepte",description="Alle hier aufgeführten rezepte können gecrafted werden")
    Rezepie_field(e,rezepies,name=name)
    return e
    