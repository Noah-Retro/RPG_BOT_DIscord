"""
Erstellt von Noah Schneider
abgesegnet am 15.10.2021
Version 1.0

Alle bot commands für das erstellen eines character und den dazugeörigen Informationen 
"""
from discord import SlashOption, slash_command
from src.Scripts.Discord_Gui_Bot.Custom_embeds.stats_embed import stats_embed
from src.Scripts.Classes.Assets_loader.asset_loader import *
from src.Scripts.Classes.Informations.informations import Informations
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Classes.Stats.player_stat import Stat
from src.Scripts.Functions.logger import log
from src.Scripts.Classes.Database.db import DB
from nextcord.ext import commands
import nextcord
from nextcord import slash_command
import validators

class character(commands.Cog):
    """Alles was man zum erstellen eines Characters braucht"""
    def __init__(self,bot):
        self.bot=bot
        self.Interface = DB()
        self.Al = Asset_Loader()

    @slash_command(name='create_character',description='Erstellt ein character.')
    async def create_character(self,interaction:nextcord.Interaction,_character_name:str,_alter:int,_grösse:float,_besonderheiten:str,story:str,gender:str,img_url:str=SlashOption(name="image_url",required=False),aussehen:str=SlashOption(name="aussehen",required=False)):
        """Erzeugt ein Spieler in der Datenbank. Man kann nach dem erstellen alle funktionen nutzen.
        Alle Werte welche ein Leerzeichen enthalten müssen in Anführungszeichen stehen.
        z.B. "Vorname Nachname"
        z.B. "Irgend eine Story welche ziemlich lange sein kann"

        Args:
            _character_name (str): Name des Characters
            _alter (int): Alter des Characters
            _grösse (float): Grösse des Characters
            _besonderheiten (str): Merkmale des Characters -> Aussehen, Perönlichkeit, etc.
            _class (str): Name einer der Klassen die hinterlegt sind in dem !classes command.
            story (str): Die Hintergrundgeschichte deines charakters.
            gender (str): Alles was du sein möchtest.
            rasse (str): Eine der Hinterlegten Rassen im !rassen command.
            img_url(str, optional): Ein Bild daas deinen Charakter wieder spiegelt. Defaults to None
            aussehen (str, optional): Das Aussehen deines Charakters in Worten gefasst. Defaults to None.
        Extra:
            Es kann ein Bild hinzugefügt werden das deinen Character wieder Spiegelt. Man muss dazu den command als Kommentar bei einem bild hinschreiben, dass man hoch lädt
        """
        if not validators.url(img_url):     
            await interaction.send("img_url must end with .jpg or .png")
            return   
        p = Player(name=str(interaction.user),
            character_name=_character_name,
                story=story,
                looks=aussehen,
                p_class=None,
                gender=gender,
                race=None,
                img= img_url ,
                age=_alter,
                height=_grösse,
                specials=_besonderheiten,
                )

        
        await interaction.send(f"Wähle noch eine Klasse und eine Rasse aus",view=Select_View(p))
        

    @commands.command(name='rassen',brief='Zeig alle verfügbaren Rassen')
    async def rassen(self,ctx):
        """Dieser Command zeigt alle verfügbaren Rassen und deren ihre basis Stats.
        HINWEIS: Die Stats der Klasse und der Rasse werden zusammen gerechnet.
        Wen du dir nicht sicher bist was gut zusammen passt, benutze den Command !stats"""

        e = nextcord.Embed()
        r = self.Al.load_races()
              
        for key in r:
            c=""
            for i in r[key]:
                c += f"**{i}:** {r[key][i]}\n"

            e.add_field(name=key,value=c)
        await ctx.send(embed=e)

    @commands.command(name='klassen',brief='Zeig alle verfügbaren Klassen')
    async def klasse(self,ctx):
        """Dieser Command zeigt alle verfügbaren Klassen und deren ihre basis Stats.
        HINWEIS: Die Stats der Klasse und der Rasse werden zusammen gerechnet.
        Wen du dir nicht sicher bist was gut zusammen passt, benutze den Command !stats"""

        e = nextcord.Embed()
        r = self.Al.load_p_classes()
              
        for key in r:
            c=""
            for i in r[key]:
                c += f"**{i}:** {r[key][i]}\n"

            e.add_field(name=key,value=c)
        await ctx.send(embed=e)

    #@commands.command(name='stats_choice',brief='Zeigt die Stats bei einer Rasse und Klasse Wahl')
    #async def stats(self,ctx,rasse:str,klasse:str):
    #    """Dieser Command zeigt die Stats einer Klasse und einer Rasse an
