from os import name
from discord import SlashOption
from nextcord import slash_command
import nextcord
from nextcord.ext import commands
from nextcord.ui import view
from pandas import options
from src.Scripts.Discord_Gui_Bot.Custom_embeds.character_embed import character_embed
from src.Scripts.Discord_Gui_Bot.Custom_embeds.inventory_embed import inventory_embed
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Views.inventory_view import Inventory_View, Stats_Inventory_Select, Stats_Inventory_View, stats_embed
from src.Scripts.Classes.Database.db import DB
from src.Scripts.Functions.logger import log
from docs.infos import AUTHOR, GITHUBACCLINK
import validators

ColorsOptions=[
'blue',
'blurple',
'brand_green',
'brand_red',
'dark_gold',
'dark_green',
'dark_magenta',
'dark_orange',
'dark_purple',
'dark_red',
'darker_grey',
'fuchsia',
'gold',
'green',
'greyple',
'light_gray',
'magenta',
'og_blurple',
'orange',
'purple',
'random',
'red',
'teal',
'yellow']


class player_infos(commands.Cog):
    def __init__(self,bot:nextcord.Client):
        self.bot = bot
        self.Interface = DB()
        self.__cog_name__="Player_Cog"
        
    @slash_command(name="player",description="Zeigt dir alle Commands für den Spieler an")
    async def player(self,interaction:nextcord.Interaction):
        pass

    @player.subcommand(name="inventory",description="Zeigt dein Inventar")
    async def show_inventory(self,interaction:nextcord.Interaction,show_off=SlashOption(name="show",description="True = alle können es sehen",required=False,default="False",choices=["False","True"])):
        p=self.Interface.load_player(name=str(interaction.user))
        e = character_embed(interaction,p)
        if show_off=="True":
            await interaction.send(embed=e)
            return 
        view = Inventory_View(p)
        await interaction.send(embed=e,view=view,ephemeral=bool(show_off=="False"))
        
        #await interaction.edit(view=view)

    @player.subcommand(name="stats",description="Zeigt deine Stats und die möglichkeit deine Skillpunkte zu verwenden")
    async def stats(self,interaction:nextcord.Interaction):
        player = self.Interface.load_player(str(interaction.user))
        view = Stats_Inventory_View(player)
        embed = stats_embed(player)
        await interaction.send(embed=embed,view=view,ephemeral=True)

    @player.subcommand(name="change",description="Ändere dein aussehen oder deine beschreibungen")
    async def change(self,interaction:nextcord.Interaction):
        print("Test")

    @change.subcommand(name="image",description="Ändere dein Character Bild. NUR DIREKTE LINKS ZU BILDER")
    async def image(self,interaction:nextcord.Interaction,imgurl:str):
        player = self.Interface.load_player(str(interaction.user))
        if not validators.url(imgurl):
            await interaction.send("Der input ist keine gültige URL",ephemeral=True)
        player.img = imgurl
        self.Interface.store_player(player)
        await interaction.send("Dein Bild wurde geupdated",ephemeral=True)

    @change.subcommand(name="color",description="Farbe für deine Embeds")
    async def color(self,interaction:nextcord.Interaction,
        color=SlashOption(choices=ColorsOptions)):
        ec = nextcord.Color(0)
        player = self.Interface.load_player(str(interaction.user))
        player.color=ec.__getattribute__(color)()
        self.Interface.store_player(player)
        await interaction.send(f"Deine Farbe ist jetzt {color}",ephemeral=True)

    @change.subcommand(name="character_name",description="Ändere deinen Charakername")
    async def character_name(self,interaction:nextcord.Interaction,name:str):
        player = self.Interface.load_player(str(interaction.user))
        player.character_name = name
        self.Interface.store_player(player)
        await interaction.send(f"Dein Character heisst jetzt {name}",ephemeral=True)


    #@player.subcommand(name="help",description="Zeigt dir die Hilfe für diese Befehle an")
    #async def help(self,interaction:nextcord.Interaction):
    #    r=""
    #    e=nextcord.Embed()
    #    for c in self.bot.get_all_application_commands():
    #        if c.name=="player":
    #            e.title=c.name
    #            for s in c.children:
    #                r+=f"   **Description**: {c.children[s].description}\n"
    #                for o in c.children[s].options:
    #                    r+=f"       **{c.children[s].options[o].name}**: {c.children[s].options[o].description}\n"
    #                    #r+=f"          **Choices**: {c.children[s].options[o].choices if c.children[s].options[o].choices != '...' else 'None' }\n"
    #                    
    #                if len(r)>1024:
    #                    e.add_field(name=f"__{c.children[s].name}__",value=r[0-1024],inline=False)
    #                else:
    #                    e.add_field(name=f"__{c.children[s].name}__",value=r,inline=False)
    #                r=""
    #    await interaction.send(embed=e,ephemeral=True)
        

                

                


