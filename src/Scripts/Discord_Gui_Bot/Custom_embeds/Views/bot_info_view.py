import nextcord
from docs.infos import *



class Current_State_Embed(nextcord.Embed):
    def __init__(self):
        super().__init__(title=f"Infos zum RPG Bot Version {VERSION}",description=f"{DESCRIPTION}")
        for l in CURRENT_CHANGELOGG:
            self.add_field(name=l["title"],value=l["body"],inline=False)
        self.set_footer(text=CREATED)
        self.set_author(name=AUTHOR,url=GITHUBACCLINK,icon_url="https://avatars.githubusercontent.com/u/61364708?v=4")
    
class Timeline_Embed(nextcord.Embed):
    def __init__(self):
        super().__init__(title=f"Infos zum RPG Bot Version {VERSION}")
        s = VERSIONTIMELINE.split("|")
        for t in s:
            self.add_field(name="Versions Verlauf",value=t,inline=False)
        self.set_footer(text=CREATED)
        self.set_author(name=AUTHOR,url=GITHUBACCLINK,icon_url="https://avatars.githubusercontent.com/u/61364708?v=4")

class Guidlines_Embed(nextcord.Embed):
    def __init__(self):    
        super().__init__(title=f"Infos zum RPG Bot Version {VERSION}")
        self.add_field(name="Guidlines",value=GUIDLINES,inline=False) 
        self.set_footer(text=CREATED)
        self.set_author(name=AUTHOR,url=GITHUBACCLINK,icon_url="https://avatars.githubusercontent.com/u/61364708?v=4")

class More_Info_Embed(nextcord.Embed):
    def __init__(self):    
        super().__init__(title=f"Infos zum RPG Bot Version {VERSION}")
        self.add_field(name="Bugs",value=BUGS,inline=False)
        self.add_field(name="Discordserver",value=DISCORD_SERVER,inline=False)
        self.set_footer(text=CREATED)
        self.set_author(name=AUTHOR,url=GITHUBACCLINK,icon_url="https://avatars.githubusercontent.com/u/61364708?v=4")



class Timeline_Button(nextcord.ui.Button):
    def __init__(self):
        super().__init__( label="Timeline")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.edit(embed=Timeline_Embed())

class More_Infos_Button(nextcord.ui.Button):
    def __init__(self):
        super().__init__( label="More Infos")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.edit(embed=More_Info_Embed())

class Current_State_Button(nextcord.ui.Button):
    def __init__(self):
        super().__init__( label="Current Changeloggs")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.edit(embed=Current_State_Embed())
    
class Guidline_Button(nextcord.ui.Button):
    def __init__(self):
        super().__init__( label="Guid Lines")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.edit(embed=Guidlines_Embed())

class Bot_Info_View(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Current_State_Button())
        self.add_item(Timeline_Button())
        self.add_item(More_Infos_Button())
        self.add_item(Guidline_Button())


