from nextcord.ext import commands
import nextcord
from nextcord import slash_command,SlashOption
from src.Scripts.Classes.Database.db import DB
from src.Scripts.Classes.Suggsetion.suggsetion import Suggsestion

class Suggsetion_Cog(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.__cog_name__="Suggsetions"
        self.Interface=DB()

    @slash_command(name="suggsetion",description="Mach einen vorschlag für eine erweiterung oder eine Verbesserung des codes")
    async def suggsetion(self,interaction:nextcord.Interaction):
        pass

    @suggsetion.subcommand(name="item",description="Erstelle einen Vorschlag für ein Item")
    async def item(self,interaction:nextcord.Interaction,
    name=SlashOption(
        name="name",
        description="Wie das Item heissen soll",
        required=True        
    ),
    value=SlashOption(
        name="preis",
        description="Lege den wert des Items fest",
        required=True
    ),
    des=SlashOption(
        name="beschreibung",
        description="Hier kannst du das Item kurz bezeichnen",
        required=True        
    ),
    img=SlashOption(
        name="bild",
        description="Füge ein Bild zu dem Item dazu. Muss eine URL sein",
        required=False
    ),
    payed=SlashOption(
        name="payed",
        description="Bezahle den Vorschlag mit 5 Diamantcoins damit die Priorität höher ist",
        required=False,
        choices=["True","False"],
        default="False"
    )):
        data={
            "name":name,
            "value":value,
            "description":des,
            "img":img
        }
        if payed != "False":
            await interaction.send("Bezahlte Vorschläge sind noch nicht implementiert",ephemeral=True)
            return
        s=Suggsestion(type_="Item",player=str(interaction.user),data=str(data),payed=False)
        self.Interface.store_suggsetion(s)
        await interaction.send("Vorschlag wurde registriert und wird in kürze bearbeitet",ephemeral=True)

    @suggsetion.subcommand(name="recepie",description="Schlage ein Rezept vor")
    async def recepie(
        self,
        interaction:nextcord.Interaction,
        item=SlashOption(
            name="item",
            description="Wie  das Item für das Rezept heisst",
            required=True
        ),
        skill=SlashOption(
            name="skill",
            description="Das minimum Crafting skill level für das rezept",
            required=True
        ),
        items=SlashOption(
            name="items",
            description="Format muss 'Name des Items':'Menge',etc. sein dabei sind Name und Quantity fix Werte",
            required=True
        ),
        payed=SlashOption(
            name="payed",
            description="Bezahle den Vorschlag mit 5 Diamantcoins damit die Priorität höher ist",
            required=False,
            choices=["True","False"],
            default="False"
        )):
            if payed !="False":
                await interaction.send("Bezahlte Vorschläge sind noch nicht implementiert",ephemeral=True)
                return
            data={
                "Item":item,
                "skill":skill,
                "Items":items
            }
            s = Suggsestion(type_="Recepie",player=str(interaction.user),data=str(data),payed=payed)
            self.Interface.store_suggsetion(s)    
            await interaction.send("Vorschlag wurde registriert und wird in kürze bearbeitet",ephemeral=True)

    @suggsetion.subcommand(name="work",description="Schlage eine Arbeit vor")
    async def work(
        self,
        interaction:nextcord.Interaction,
        name=SlashOption(
            name="name",
            description="Name der Arbeit",
            required=True),
        items=SlashOption(
            name="items",
            description="Items die gedroped werden können. Format 'Itemname':'Dropchance',etc. dropchance zwishcen 0 und 1",
            required=True),
        level=SlashOption(
            name="level",
            description="Das minimum Level des Spielers für diese Arbeit",
            required=True),
        payed=SlashOption(
            name="payed",
            description="Bezahle den Vorschlag mit 5 Diamantcoins damit die Priorität höher ist",
            required=False,
            choices=["True","False"],
            default="False")           
        ):
            if payed !="False":
                await interaction.send("Bezahlte Vorschläge sind noch nicht implementiert",ephemeral=True)
                return
            data={
                "name":name,
                "items":items,
                "level":level,
            }
            s = Suggsestion(type_="Work",player=str(interaction.user),data=str(data),payed=payed)
            self.Interface.store_suggsetion(s)    
            await interaction.send("Vorschlag wurde registriert und wird in kürze bearbeitet",ephemeral=True)

    @suggsetion.subcommand(name="bounty",description="schlage ein Bounty vor")
    async def bounty(
        self,
        interaction:nextcord.Interaction,
        name=SlashOption(
            name="name", 
            description="Name des Bountys",
            required=True),
        level=SlashOption(
            name="level",
            description="Minimum Level des Spielers für das Bounty",
            required=True),
        task=SlashOption(
            name="task",
            description="Items die gesammelt werden müssen. 'Itemname':'quantity',etc.",
            required=True),
        reward_money=SlashOption(
            name="money",
            description="Geld welches dem Spieler gutgescrieben wird",
            required=True),
        reward_items=SlashOption(
            name="items",
            description="Items die der Spieler erhält. Format 'Itemname':'quantity',etc.",
            required=True),
        exp=SlashOption(
            name="exp",
            description="Erfahrungspunkt die der Spieler erhällt",
            required=True),
        payed=SlashOption(
            name="payed",
            description="Bezahle den Vorschlag mit 5 Diamantcoins damit die Priorität höher ist",
            required=False,
            choices=["True","False"],
            default="False")           
        ):
            if payed !="False":
                await interaction.send("Bezahlte Vorschläge sind noch nicht implementiert",ephemeral=True)
                return
            data={
                "name":name,
                "level":level,
                "task":task,
                "reward_money":reward_money,
                "reward_items":reward_items,
                "exp":exp
            }
            s = Suggsestion(type_="Bounty",player=str(interaction.user),data=str(data),payed=payed)
            self.Interface.store_suggsetion(s)    
            await interaction.send("Vorschlag wurde registriert und wird in kürze bearbeitet",ephemeral=True)

    @suggsetion.subcommand(name="weapon",description="Schlage eine neue Waffe vor")
    async def weapon(
        self,
        interaction:nextcord.Interaction,
        name=SlashOption(
            name="name",
            description="Name der Waffe",
            required=True
            ),
        value=SlashOption(
            name="value",
            description="Wert der Waffe",
            required=True),
        description=SlashOption(
            name="description",
            description="Beschreibung der Waffe",
            required=True),
        atk=SlashOption(
            name="atack",
            description="Der base Angrifswert der Waffe",
            required=True),
        img=SlashOption(
            name="image",
            description="Ein Bild der waffe. Muss eine URL sein",
            required=True),
        payed=SlashOption(
            name="payed",
            description="Bezahle den Vorschlag mit 5 Diamantcoins damit die Priorität höher ist",
            required=False,
            choices=["True","False"],            
            default="False")           
        ):
            if payed !="False":
                await interaction.send("Bezahlte Vorschläge sind noch nicht implementiert",ephemeral=True)
                return
            data={
                "name":name,
                "value":value,
                "description":description,
                "atk":atk,
                "img":img
            }
            s = Suggsestion(type_="Weapon",player=str(interaction.user),data=str(data),payed=payed)
            self.Interface.store_suggsetion(s)    
            await interaction.send("Vorschlag wurde registriert und wird in kürze bearbeitet",ephemeral=True)

    @suggsetion.subcommand(name="armor",description="Schlage eine neue Rüstung vor")
    async def armor(
        self,
        interaction:nextcord.Interaction,
        name=SlashOption(
            name="name",
            description="Name der Rüstung",
            required=True
            ),
        value=SlashOption(
            name="value",
            description="Wert der Rüstung",
            required=True),
        description=SlashOption(
            name="description",
            description="Beschreibung der Rüstung",
            required=True),
        deff=SlashOption(
            name="deffense",
            description="Der base Verteidigungswert der Rüstung",
            required=True),
        img=SlashOption(
            name="image",
            description="Ein Bild der Rüstung. Muss eine URL sein",
            required=True),
        payed=SlashOption(
            name="payed",
            description="Bezahle den Vorschlag mit 5 Diamantcoins damit die Priorität höher ist",
            required=False,
            choices=["True","False"],            
            default="False")           
        ):
            if payed !="False":
                await interaction.send("Bezahlte Vorschläge sind noch nicht implementiert",ephemeral=True)
                return
            data={
                "name":name,
                "value":value,
                "description":description,
                "deff":deff,
                "img":img
            }
            s = Suggsestion(type_="Rüstung",player=str(interaction.user),data=str(data),payed=payed)
            self.Interface.store_suggsetion(s)    
            await interaction.send("Vorschlag wurde registriert und wird in kürze bearbeitet",ephemeral=True)

    @suggsetion.subcommand(name="artefact",description="Schlage eine neue Artefakt vor")
    async def artefact(
        self,
        interaction:nextcord.Interaction,
        name=SlashOption(
            name="name",
            description="Name des Artefaktes",
            required=True
            ),
        value=SlashOption(
            name="value",
            description="Wert des Artefaktes",
            required=True),
        description=SlashOption(
            name="description",
            description="Beschreibung des Artefaktes",
            required=True),
        atk=SlashOption(
            name="attack",
            description="Der base Angriffswert des Artefaktes",
            required=True),
        deffens=SlashOption(
            name="deffense",
            description="Der base Verteidigungswert des Artefaktes",
            required=True),
        stamina=SlashOption(
            name="stamina",
            description="Der base Staminawert des Artefaktes",
            required=True),
        mana=SlashOption(
            name="deffense",
            description="Der base Manawert des Artefaktes",
            required=True),
        img=SlashOption(
            name="image",
            description="Ein Bild des Artefaktes. Muss eine URL sein",
            required=True),
        payed=SlashOption(
            name="payed",
            description="Bezahle den Vorschlag mit 5 Diamantcoins damit die Priorität höher ist",
            required=False,
            choices=["True","False"],            
            default="False")           
        ):
            if payed !="False":
                await interaction.send("Bezahlte Vorschläge sind noch nicht implementiert",ephemeral=True)
                return
            data={
                "name":name,
                "value":value,
                "description":description,
                "atk":atk,
                "deff":deffens,
                "stamina":stamina,
                "mana":mana,
                "img":img
            }
            s = Suggsestion(type_="Artefact",player=str(interaction.user),data=str(data),payed=payed)
            self.Interface.store_suggsetion(s)    
            await interaction.send("Vorschlag wurde registriert und wird in kürze bearbeitet",ephemeral=True)

    @suggsetion.subcommand(name="guild_reward",description="Schlage einen Guilden reward an einem bestimmten Level vor.")
    async def guild_reward(
        self,
        interaction:nextcord.Interaction,
        level=SlashOption(
            name="level",
            description="Bei welchem Level das Item gegeben werden soll",
            required=True
        ),
        item=SlashOption(
            name="item",
            description="Der Name des Items",
            required=True),
        payed=SlashOption(
            name="payed",
            description="Bezahle den Vorschlag mit 5 Diamantcoins damit die Priorität höher ist",
            required=False,
            choices=["True","False"],            
            default="False")           
        ):
            if payed !="False":
                await interaction.send("Bezahlte Vorschläge sind noch nicht implementiert",ephemeral=True)
                return

            data={
                "level":level,
                "item":item
            }
            s = Suggsestion(type_="Guild_Reward",player=str(interaction.user),data=str(data),payed=payed)
            self.Interface.store_suggsetion(s)    
            await interaction.send("Vorschlag wurde registriert und wird in kürze bearbeitet",ephemeral=True)

    @suggsetion.subcommand(name="klasse",description="Schlage eine neue Klasse vor")
    async def klasse(
        self,
        interaction:nextcord.Interaction,
        name=SlashOption(
            name="name",
            description="Name der Klasse",
            required=True
            ),
        description=SlashOption(
            name="description",
            description="Beschreibung der Klasse",
            required=True),
        atk=SlashOption(
            name="attack",
            description="Der base Angriffswert der Klasse",
            required=True),
        deffens=SlashOption(
            name="deffense",
            description="Der base Verteidigungswert der Klasse",
            required=True),
        stamina=SlashOption(
            name="stamina",
            description="Der base Staminawert der Klasse",
            required=True),
        mana=SlashOption(
            name="mana",
            description="Der base Manawert der Klasse",
            required=True),
        trading=SlashOption(
            name="trading",
            description="Der base Handelwert der Klasse",
            required=True),
        sneak=SlashOption(
            name="sneak",
            description="Der base Schleich der Klasse",
            required=True),
        cook=SlashOption(
            name="cook",
            description="Der base Kochenwert der Klasse",
            required=True),
        health=SlashOption(
            name="health",
            description="Das base Leben der Klasse",
            required=True),
        craft=SlashOption(
            name="craft",
            description="Der base Manawert der Klasse",
            required=True),
        knowledge=SlashOption(
            name="deffense",
            description="Der base Wissenswert der Klasse",
            required=True),
        img=SlashOption(
            name="image",
            description="Ein Bild der Klasse. Muss eine URL sein",
            required=True),
        payed=SlashOption(
            name="payed",
            description="Bezahle den Vorschlag mit 5 Diamantcoins damit die Priorität höher ist",
            required=False,
            choices=["True","False"],            
            default="False")           
        ):
            if payed !="False":
                await interaction.send("Bezahlte Vorschläge sind noch nicht implementiert",ephemeral=True)
                return

            data={
                "name":name,
                "description":description,
                "deff":deffens,
                "atk":atk,
                "stamina":stamina,
                "trading":trading,
                "sneak":sneak,
                "cook":cook,
                "health":health,
                "mana":mana,
                "craft":craft,
                "knowledge":knowledge,
                "img":img
            }
            s = Suggsestion(type_="Klass",player=f"{interaction.user} {interaction.user.id}",data=str(data),payed=payed)
            self.Interface.store_suggsetion(s)    
            await interaction.send("Vorschlag wurde registriert und wird in kürze bearbeitet",ephemeral=True)

    @suggsetion.subcommand(name="rasse",description="Schlage eine neue Klasse vor")
    async def rasse(
        self,
        interaction:nextcord.Interaction,
        name=SlashOption(
            name="name",
            description="Name der Rasse",
            required=True
            ),
        description=SlashOption(
            name="description",
            description="Beschreibung der Rasse",
            required=True),
        atk=SlashOption(
            name="attack",
            description="Der base Angriffswert der Rasse",
            required=True),
        deffens=SlashOption(
            name="deffense",
            description="Der base Verteidigungswert der Rasse",
            required=True),
        stamina=SlashOption(
            name="stamina",
            description="Der base Staminawert der Rasse",
            required=True),
        mana=SlashOption(
            name="mana",
            description="Der base Manawert der Rasse",
            required=True),
        trading=SlashOption(
            name="trading",
            description="Der base Handelwert der Rasse",
            required=True),
        sneak=SlashOption(
            name="sneak",
            description="Der base Schleich der Rasse",
            required=True),
        cook=SlashOption(
            name="cook",
            description="Der base Kochenwert der Rasse",
            required=True),
        health=SlashOption(
            name="health",
            description="Das base Leben der Rasse",
            required=True),
        craft=SlashOption(
            name="craft",
            description="Der base Manawert der Rasse",
            required=True),
        knowledge=SlashOption(
            name="deffense",
            description="Der base Wissenswert der Rasse",
            required=True),
        img=SlashOption(
            name="image",
            description="Ein Bild der Rasse. Muss eine URL sein",
            required=True),
        payed=SlashOption(
            name="payed",
            description="Bezahle den Vorschlag mit 5 Diamantcoins damit die Priorität höher ist",
            required=False,
            choices=["True","False"],            
            default="False")           
        ):
            if payed !="False":
                await interaction.send("Bezahlte Vorschläge sind noch nicht implementiert",ephemeral=True)
                return

            data={
                "name":name,
                "description":description,
                "deff":deffens,
                "atk":atk,
                "stamina":stamina,
                "trading":trading,
                "sneak":sneak,
                "cook":cook,
                "health":health,
                "mana":mana,
                "craft":craft,
                "knowledge":knowledge,
                "img":img
            }
            s = Suggsestion(type_="Rasse",player=f"{interaction.user} {interaction.user.id}",data=str(data),payed=payed)
            self.Interface.store_suggsetion(s)    
            await interaction.send("Vorschlag wurde registriert und wird in kürze bearbeitet",ephemeral=True)

    #GameMechanics MODAL?
    
    
    
    #Spells
    #Attack
    #Markets
    #Enemys


    #@suggsetion.subcommand(name="help",description="Zeigt dir die Hilfe für diese Befehle an")
    #async def help(self,interaction:nextcord.Interaction):
    #    r=""
    #    e=nextcord.Embed()
    #    for c in self.bot.get_all_application_commands():
    #        if c.name=="suggsetion":
    #            e.title=c.name
    #            for s in c.children:
    #                r+=f"   **Description**: {c.children[s].description}\n"
    #                for o in c.children[s].options:
    #                    r+=f"       **{c.children[s].options[o].name}**: {c.children[s].options[o].description}\n"
    #                    #r+=f"          **Choices**: {c.children[s].options[o].choices if c.children[s].options[o].choices != '...' else 'None' }\n"
    #                    
    #                if len(r)>1024:
    #                    e.add_field(name=f"__{c.children[s].name}__",value=r[0-1024],inline=False)
    #                else:
    #                    e.add_field(name=f"__{c.children[s].name}__",value=r,inline=False)
    #                r=""
    #    await interaction.send(embed=e,ephemeral=True)


            