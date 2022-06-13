import nextcord
from src.Scripts.Classes.Character.player import Player


def Balance_field(e:nextcord.Embed,p:Player)->nextcord.Embed:
    e.add_field(name="Kontostand",value=f'{p.money}$',inline=False)
    return e