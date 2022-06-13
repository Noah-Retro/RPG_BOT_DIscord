from typing import overload
from nextcord.ext import commands
import nextcord
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Views.bot_info_view import Bot_Info_View,Current_State_Embed
from docs.infos import *



class infos(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
    
    @commands.command(name="info",aliases=["Info","Bot"],brief="Zeigt Infos zu dem Bot")
    async def info(self,ctx):
        await ctx.send(embed =Current_State_Embed(),view=Bot_Info_View())
        
    @commands.command(name=f'create_item_info',brief=f'Gibt Infos wie man ein Item erstellen kann.')
    async def create_item_info(self,ctx):
        e = nextcord.Embed(title="How to Create a Gameobject",description="Hier zeigt es dir an wie du ein Item erstellen kannst.")
        e.add_field(name="Item",value=CREATE_OBJECTS)
        await ctx.send(embed=e)
        