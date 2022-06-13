from random import random
from nextcord import slash_command,SlashOption,user_command
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
import nextcord
from nextcord.utils import get
from src.Scripts.Classes.Damage.damage import Damage
from src.Scripts.Classes.Fireteam.base_fireteam import Base_Fireteam, Fireteam_View

from src.Scripts.Classes.Database.db import DB
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Functions.logger import log
from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader


class admin(commands.Cog):
    """Diese Commands sind nur für Administratoren des Servers gedacht.
    """
    def __init__(self,bot:commands.Bot) -> None:
        global client 
        client = bot
        self.bot = bot
        self.Interface = DB()
        self.Al = Asset_Loader()
    
    @commands.is_owner()
    @slash_command(name="give_item",description="Gibt ein Item dem angegebenen Spieler",guild_ids=[879020821174169640])
    async def give_item(self,interaction:nextcord.Interaction,player:nextcord.Member,item_name:str,quantity:int=1):
        ph=self.Interface.load_player(name=str(player))
        ph.add_item(self.Al.load_item(item_name,quantity=quantity))
        self.Interface.store_player(ph)
        s = f"{ph.name} hat {quantity}x{item_name} bekommen von {interaction.user}"
        log(1,s)
        await interaction.send(s,ephemeral=True)
    
    @commands.is_owner()
    @slash_command(name="remove_item",description="Löscht ein Item des angegebenen Spielers",guild_ids=[879020821174169640])
    async def remove_item(self,interaction:nextcord.Interaction,player:nextcord.Member,item_name:str,amount:int):
        ph = self.Interface.load_player(name=str(player))
        s = "Ein zu wenig von dem Item vorhanden"
        if ph.remove_item(item_name=item_name,quantity=amount):
            self.Interface.store_player(ph)
            s = f"{ph.name} wurde {amount}x{item_name} von {interaction.user} weggenommen"
        log(1,s)
        await interaction.send(s,ephemeral=True)

    @commands.is_owner()
    @commands.command(name="show_all_player",brief="Zeigt alle Spieler die sich eingeloggt haben",guild_ids=[879020821174169640])
    async def show_all_player(self,ctx):
        l = self.Interface.load_all_names()
        e = nextcord.Embed()
        e.add_field(name="Spieler",value=f"{l}")
        await ctx.send(embed=e)

    @commands.is_owner()
    @slash_command(name="give_money",description="Gibt an einem Spieler Geld",guild_ids=[879020821174169640])
    async def give_money(self,ctx,player_name:nextcord.Member,amount:int):
        ph=self.Interface.load_player(str(player_name))
        ph.add_money(amount)
        self.Interface.store_player(ph)
        await ctx.send(f"{player_name} wurden {amount}$ gegeben",ephemeral=True)
        log(f"{player_name} wurden {amount}$ gegeben von {ctx.user}")

    @commands.is_owner()
    @slash_command(name="take_money",description="Nimmt an einem Spieler Geld",guild_ids=[879020821174169640])
    async def take_money(self,ctx,player_name:nextcord.Member,amount:int):
        ph=self.Interface.load_player(str(player_name))
        ph.sub_money(amount)
        self.Interface.store_player(ph)
        await ctx.send(f"{player_name} wurden {amount}$ abgezogen")
        log(1,f"{player_name} wurden {amount}$ abgezogen von {ctx.user}",ephemeral=True)
 
    @commands.is_owner()
    @slash_command(name=f'set_skill',description=f'setzt einen Skill auf einen gewünschten Wert',guild_ids=[879020821174169640])
    async def set_skill(self,ctx:nextcord.Interaction,player_name:nextcord.Member,skill:str=SlashOption(name="skill",description="Der Skill zum setzten",choices={"def":"deff","atk":"atk","stamina":"stamina","trading":"trading","sneak":"sneak","cook":"cook","health":"health","mana":"mana","craft":"craft","knowledge":"knowledge","speed":"speed"}),value:int=1):
        ph=self.Interface.load_player(str(player_name))
        setattr(ph,skill,value)
        self.Interface.store_player(ph)
        log(1,f"{player_name} sein {skill} Skill wurde auf {value} gesetzt von {ctx.user}")
        await ctx.send(f"{player_name} sein {skill} Skill wurde auf {value} gesetzt",ephemeral=True)

    
    @commands.is_owner()
    @user_command(name="delete character",guild_ids=[879020821174169640])
    async def del_character(self,interaction:nextcord.Interaction,user):
        print(interaction,user)
        self.Interface.del_player(str(user))
        await interaction.send(f"{user} wurde gelöscht")
        log(1,f"{interaction.user} hat {user} seinen Character gelöscht")

    @commands.is_owner()
    @commands.command(name="DELETE_DATABASE",brief="Löscht alle Spieler aus der Datenbank.")
    async def del_all_player(self,ctx):
        self.Interface.del_db()
        await ctx.send("Die datenbank wurde zurückgesetzt.")
        
    @commands.is_owner()
    @user_command(name="stop work state",guild_ids=[879020821174169640])
    async def set_state(self,ctx,user):
        ph=self.Interface.load_player(str(user))
        ph.pause()
        self.Interface.store_player(ph)
        await ctx.send(f"Player {user} stoped working")

    
    @commands.is_owner()
    @commands.command(name="TestF")
    async def TestF(self,ctx):
        f = Base_Fireteam(players=[self.Interface.load_player(name=str(ctx.message.author))])
        await ctx.send(embed=f.embed,view=Fireteam_View(f))
    
    @commands.is_owner()
    @slash_command()
    async def take_damage(self,ctx:nextcord.Interaction,user:nextcord.Member):
        ph=self.Interface.load_player(str(user))
        ph.receve_damage(Damage("Hey",10,False))
        self.Interface.store_player(ph)
