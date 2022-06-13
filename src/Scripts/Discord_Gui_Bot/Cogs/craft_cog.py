from nextcord import slash_command
from nextcord.ext import commands
import nextcord
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Views.recepie_book_view import Recepie_View,Recepie_Embed
from src.Scripts.Discord_Gui_Bot.Custom_embeds.item_list_embed import item_list_embed
from src.Scripts.Discord_Gui_Bot.Custom_embeds.rezpie_embed import Rezept_embed

from src.Scripts.Classes.Database.db import DB
from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader



class Crafting_Cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.Interface = DB()
        self.Al =Asset_Loader()

    @slash_command(name="crafting",description="Zeigt alle Verfügbaren Kommands rund um Crafting")
    async def Crafting(self,interaction:nextcord.Interaction):
        pass

    @Crafting.subcommand(name="books",description="Öffnet ein Rezept buch")
    async def books(self,interaction:nextcord.Interaction):
        pass

    @books.subcommand(name="item",description="Zeigt dir das Rezeptbuch für das Craften an")
    async def item(self,interaction:nextcord.Interaction):
        await interaction.send(embed=Recepie_Embed(recepie=None,pagenumber=0,playername=str(interaction.user)),view=Recepie_View(0),ephemeral=True)


    @Crafting.subcommand(name=f'item',description=f'Craftet ein item nach einem Rezept')
    async def craft_item(self,interaction:nextcord.Interaction,item_name:str):
        ph=self.Interface.load_player(str(interaction.user))
        if ph.craft_item(self.Al.load_recepie(item_name)):
            await interaction.send(f"{interaction.user} hat {item_name} gecrafted.",ephemeral=True)
        else:
            await interaction.send(f"Überprüfe nochmals ob du alle Items für das Rezept hast oder ob du ein genug hohes Level hast",ephemeral=True)
        self.Interface.store_player(ph)     


    


    