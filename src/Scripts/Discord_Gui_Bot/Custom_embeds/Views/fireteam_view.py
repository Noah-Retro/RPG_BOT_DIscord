from nextcord import ChannelType
import nextcord

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
        await interaction.channel.create_thread(name=f"Fireteam thread from: {self.ft.players[0].name}",auto_archive_duration=60,type=ChannelType.public_thread)
        pass



class Fight_View(nextcord.ui.View):
    def __init__(self,ft:Base_Fireteam):
        super().__init__(timeout=300)


    async def on_timeout(self) -> None:
        return await super().on_timeout()

    def attack(self):
        print("FT and Enemys attack")


class Fight_Attack_Button(nextcord.ui.Button):
    def __init__(self):
        super().__init__(label="Attack")

