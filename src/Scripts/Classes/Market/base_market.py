import dataclasses
from typing import Any, List

from docs.conf import *
from src.Scripts.Classes.Items.base_item import Base_Item
from src.Scripts.Classes.Bounty.bounty import Bounty
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Classes.Database.db import DB
from src.Scripts.Classes.Trade.trade import Trade


@dataclasses.dataclass
class Market():
    name:str=""
    trades:List[Trade]=None
    bountys:List[Bounty]=None
    Interface=DB()
    level:int=1

    def trade(self,item:Base_Item,player:Player):
        for t in self.trades:
            if t.item==item:
                rabat=t.price * player.trading * TRADE_DISCOUNT
                if player.sub_money(t.price-rabat):
                    player.add_item(t.item)
                    final_price = t.price-rabat
                    return True,final_price
        return False,0

    def give_bounty(self,player:Player,bounty:Bounty):
        for b in self.bountys:
            if b.name == bounty.name:
                player.add_bounty(b)
                return True
        return False
