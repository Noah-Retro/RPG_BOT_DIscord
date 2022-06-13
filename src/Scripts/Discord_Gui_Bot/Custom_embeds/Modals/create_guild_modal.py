import nextcord
from nextcord.ui import Modal,Select,TextInput,View,Button
from src.Scripts.Classes.Character.player import Player

from src.Scripts.Classes.Database.db import DB

class Create_Guild_Modal(Modal):
    def __init__(self, title: str="Fill in the fields to create an Guild"):
        super().__init__(title)
        self.Interface = DB()
        self.guildnameField = TextInput(label="Name of the guild")
        self.descriptionField = TextInput(label="Description of the guild")
        self.guildEmblemField = TextInput(label="URL to guild emblem")
        self.guildHouseField = TextInput(label="URL to guild house image")
        self.add_item(self.guildnameField)
        self.add_item(self.descriptionField)
        self.add_item(self.guildEmblemField)
        self.add_item(self.guildHouseField)

    async def callback(self, interaction: nextcord.Interaction):
        guild = interaction.guild
        #Verhindern der erstellung von zwei odern mehreren gleichen guilden
        #so wie das verhindern des doppelten leaders
        l = self.Interface.get_all_leaders()
        if l != [] and l != None:
            for i in l:
                if str(interaction.user) in i:
                    await interaction.send("You already have an guild delete it to create a new one",ephemeral=True)
                    return
        category = await guild.create_category(self.guildnameField.value)        
        channelv = await guild.create_voice_channel(f"{self.guildnameField.value} Voice channel",category=category)
        channelt = await guild.create_text_channel(f"{self.guildnameField.value} Text channel",category=category)
        self.Interface.create_guild(name=self.guildnameField.value,
            leader=str(interaction.user),
            emblem=self.guildEmblemField.value,
            house=self.guildHouseField.value,
            voicechannel=str(channelv.id),
            textchannel=str(channelt.id),
            category=str(category.id))

        player:Player = self.Interface.load_player(str(interaction.user))
        player.guild=self.guildnameField.value
        self.Interface.store_player(player)
        await interaction.send(f"Du bist jetzt der Anführer der Guilde {self.guildnameField.value}",ephemeral=True)


class Create_Guild_Button(Button):
    def __init__(self):
        super().__init__(label = "Create Guild")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(Create_Guild_Modal())

class Create_Guild_View(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Create_Guild_Button())