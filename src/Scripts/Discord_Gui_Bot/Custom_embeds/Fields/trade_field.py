from typing import List
import nextcord
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Classes.Trade.trade import Trade


def Trade_field(e:nextcord.Embed,p:Player):#-> discord.Embed:
    s="Kein offener Trade"
    if p.trades != [] and p.trades != None:
        s=""
        for t in p.trades:
            if t.public:
                s += f'{t.item.quantity}x{t.item.name} at {t.price}$\n'
            else:
                s += "Privater trade\n"
    e.add_field(name="Trades",value=s,inline=False)  
    return e