from src.Scripts.Classes.Character.player import Player
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.looks_field import Looks_field
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.stats_field import Stats_field
import nextcord

from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.balance_field import Balance_field
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.bounty_field import Bounty_field
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.equipment_field import Equipment_field
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.item_field import Item_field
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.trade_field import Trade_field

def inventory_embed(ctx,p:Player):
    e = nextcord.Embed(title=f"Inventar von {p.character_name}",description="Zeigt dir alle deine Items, deine Trades, deine Momentane Waffe, deine Momentane Rüstung und deinen momentanen Kontostand")
    e = Balance_field(e,p)
    e = Equipment_field(e,p)
    e = Stats_field(e,s = p.stats)
    e = Looks_field(e,p)   
    e = Bounty_field(e,p)
    e.set_thumbnail(url=str(p.img))
    e.add_field(name="Status",value=f'{":x:" if p.working else ":white_check_mark:"}')
    return e