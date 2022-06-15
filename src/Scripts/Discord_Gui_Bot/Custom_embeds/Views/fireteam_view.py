from typing import Coroutine
from nextcord import ChannelType
import nextcord

from src.Scripts.Classes.HealthBar.healthbar import HelthBar
from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Classes.Fireteam.base_fireteam import Base_Fireteam
from src.Scripts.Classes.Database.db import DB

class Fight_Embed(nextcord.Embed):
    def __init__(self,ft:Base_Fireteam):
        super().__init__(colour=ft.players[0].color)
        for i in ft.players:
            self.add_field(name = i.name,value=f"""
                {HelthBar.healthbar(i.health-i.damage,i.health)} Helath
                {HelthBar.healthbar(i.mana-i.mana_used,i.mana)} Mana
                {HelthBar.healthbar(i.stamina-i.stamina_used,i.stamina)} Stamina
                Nextmove: {i.next_move}
            """)
        i=0
        first=False
        for e in ft.fight.enemys:
            self.add_field(name=f"{e.name}:{i}",value=f"Health: {e.health}, Weapon: {e.weapon['name']}",inline=first)
            first = True
            i+=1

class Fireteam_View(nextcord.ui.View):
    def __init__(self,ft:Base_Fireteam):
        super().__init__()
        self.ft=ft

    @nextcord.ui.button(label="join")
    async def joinb(self,button,interaction):
        d = DB()
        p = d.load_player(str(interaction.user))
        p.fireteam=self.ft
        self.ft.join(p)
        await interaction.message.edit(embed=self.ft.embed)

    @nextcord.ui.button(label="leave")
    async def leveb(self,button,interaction:nextcord.Interaction):
        d = DB()
        p = d.load_player(str(interaction.user))
        p.fireteam=None
        self.ft.leave(str(interaction.user))
        await interaction.message.edit(embed=self.ft.embed)

    @nextcord.ui.button(label="start fight")
    async def startb(self,button,interaction:nextcord.Interaction):
        #set fight of fireteam
        al = Asset_Loader()
        if self.ft.fight == None:
            #Make it random
            self.ft.fight=al.load_fight("Test Fight")
            
        #Send fight embed and Fight view
        self.stop()
        test = await interaction.channel.create_thread(name=f"Fireteam thread from: {self.ft.players[0].name}",auto_archive_duration=60,type=ChannelType.public_thread)
        await test.send(embed=Fight_Embed(self.ft),view=Fight_View(self.ft))
        await interaction.message.delete()


class Fight_View(nextcord.ui.View):
    def __init__(self,ft:Base_Fireteam):
        super().__init__(timeout=300)
        self.ft=ft
        self.add_item(Fight_Attack_Button(ft))
        self.add_item(Fight_Spell_Button(ft))
        self.add_item(Skip_Input_Button(ft))


class Skip_Input_Button(nextcord.ui.Button):
    def __init__(self,ft:Base_Fireteam):
        super().__init__(label="Skip Input")
        self.ft = ft

    async def callback(self, interaction: nextcord.Interaction):
        beendet,playerwin= self.ft.atack()
        if playerwin:
            await interaction.message.delete()
            self.ft.close()
            await interaction.send("Der Kampf wurde beendet! Die Spieler haben gewonnen")
            return
        await interaction.edit(embed=Fight_Embed(self.ft),view=Fight_View(self.ft))


class Fight_Attack_Button(nextcord.ui.Button):
    def __init__(self,ft:Base_Fireteam):
        super().__init__(label="Attack")
        self.ft=ft

    async def callback(self, interaction: nextcord.Interaction):
        for player in self.ft.players:
            if player.name==str(interaction.user):
                player.next_move="attack"
        await interaction.send(content="Wähle einen Gegner aus",view=Enemy_Select_View(self.ft,interaction.edit),ephemeral=True)

class Fight_Spell_Button(nextcord.ui.Button):
    def __init__(self,ft:Base_Fireteam):
        super().__init__(label="Use Spell")
        self.ft=ft

    async def callback(self, interaction: nextcord.Interaction):
        for player in self.ft.players:
            if player.name==str(interaction.user):
                player.next_move="spell"
        await interaction.send("Chose a spell",view=Spell_View(ft = self.ft,coro=interaction.edit,player_name=str(interaction.user)),ephemeral=True)

    
class Spell_View(nextcord.ui.View):
    def __init__(self,ft:Base_Fireteam,coro:Coroutine,player_name):
        super().__init__()
        self.add_item(Spell_Select(ft,coro,player_name))
    #add spell move to player
    #send enemy select view ephemeral = true
    pass

class Spell_Select(nextcord.ui.Select):
    def __init__(self,ft:Base_Fireteam,coro:Coroutine,player_name:str) -> None:
        super().__init__(placeholder="Chose a Spell")
        self.coro = coro
        self.ft=ft
        for p in ft.players:
            if p.name == player_name:
                if p.spells == None:
                    self.add_option(label="You have no spells",value=":None:None")
                    return
                for spell in p.spells:
                    self.add_option(label=spell.name,value=":"+spell.name+":"+spell.type)
    
    async def callback(self, interaction: nextcord.Interaction):
        for player in self.ft.players:
            player.next_move += self.values[0]
        if self.values[0].split(":")[1] == "single":
            await interaction.send(content="Wähle ein Ziel aus",view=Enemy_Select_View(self.ft,self.coro,singel=True),ephemeral=True)
            return
        await interaction.send(content="Wähle einen Gegner aus",view=Enemy_Select_View(self.ft,self.coro),ephemeral=True)
        await interaction.message.delete()

class Enemy_Select_View(nextcord.ui.View):
    def __init__(self,ft:Base_Fireteam,coro:Coroutine):
        super().__init__()
        self.add_item(Enemy_Select(ft,coro=coro))

class Enemy_Select(nextcord.ui.Select):
    def __init__(self,ft:Base_Fireteam,coro:Coroutine,single=True) -> None:
        super().__init__(placeholder="Wähle ein Ziel aus")
        self.coro=coro
        self.ft = ft
        i= 0
        if not single:
            self.add_option(label="Enemys",value="Enemys:0")
            self.add_option(label="Allays",value="Allays:0")

        for e in ft.fight.enemys:
            self.add_option(label=f"{e.name}:{i}",value=f":{e.name}:{i}")
            i+=1
        i = 0
        for e in ft.players:
            self.add_option(label=f"{e.name}:{i}",value=f":{e.name}:{i}")
            i+=1

    async def callback(self, interaction: nextcord.Interaction):
        for p in self.ft.players:
            if p.name==str(interaction.user):
                p.next_move+=self.values[0]
        await self.coro(embed=Fight_Embed(self.ft),view=Fight_View(self.ft))
        await interaction.message.delete()
        