#
    #    Args:
    #        rasse(str): Rassen Name
    #        klasse(str): Klassen Name
    #    """
    #    s = self.Al.load_stats(klasse,rasse)
    #    log(1,f"{ctx.message.author} hat stats_info für {rasse}/{klasse}")
    #    e=nextcord.Embed()
    #    e.add_field(name="Stats info",value=f"""
    #    **deff:** {s["deff"]}
    #    **atk:** {s["atk"]}
    #    **stamina:** {s["stamina"]}
    #    **trading:** {s["trading"]}
    #    **sneak:** {s["sneak"]}
    #    **cook:** {s["cook"]}
    #    **health:** {s["health"]}
    #    **mana:** {s["mana"]}
    #    **craft:** {s["craft"]}""")
    #    log(1,f"{ctx.message.author} hat stats_info aufgerufen")
    #    await ctx.send(embed=e)

    @commands.command(name="info_stats",brief="Zeigt was alle Stats macht")
    async def info_stats(self,ctx):
        """Zeig die Informationen zu den einzelnen Skills"""
        e = nextcord.Embed()
        e.add_field(name="Stats info",value="""
        **deff:** Der Defensiev wert des Spielers.
        **atk:** Der Angrifswert eines Spielers.
        **stamina:** Die Ausdauer eines Spielers. Wieviele Angriffe er ausführen kann.
        **trading:** Der trading Stat verschaft einen immer grösser werdenden Rabat auf None Player Trades.
        **sneak:** Der Wert erhöht die warscheinlichkeit sich bei einem Gegner vorbei zu schleichen.
        **cook:** Um so höher um so bessere Koch rezepte können gekocht werden
        **health:** Das basis Leben eines Spielers
        **mana:** Wie viele Zauber ein Spieler benutzen kann
        **craft:** Kann immer wie schwerere rezepte craften""")
        log(1,f"{ctx.message.author} hat stats_info aufgerufen")
        await ctx.send(embed= e)



class ClassSelect(nextcord.ui.Select):
    def __init__(self,player) -> None:
        super().__init__(placeholder="Wähle eine Klasse aus!")
        al = Asset_Loader()
        classes = al.load_p_classes()
        for key in classes:
            self.add_option(label=key,value=key,description=classes[key]["description"][0:90] if len(classes[key]["description"])>90 else classes[key]["description"])
        self.player = player

    async def callback(self, interaction: nextcord.Interaction):
        self.player.p_class = self.values[0]
        Al = Asset_Loader()
        if self.player.race != None and self.player.race != "":
            db = DB()
            self.player.add_stats(**Al.load_stats(self.player.p_class,self.player.race))

            db.create_character(self.player)
            await interaction.send("Charakter wurde erstellt")
        await interaction.edit(view=Select_View(self.player))
            
class RaceSelect(nextcord.ui.Select):
    def __init__(self,player:Player) -> None:
        super().__init__(placeholder="Wähle eine Rasse aus!")
        al = Asset_Loader()
        classes = al.load_races()
        for key in classes:
            self.add_option(label=key,value=key,description=classes[key]["description"][0:90] if len(classes[key]["description"])>90 else classes[key]["description"])
        self.player = player

    async def callback(self, interaction: nextcord.Interaction):
        self.player.race = self.values[0]
        Al = Asset_Loader()
        if self.player.p_class != None and self.player.p_class != "":
            db = DB()
            self.player.add_stats(**Al.load_stats(self.player.p_class,self.player.race))

            db.create_character(self.player)
            await interaction.send("Charakter wurde erstellt")
        await interaction.edit(view=Select_View(self.player))
     
class Select_View(nextcord.ui.View):
    def __init__(self,player):
        super().__init__()
        self.add_item(ClassSelect(player))
        self.add_item(RaceSelect(player))
