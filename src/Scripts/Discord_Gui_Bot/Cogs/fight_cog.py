from nextcord.ext import commands
from nextcord import slash_command,SlashOption,Interaction
from src.Scripts.Classes.Fireteam.base_fireteam import Base_Fireteam
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Views.fireteam_view import Fireteam_View
from src.Scripts.Classes.Database.db import DB
from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader


class Fight_Cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.Interface = DB()
        self.Al =Asset_Loader()
        self.Interface = DB()

    @slash_command(name="fight")
    async def fight(self,interaction:Interaction):
        pass

    @fight.subcommand(name="start",description="Starte einen Kampf")
    async def start(self,interaction:Interaction):
        player = self.Interface.load_player(str(interaction.user))
        fireteam = Base_Fireteam(players=[player])
        await interaction.send(embed=fireteam.embed,view=Fireteam_View(fireteam))
