from nextcord.embeds import Embed
from nextcord.ext import commands
import nextcord
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Views.trade_view import Trade_View,Trade_Embed
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.trade_field import Trade_field

from src.Scripts.Classes.Database.db import DB
from src.Scripts.Functions.logger import log
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader


class Gameplay(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.Interface = DB()
        self.Al = Asset_Loader()
        
    @commands.command(name="accept_trade",brief="Akzeptiert einen Trade")
    async def accept_item_trade(self,ctx,player_name:str,item:str,price:float=0):
        if str(ctx.message.author == player_name):
            await ctx.send(f"Du kannst deinen eigenen Trade nicht akzeptieren. Wen du ihn schliessen möchtest benutze !remove_item_trade")
            return
        ph =self.Interface.load_player(name=str(ctx.message.author))
        if ph.close_trade(item=item,price=price,ph=self.Interface.load_player(player_name)):
            await ctx.send(f"{ctx.message.author} hat den Trade {item} {price} von {player_name} akzeptiert") 
        else:
            await ctx.send(f"Trade nicht abgeschlossen")
        self.Interface.store_player(ph)

    @commands.command(name="show_trades",brief="Zeigt alle Öffentlichen Trades")
    async def show_trades(self,ctx):
        names = self.Interface.load_all_names()
        e = nextcord.Embed(title="Trades",description="Hier siehst du alle Öffentlichen Trades von jedem Spieler")
        for name in names:
            for i in range(len(name)):
                ph = self.Interface.load_player(name[i])
                Trade_field(e=e,p=ph)
        await ctx.send(embed=e)   



        