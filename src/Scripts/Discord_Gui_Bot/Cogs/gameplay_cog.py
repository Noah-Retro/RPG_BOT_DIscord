from discord import slash_command
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

    @slash_command(name="trade",description="Gruppe aller Trade commands")    
    async def trade(self,interaction):
        pass

    @trade.subcommand(name="accept",description="Akzeptiert einen Trade")
    async def accept_item_trade(self,interaction,player:nextcord.Member,item:str,price:float=0):
        if str(interaction.user == str(player)):
            await interaction.send(f"Du kannst deinen eigenen Trade nicht akzeptieren. Wen du ihn schliessen möchtest benutze !remove_item_trade")
            return
        ph =self.Interface.load_player(name=str(interaction.user))
        if ph.close_trade(item=item,price=price,ph=self.Interface.load_player(str(player))):
            await interaction.send(f"{interaction.user} hat den Trade {item} {price} von {player} akzeptiert") 
        else:
            await interaction.send(f"Trade nicht abgeschlossen")
        self.Interface.store_player(ph)

    @trade.subcommand(name="show",description="Zeigt alle Öffentlichen Trades")
    async def show_trades(self,interaction):
        names = self.Interface.load_all_names()
        e = nextcord.Embed(title="Trades",description="Hier siehst du alle Öffentlichen Trades von jedem Spieler")
        for name in names:
            for i in range(len(name)):
                ph = self.Interface.load_player(name[i])
                Trade_field(e=e,p=ph)
        await interaction.send(embed=e)   



        