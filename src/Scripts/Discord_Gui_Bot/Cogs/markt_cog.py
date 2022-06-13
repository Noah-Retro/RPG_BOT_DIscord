from nextcord import slash_command
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import bot
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Views.market_view import Market_View
from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader
from src.Scripts.Classes.Database.db import DB
from src.Scripts.Classes.Market.base_market import Market
from src.Scripts.Functions.logger import log


class Market_Trading(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.Al = Asset_Loader()
        self.Interface = DB()

    @slash_command(name="market",description="Zeigt alle Märkte")
    async def Market(self,interaction:nextcord.Interaction):
        ma = self.Al.load_markets()
        await interaction.send("Choose a market where you want to go",view=Market_View(ma),ephemeral=True)