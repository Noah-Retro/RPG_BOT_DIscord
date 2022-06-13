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

class character(commands.Cog):
    """Alles was man zum erstellen eines Characters braucht"""
    def __init__(self,bot):
        self.bot=bot
        self.Interface = DB()
        self.Al = Asset_Loader()

    @slash_command(name='create_character',description='Erstellt ein character.')
    async def create_character(self,interaction:nextcord.Interaction,_character_name:str,_alter:int,_grösse:float,_besonderheiten:str,_class:str,story:str,gender:str,rasse:str,img_url:str=SlashOption(name="image_url",required=False),aussehen:str=SlashOption(name="aussehen",required=False)):
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
        if not img_url.endswith((".jpg",".png")) and img_url != None:     
            await interaction.send("img_url must end with .jpg or .png")   
        p = Player(name=str(interaction.user),
            character_name=_character_name,
                story=story,
                looks=aussehen,
                p_class=_class,
                gender=gender,
                race=rasse,
                img= img_url ,
                age=_alter,
                height=_grösse,
                specials=_besonderheiten,
                **self.Al.load_stats(_class,rasse))

        self.Interface.create_character(p)
        log(f"{interaction.user} hat einen Char erstellt Klasse:{_class},Rasse:{rasse},Gender:{gender}")
        await interaction.send(f"Spieler {interaction.user} wurde registriert")
        

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
