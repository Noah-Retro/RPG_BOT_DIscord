from typing import Coroutine
from nextcord import ChannelType
import nextcord
from src.Scripts.Classes.Character.player import Player

from src.Scripts.Classes.Fireteam.base_fireteam import Base_Fireteam
from src.Scripts.Classes.Database.db import DB


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
        #Send fight embed and Fight view
        test = await interaction.channel.create_thread(name=f"Fireteam thread from: {self.ft.players[0].name}",auto_archive_duration=60,type=ChannelType.public_thread)
        await test.send("place fight embed here!",view=Fight_View(self.ft))
        pass



class Fight_View(nextcord.ui.View):
    def __init__(self,ft:Base_Fireteam):
        super().__init__(timeout=300)
        self.add_item(Fight_Attack_Button(ft))
        self.add_item(Fight_Spell_Button(ft))

    async def on_timeout(self) -> None:
        return await super().on_timeout()

    def attack(self):
        print("FT and Enemys attack")


class Fight_Attack_Button(nextcord.ui.Button):
    def __init__(self,ft:Base_Fireteam):
        super().__init__(label="Attack")
        self.ft=ft

    async def callback(self, interaction: nextcord.Interaction):
        for player in self.ft.players:
            if player.name==str(interaction.user):
                player.next_move="attack"
        await interaction.send(Enemy_Select_View(self.ft,interaction.edit),ephemeral=True)

class Fight_Spell_Button(nextcord.ui.Button):
    def __init__(self,ft:Base_Fireteam):
        super().__init__(label="Use Spell")
        self.ft=ft

    async def callback(self, interaction: nextcord.Interaction):
        db = DB()
        player=db.load_player(str(interaction.user))
        await interaction.send("Chose a spell",view=Spell_View(ft = self.ft,coro=interaction.edit),ephemeral=True)

    
class Spell_View(nextcord.ui.View):
    def __init__(self,ft:Base_Fireteam,coro:Coroutine):
        super().__init__()
    #add spell move to player
    #send enemy select view ephemeral = true
    pass



class Enemy_Select_View(nextcord.ui.View):
    def __init__(self,ft:Base_Fireteam,coro:Coroutine):
        super().__init__()
        self.add_item(Enemy_Select(ft,coro=coro))

class Enemy_Select(nextcord.ui.Select):
    def __init__(self,ft:Base_Fireteam,coro:Coroutine) -> None:
        super().__init__(playceholder="Wähle eine Ziel aus")
        