from random import random
from discord import SlashOption, slash_command,user_command

import nextcord
from nextcord.ext import commands
from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader
from src.Scripts.Classes.Database.db import DB
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Modals.create_guild_modal import (
    Create_Guild_Modal, Create_Guild_View)

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

class Guild_Cog(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.Interface=DB()
        self.Al = Asset_Loader()
        self.__cog_name__="Guild_Cog"

    @slash_command(name="guild",description="Benutze die subcommands um die funktionen zu verwenden")
    async def guild(self,interaction:nextcord.Interaction):
        pass

    @guild.subcommand(name="leave",description="Verlasse deine Guilde")
    async def leave_guild(self,interaction:nextcord.Interaction):
        player = self.Interface.load_player(str(interaction.user))
        guild = self.Interface.load_guild(player.guild)
        if guild.leader == str(interaction.user):
            await interaction.send("Du bist der Anführer der Guilde! Ernenne jemand anderes zum Anführer oder lösche die gesammte guilde")
            return
        guild.remove_player(str(interaction.user))
        player.guild=""
        self.Interface.store_guild(guild)
        self.Interface.store_player(player)
        await interaction.send(f"Du hast die Guilde {guild.name} verlassen",ephemeral=True)

    @guild.subcommand(name="create",description="Form für erstellung einer Guilde")
    async def create_guild(self,interaction:nextcord.Interaction):
        await interaction.response.send_modal(Create_Guild_Modal())
        
    @user_command(name="Invite to Guild")        
    async def guild_invite(self,interaction:nextcord.Interaction,playeri:nextcord.Member):
        
        class Button_Accept(nextcord.ui.Button):
            def __init__(self, *, style: nextcord.ButtonStyle = nextcord.ButtonStyle.green, label = "Accept Invite",playername:str,guild:str):
                super().__init__(style=style, label=label, custom_id=f"Custom_ID:{random()}")
                self.playername = playername
                self.guild = guild
                self.Interface = DB()
                self.Al = Asset_Loader()

            async def callback(self, interaction: nextcord.Interaction):
                player = self.Interface.load_player(self.playername)
                guild = self.Interface.load_guild(self.guild)
                if not guild.add_player(player.name):
                    await interaction.send("Das Beitreten der Guilde ist fehlgeschlagen")
                player.guild = guild.name
                self.Interface.store_player(player)
                self.Interface.store_guild(guild)
                await interaction.send(f"Du bist jetzt Mitglied der Guilde {guild.name}")    

        class Invite(nextcord.ui.View):
            def __init__(self,playername:str,guild:str):
                super().__init__(timeout=None)
                self.add_item(Button_Accept(playername=playername,guild=guild))
        
        player = self.Interface.load_player(str(interaction.user))
        guild = self.Interface.load_guild(player.guild)
        
        if str(playeri) in guild.players:
            await interaction.send("Member is already in your guild")
            return

        player_split = str(playeri).split("#")
        user = nextcord.utils.get(interaction.guild.members, name=player_split[0], discriminator=player_split[1])
        await user.send(f"{guild.leader} hat dich eingeladen um der Guilde {guild.name} beizutreten",view=Invite(str(playeri),guild.name))
        await interaction.send("Der Spieler wurde eingeladen",ephemeral=True)


    @guild.subcommand(name="invite",description="Lade einen Spieler in deine Gilde ein")
    async def guild_invite(self,interaction:nextcord.Interaction,playeri:nextcord.Member):
        
        class Button_Accept(nextcord.ui.Button):
            def __init__(self, *, style: nextcord.ButtonStyle = nextcord.ButtonStyle.green, label = "Accept Invite",playername:str,guild:str):
                super().__init__(style=style, label=label, custom_id=f"Custom_ID:{random()}")
                self.playername = playername
                self.guild = guild
                self.Interface = DB()
                self.Al = Asset_Loader()

            async def callback(self, interaction: nextcord.Interaction):
                player = self.Interface.load_player(self.playername)
                guild = self.Interface.load_guild(self.guild)
                if not guild.add_player(player.name):
                    await interaction.send("Das Beitreten der Guilde ist fehlgeschlagen")
                player.guild = guild.name
                self.Interface.store_player(player)
                self.Interface.store_guild(guild)
                await interaction.send(f"Du bist jetzt Mitglied der Guilde {guild.name}")    

        class Invite(nextcord.ui.View):
            def __init__(self,playername:str,guild:str):
                super().__init__(timeout=None)
                self.add_item(Button_Accept(playername=playername,guild=guild))
        
        player = self.Interface.load_player(str(interaction.user))
        guild = self.Interface.load_guild(player.guild)
        
        if str(playeri) in guild.players:
            await interaction.send("Member is already in your guild")
            return

        player_split = str(playeri).split("#")
        user = nextcord.utils.get(interaction.guild.members, name=player_split[0], discriminator=player_split[1])
        await user.send(f"{guild.leader} hat dich eingeladen um der Guilde {guild.name} beizutreten",view=Invite(str(playeri),guild.name))
        await interaction.send("Der Spieler wurde eingeladen",ephemeral=True)

    @guild.subcommand(name="delete",description="Löscht deine Guilde, wen du der Anführer bist")
    async def guild_del(self,interaction:nextcord.Interaction):
        player = self.Interface.load_player(str(interaction.user))
        guild = self.Interface.load_guild(player.guild)
        player.guild= ""
        self.Interface.store_player(player)
        
        if player.name != guild.leader:
            return
        self.Interface.del_guild(guild.name)
        guildl = interaction.guild
        
        for p in guild.players:
            if p != None and p != "":
                players = self.Interface.load_player(p)
                players.guild = ""
                self.Interface.store_player(players)
        
        for ch in guildl.channels:
            if ch.id == guild.textchannel_id or ch.id == guild.voicechannel_id:
                await ch.delete()
        
        for c in guildl.categories:
            if c.id == guild.category_id:
                await c.delete()    
        await interaction.send("Du hast deine Guilde aufgelöst",ephemeral=True)

    @guild.subcommand(name="show",description="Zeigt deine Guilde")
    async def guild_show(self,interaction:nextcord.Interaction):
        player = self.Interface.load_player(str(interaction.user))
        guild = self.Interface.load_guild(player.guild)   
        if guild != False:     
            await interaction.send(embed=guild.embed,ephemeral=False)
        else:
            await interaction.send("Du bist noch in keiner Guilde",ephemeral=True)

    @guild.subcommand(name="kick")
    async def guild_kick(self,interaction:nextcord.Interaction,playername:nextcord.User):
        player = self.Interface.load_player(str(interaction.user))
        guild = self.Interface.load_guild(player.guild)
        playerr = self.Interface.load_player(str(playername))
        if player.name != guild.leader:
            await interaction.send("Du bist nicht der Anführer der Guilde",ephemeral=True)
            return
        guild.remove_player(str(playername))
        playerr.guild=""
        self.Interface.store_guild(guild)
        self.Interface.store_player(playerr)
        await interaction.send(f"Du hast {playername} aus der Guilde gekickt",ephemeral=True)

    @guild.subcommand(name="promote")
    async def guild_promote(self,interaction:nextcord.Interaction,playername:nextcord.Member):
        player = self.Interface.load_player(str(interaction.user))
        guild = self.Interface.load_guild(player.guild)
        playerr = self.Interface.load_player(str(playername))
        guild.leader=str(playername)
        guild.add_player(str(interaction.user))
        self.Interface.store_guild(guild)
        await interaction.send(f"{playername} ist jetzt der anführer der Guilde {guild.name}",ephemeral=True)

    @commands.has_permissions(administrator=True)
    @commands.command(name="populate_guild",hidden=True)
    async def populate_guild(self,ctx:commands.Context):
        player = self.Interface.load_player(str(ctx.message.author))
        guild = self.Interface.load_guild(player.guild)
        for i in range(10,34):
            guild.add_player(f"Player#02{i}")
        self.Interface.store_guild(guild)

    @guild.subcommand(name="change_color",description="Änder die farbe für deine Guilde")
    async def change_color(self,interaction:nextcord.Interaction,
    color=SlashOption(choices=ColorsOptions)):
        ec = nextcord.Color(0)
        player = self.Interface.load_player(str(interaction.user))
        guild= self.Interface.load_guild(player.guild)
        guild.color=ec.__getattribute__(color)()
        self.Interface.store_guild(guild)
        await interaction.send(embed=guild.embed,ephemeral=True)