from nextcord.ext import commands
import nextcord
from src.Scripts.Classes.Items.base_item import Base_Item
from src.Scripts.Classes.Items.base_recepie import Base_Recepie
from src.Scripts.Discord_Gui_Bot.Custom_embeds.item_list_embed import item_list_embed
from src.Scripts.Discord_Gui_Bot.Custom_embeds.rezpie_embed import Rezept_embed

from src.Scripts.Classes.Database.db import DB
from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader

class Recepie_Embed(nextcord.Embed):
    def __init__(self,recepie:Base_Recepie,pagenumber,playername:str):
        self.recepie = recepie
        self.pagenumber=pagenumber
        self.al=Asset_Loader()
        self.interface = DB()
        self.player=self.interface.load_player(playername)
        super().__init__(colour=nextcord.Colour.blurple(), color=nextcord.Color.blurple(), title="Rezepie book")
        
        if recepie == None:
            recepies=self.al.load_all_recepies()
            for i in recepies:
                if self.player.craft >= i.skill:
                    self.add_field(name=i.item.name,value="-----------")
            return
        if recepie.skill > self.player.craft:
            self.add_field(name="Reducted!",value="Get more crafting skill")
            return
        self.set_footer(text=f"page:{pagenumber}/{len(self.al.load_all_recepies())-1}")
        s=""
        for i in recepie.items:
            s+=f'{i.quantity}x{i.name}\n'
        self.add_field(name=recepie.item.name,value=s+f'Craft Skill: {recepie.skill}')
        if recepie.item.img !="":
            self.set_thumbnail(url=recepie.item.img)
            

class Next_Page_Button(nextcord.ui.Button):
    def __init__(self,pagenumber,label = "Next page"):
        super().__init__(label=label)
        self.Al = Asset_Loader()
        self.recepies = self.Al.load_all_recepies()
        self.pagenumber = pagenumber

    async def callback(self, interaction: nextcord.Interaction):
        self.pagenumber += 1
        if self.pagenumber > len(self.recepies)-1:
            self.pagenumber=0
        await interaction.edit(embed=Recepie_Embed(self.recepies[self.pagenumber],self.pagenumber,str(interaction.user)),view=Recepie_View(self.pagenumber))

class Prev_Page_Button(nextcord.ui.Button):
    def __init__(self,pagenumber,label = "Previous page"):
        super().__init__(label=label)
        self.Al = Asset_Loader()
        self.recepies = self.Al.load_all_recepies()
        self.pagenumber = pagenumber

    async def callback(self, interaction: nextcord.Interaction):
        self.pagenumber -= 1
        if self.pagenumber < 0:
            self.pagenumber=len(self.recepies)-1
        await interaction.edit(embed=Recepie_Embed(self.recepies[self.pagenumber],self.pagenumber,str(interaction.user)),view=Recepie_View(self.pagenumber))

class Craft_Recepie_Button(nextcord.ui.Button):
    def __init__(self,pagenumber,label = "Craft recepie"):
        super().__init__(label=label)
        self.Al = Asset_Loader()
        self.Interface = DB()
        self.recepies = self.Al.load_all_recepies()
        self.pagenumber = pagenumber

    async def callback(self, interaction: nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        if ph.craft < self.recepies[self.pagenumber].skill:
            return
        if ph.craft_item(self.recepies[self.pagenumber]):
            await interaction.send(f"{self.recepies[self.pagenumber].item.name} wurde gecrafted.",ephemeral=True)
            self.Interface.store_player(ph)
        else:
            await interaction.send(f"Überprüfe nochmals ob du alle Items für das Rezept hast.",ephemeral=True)



class Recepie_View(nextcord.ui.View):
    def __init__(self,pagenumber:int=None):
        if pagenumber == None:
            self.pagenumber = -1
        else:
            self.pagenumber=pagenumber
        super().__init__()
        self.add_item(Prev_Page_Button(self.pagenumber))
        self.add_item(Craft_Recepie_Button(self.pagenumber))
        self.add_item(Next_Page_Button(self.pagenumber))
