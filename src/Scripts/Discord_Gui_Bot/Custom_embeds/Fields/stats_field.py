import nextcord
from src.Scripts.Classes.Stats.player_stat import Stat

def Stats_field(e:nextcord.Embed,s,rasse="",klasse="")->nextcord.Embed:
    if s == None:
        return e
    e.add_field(name=f"Stats {rasse} {klasse}",value=f"""
        **def:**     {s.deff } **atk:**     {s.atk }
        **stamina:** {s.stamina } **trading:**  {s.trading }
        **sneak:**    {s.sneak } **cook:**     {s.cook }
        **health:**   {s.health } **mana:**     {s.mana }
        **craft:**    {s.craft } **knowledge:**   {s.knowledge}
        **speed:**    {s.speed}""")
    return e