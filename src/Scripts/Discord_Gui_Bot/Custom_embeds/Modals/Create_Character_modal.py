from nextcord import TextInputStyle
from src.Scripts.Discord_Gui_Bot.Custom_embeds.stats_embed import stats_embed
from src.Scripts.Classes.Assets_loader.asset_loader import *
from src.Scripts.Classes.Informations.informations import Informations
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Classes.Stats.player_stat import Stat
from src.Scripts.Functions.logger import log
from src.Scripts.Classes.Database.db import DB
import nextcord
from nextcord.ui import Modal,Select,TextInput,View


class Race_Select(Select):
    def __init__(self,viewM, custom_id: str = ..., placeholder = None, min_values: int = 1, max_values: int = 1) -> None:
        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values)
        self.Al = Asset_Loader()
        self.viewM = viewM        
        self.raceSelect=Select(custom_id="Modal:Race:Select")
        r = self.Al.load_races()   
        for key in r:
            self.add_option(label=key,value=key,description="More details are in the !races comand")
    
    async def callback(self, interaction: nextcord.Interaction):
        self.viewM.rasse = self.values[0]

class Class_Select(Select):
    def __init__(self,viewM, custom_id: str = ..., placeholder = None, min_values: int = 1, max_values: int = 1) -> None:
        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values)
        self.Al = Asset_Loader()
        self.viewM = viewM        
        self.raceSelect=Select(custom_id="Modal:Classes:Select")
        r = self.Al.load_p_classes()   
        for key in r:
            self.add_option(label=key,value=key,description="More details are in the !classes comand")
    
    async def callback(self, interaction: nextcord.Interaction):
        self.viewM.classp = self.values[0]


class Character_Create_Buttone(nextcord.ui.Button):
    def __init__(self,viewM, label: str = "Character essentials"):
        super().__init__(label=label)
        self.viewM = viewM

    async def callback(self, interaction: nextcord.Interaction):
        modal = Create_Character_Modal(viewM = self.viewM)
        await interaction.response.send_modal(modal)

class Character_Create_Buttono(nextcord.ui.Button):
    def __init__(self,viewM, label: str = "Character options"):
        super().__init__(label=label)
        self.viewM = viewM

    async def callback(self, interaction: nextcord.Interaction):
        modal = Create_Character_Modal2(viewM = self.viewM)
        await interaction.response.send_modal(modal)

class Character_Create_Button(nextcord.ui.Button):
    def __init__(self,viewM, label: str = "Create character"):
        super().__init__(label=label)
        self.data = viewM

    async def callback(self, interaction: nextcord.Interaction):
        self.Al = Asset_Loader()
        self.Interface = DB()
        p = Player(name=str(interaction.user.name),
            character_name=self.data.name,
            information=Informations(story=self.data.story,
                looks=self.data.looks,
                p_class=self.data.classp,
                gender=self.data.gender,
                race=self.data.rasse,
                img= self.data.img if self.data.name != None else "" ,
                age=self.data.age,
                height=self.data.height,
                specials=self.data.specials),
            stats=Stat(**self.Al.load_stats(self.data.classp,self.data.rasse)))

        self.Interface.create_character(p)
        log(f"{interaction.message.author} hat einen Char erstellt Klasse:{self.data.classp},Rasse:{self.data.rasse},Gender:{self.data.gender}")
        await interaction.send(f"Spieler {interaction.user.name} wurde registriert")



class Create_Character_View(View):
    def __init__(self, timeout= None):
        super().__init__(timeout=timeout)
        self.name=None
        self.age = None
        self.height = None
        self.specials = None
        self.story = None
        self.gender = None
        self.look = None
        self.img = None
        self.classp = None
        self.rasse = None
        self.add_item(Character_Create_Buttone(self))
        self.add_item(Character_Create_Buttono(self))
        self.add_item(Race_Select(viewM=self))
        self.add_item(Class_Select(viewM=self))
        self.add_item(Character_Create_Button(viewM=self))

class Create_Character_Modal(Modal):
    def __init__(self,viewM, title: str="Create your character", timeout:float = None, custom_id: str = "Modal:Create_Character", auto_defer: bool = True):
        super().__init__(title, timeout=timeout, custom_id=custom_id, auto_defer=auto_defer)
        self.viewM =viewM
        self.nameField=TextInput(label="Character name",max_length=20,required=True)
        self.ageField=TextInput(label="Character age",max_length=4,required=True)
        self.heightField=TextInput(label="Character height",max_length=3,required=True)
        self.specialsField=TextInput(label="Character specials",style=TextInputStyle.paragraph,max_length=100,required=False)
        self.storyField=TextInput(label="Character story",style=TextInputStyle.paragraph,max_length=400,required=False)

        self.add_item(self.nameField)
        self.add_item(self.ageField)
        self.add_item(self.heightField)
        self.add_item(self.specialsField)
        self.add_item(self.storyField)

    async def callback(self, interaction: nextcord.Interaction):
        self.viewM.name = self.nameField.value
        self.viewM.age = int(self.ageField.value)
        self.viewM.height=float(self.heightField.value)
        self.viewM.specials=self.specialsField.value
        self.viewM.story = self.storyField.value        


class Create_Character_Modal2(Modal):
    def __init__(self,viewM, title: str="Create your character", timeout:float = None, custom_id: str = "Modal:Create_Character:2", auto_defer: bool = True):
        super().__init__(title, timeout=timeout, custom_id=custom_id, auto_defer=auto_defer)
        self.viewM = viewM
                
        self.genderField=TextInput(label="Character gender",style=TextInputStyle.short,max_length=20,required=True)
        self.looksField=TextInput(label="Character looks",style=TextInputStyle.paragraph,max_length=200,required=False)
        self.imgField=TextInput(label="Character image url",style=TextInputStyle.short,max_length=1000,required=False)

        #self.classSelect=Select(custom_id="Modal:Classes:Select")
        #r = self.Al.load_p_classes()   
        #for key in r:
        #    self.classSelect.add_option(label=key,value=key,description="More details are in the !classes comand")
        #
        
        #self.add_item(self.classSelect)
        self.add_item(self.genderField)
        #self.add_item(self.raceSelect)
        self.add_item(self.looksField)
        self.add_item(self.imgField)

    async def callback(self, interaction: nextcord.Interaction):
        self.viewM.gender = self.genderField.value
        self.viewM.looks = self.looksField.value
        self.viewM.img = self.imgField.value

