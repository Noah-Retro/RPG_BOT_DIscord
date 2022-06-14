import nextcord
from discord import slash_command
from flask import flash
from nextcord.embeds import Embed
from nextcord.types.components import ButtonStyle
from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader
from src.Scripts.Classes.Bounty.bounty import Bounty
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Classes.Database.db import DB
from src.Scripts.Classes.Items.Armors.armor import Armor
from src.Scripts.Classes.Items.Artefacts.artefact import Artefact
from src.Scripts.Classes.Items.base_item import Base_Item
from src.Scripts.Classes.Items.Potions.potions import Potion
from src.Scripts.Classes.Items.Weapons.weapon import Weapon
from src.Scripts.Classes.Trade.trade import Trade
from src.Scripts.Discord_Gui_Bot.Custom_embeds.character_embed import \
    character_embed
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.stats_field import \
    Stats_field


def stats_embed(player:Player)->nextcord.Embed:
    color=nextcord.Color.default()
    if player.color!=None:
        color=player.color
    e = nextcord.Embed(title="Stats from your character",color=color)
    e.add_field(name="Skilltoken",value=f"Your skilltokens: {player.skill_tokens}")
    embed = Stats_field(e,s = player)
    return embed

def item_embed(item:Base_Item):
    al = Asset_Loader()
    e = nextcord.Embed(title=f"{item.name}x{item.quantity}",
                       description="Genaue beschreibung des Items")
    e.add_field(name="Beschreibung",value=f"{item.description}")
    if item.img !="":
        e.set_thumbnail(url=item.img)
    r = al.load_recepie(item.name)
    rs=""
    if r !=None:
        for i in r.items:
            rs+=f"{i.name}x{i.quantity}"
        rs+=f"\nskill:{r.skill}"
        e.add_field(name="Rezept",value=rs)
        r=True
        return e,r
    r=False
    return e,r

def trade_embed(trade:Trade):
    e=nextcord.Embed(title=trade.item.name)
    e.add_field(name=trade.item.name,value=f"""
                {trade.item.name}x{trade.item.quantity}
                {trade.price}$
                open since: {trade.time}
                trade closed: {trade.done}""")
    e.set_thumbnail(url=trade.item.img)
    return e

def bounty_embed(bounty:Bounty):
    ri = ""
    e = nextcord.Embed(title=bounty.name)
    for i in bounty.reward_items:
        ri+=i.name
        ri+=", "
    e.add_field(name="Details",value=f"reward items:{ri}\nreward money: {bounty.reward_money}$\ntask to complete:{bounty.task}\ntask progress: {bounty.done_items}")
    return e

class Show_Poststelle(nextcord.ui.Button):
    def __init__(self,p:Player):
        super().__init__(style=nextcord.ButtonStyle.blurple, label=f"show_Poststelle", disabled=False, custom_id=f"Inventory:Button:Show_Poststelle")

    async def callback(self,interaction:nextcord.Interaction):
        await interaction.send("Noch nicht implementiert. Hier kannst du bald alle deine Items sehen welche die Limite von 25 übersteigen",ephemeral=True)


class Craft_Item_Button(nextcord.ui.Button):
    def __init__(self,i:Base_Item):
        self.i = i
        self.Interface= DB()
        self.Al=Asset_Loader()
        super().__init__(style=nextcord.ButtonStyle.green, label=f"Craft: {i.name}", disabled=False, custom_id=f"Inventory:Button:{i.name}")

    async def callback(self, interaction: nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        if ph.craft_item(self.Al.load_recepie(self.i.name)):
            await interaction.send(f"{self.i.name} wurde gecrafted.",ephemeral=True)
            self.Interface.store_player(ph)
        else:
            await interaction.send(f"Überprüfe nochmals ob du alle Items für das Rezept hast.",ephemeral=True)

class Delete_Item_Button(nextcord.ui.Button):
    def __init__(self,i:Base_Item):
        self.i = i
        self.Interface= DB()
        self.Al=Asset_Loader()
        super().__init__(style=nextcord.ButtonStyle.red,
                        label=f"DELETE: {i.name}",
                        disabled=False,
                        custom_id=f"Inventory:Button_Delete:{i.name}")
       
    async def callback(self, interaction: nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        if ph.remove_item(self.i.name,1):
             await interaction.send(f"{self.i.name} wurde gelöscht.",ephemeral=True)
        else:
            await interaction.send(f"Überprüfe nochmals, ob du das Item überhaubt besitzt.",ephemeral=True)
        self.Interface.store_player(ph)
   
class Open_Trade_Button(nextcord.ui.Button):
    def __init__(self,i:Base_Item):
        self.i = i
     
        super().__init__(style=nextcord.ButtonStyle.blurple,
                         label=f"Open a Trade",
                         custom_id=f"Inventory:Button:Trade:{i.name}")   

    async def callback(self,interaction:nextcord.Interaction):
        await interaction.response.send_modal(Create_Trade_Modal(self.i))


class Create_Trade_Modal(nextcord.ui.Modal):
    def __init__(self,i:Base_Item, title: str=None, *, timeout = None, custom_id: str = f"Inventory:Modal:Trade", auto_defer: bool = True):
        super().__init__(title=i.name, timeout=timeout, custom_id=custom_id, auto_defer=auto_defer)
        self.i = i
        self.Interface= DB()
        self.Al=Asset_Loader()
        self.quantityField = nextcord.ui.TextInput(label="Quantity:",default_value="10",required=True,custom_id="Inventory:Modal:TextInput:Quantity")
        self.priceField = nextcord.ui.TextInput(label="Price:",default_value="100",required=True,custom_id="Inventory:Modal:TextInput:Price")
        self.add_item(self.quantityField)
        self.add_item(self.priceField)

    async def callback(self, interaction: nextcord.Interaction):
        ph:Player = self.Interface.load_player(str(interaction.user))
        self.quantity = int(self.quantityField.value)
        self.price = int(self.priceField.value)
        self.i.quantity= self.quantity
        if ph.open_trade(Trade(item=self.i,price=self.price,public=True)):
            e = nextcord.Embed()
            e.add_field(name="**Trade**",value=f"Ein trade mit {self.quantity}x{self.i.name} für {self.price}$ wurde erstellt")
            await interaction.send(embed=e,ephemeral=True)
        else:
            await interaction.send("Überprüfe ob du genügend von dem Item hast",ephemeral=True)
        self.Interface.store_player(ph)
        


class Unequip_Armor_Button(nextcord.ui.Button):
    def __init__(self):
        self.Interface= DB()
        self.Al=Asset_Loader()
        super().__init__(style=nextcord.ButtonStyle.gray, label="Unequip your armor", custom_id="Inventory:Unequip:Armor:Button")
         
    async def callback(self, interaction: nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        ph.unequip_armor()
        await interaction.edit(embed=character_embed(interaction,ph),view=Inventory_View(ph))
        self.Interface.store_player(ph)

class Unequip_Weapon_Button(nextcord.ui.Button):
    def __init__(self):
        self.Interface= DB()
        self.Al=Asset_Loader()
        super().__init__(style=nextcord.ButtonStyle.gray, label="Unequip your weapon", custom_id="Inventory:Unequip:Weapon:Button")
    
    async def callback(self, interaction: nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        ph.unequip_weapon()
        self.Interface.store_player(ph)
        await interaction.edit(embed=character_embed(interaction,ph),view=Inventory_View(ph))
        self.Interface.store_player(ph)

class Unequip_Artefact_Button(nextcord.ui.Button):
    def __init__(self):
        self.Interface= DB()
        self.Al=Asset_Loader()
        super().__init__(style=nextcord.ButtonStyle.gray, label="Unequip your artefact", custom_id="Inventory:Unequip:Artefact:Button")
    
    async def callback(self, interaction: nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        ph.unequip_artefact()
        self.Interface.store_player(ph)
        await interaction.edit(embed=character_embed(interaction,ph),view=Inventory_View(ph))
        self.Interface.store_player(ph)

class Equip_Armor_Button(nextcord.ui.Button):
    def __init__(self,i:Base_Item):
        self.i = i
        self.Interface= DB()
        self.Al=Asset_Loader()
        super().__init__(style=nextcord.ButtonStyle.gray, label="Equip armor", custom_id="Inventory:Equip:Armor:Button")
    async def callback(self,interaction:nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        if ph.equip_armor(self.i):
           await interaction.edit(embed=character_embed(interaction,ph),view=Inventory_View(ph))
        self.Interface.store_player(ph)

class Equip_Weapon_Button(nextcord.ui.Button):
    def __init__(self,i:Base_Item):
        self.i = i
        self.Interface= DB()
        self.Al=Asset_Loader()
        super().__init__(style=nextcord.ButtonStyle.gray, label="Equip weapon", custom_id="Inventory:Equip:Weapon:Button")
    
    async def callback(self,interaction:nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        if ph.equip_weapon(self.i):
            await interaction.edit(embed=character_embed(interaction,ph),view=Inventory_View(ph))
        self.Interface.store_player(ph)

class Equip_Artefact_Button(nextcord.ui.Button):
    def __init__(self,i:Base_Item):
        self.i = i
        self.Interface= DB()
        self.Al=Asset_Loader()
        super().__init__(style=nextcord.ButtonStyle.gray, label="Equip artefact", custom_id="Inventory:Equip:Artefact:Button")
    
    async def callback(self,interaction:nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        if ph.equip_artefact(self.i):
            await interaction.edit(embed=character_embed(interaction,ph),view=Inventory_View(ph))
        self.Interface.store_player(ph)

class Use_Item_Button(nextcord.ui.Button):
    def __init__(self,i:Base_Item):
        self.i = i
        self.Interface= DB()
        self.Al=Asset_Loader()
        super().__init__(style=nextcord.ButtonStyle.gray, label="Use Item", custom_id="Inventory:Use:Item:Button")
    
    async def callback(self,interaction:nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        if ph.heal(self.i):
            self.i.quantity -=1
            await interaction.edit(embed=character_embed(interaction,ph),view=Inventory_View(ph))
            if self.i.quantity >0:
                await interaction.edit(embed=item_embed(self.i)[0])
            else:
                await interaction.edit(content="Kein Item mehr vorhanden",embed=None,view=None)#content="Du hast keines dieses Item im Inventar",embed=None,view=None)
            self.Interface.store_player(ph)
            return
        


class Delete_Trade_Button(nextcord.ui.Button):
    def __init__(self,t:Trade):
        self.t = t
        self.Interface= DB()
        super().__init__(style=nextcord.ButtonStyle.red, label="Delete Trade", custom_id="Inventory:Trade:Delete:Button:{t.item.name}")
     
    async def callback(self, interaction: nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        ph.remove_trade(self.t)
        self.Interface.store_player(ph) 
        await interaction.send("Ein trade wurde zurück genommen",ephemeral=True)
         
class Remove_Bounty_Button(nextcord.ui.Button):
    def __init__(self,b:Bounty):
        self.b = b
        self.Interface= DB()
        super().__init__(style=nextcord.ButtonStyle.primary, label="Remove", custom_id="Inventory:Bounty:Remove:Button:{b.name}")

    async def callback(self, interaction: nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        if self.b.worked_on == True:
            return
        ph.remove_bounty(self.b)
        await interaction.send(f'Bounty {self.b.name} wurde entfernt',ephemeral=True)
        self.Interface.store_player(ph)

class Complete_Bounty_Button(nextcord.ui.Button):
    def __init__(self,b:Bounty):
        self.b = b
        self.Interface= DB()
        super().__init__(style=nextcord.ButtonStyle.green, label="Complete", custom_id="Inventory:Bounty:Complete:Button:{b.name}")       
        
    async def callback(self, interaction: nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        if ph.complete_bounty(ph):
            ph.remove_bounty(self.b)
            self.Interface.store_player(ph)
            await interaction.edit(embed=character_embed(interaction,ph),view=Inventory_View(ph))
            await interaction.send(f'Alle erledigten bountys wurden eingesammelt',ephemeral=True)
        else:
            await interaction.send(f'Etwas ist schief gelaufen',ephemeral=True)
        
        

class Stats_Inventory_Button(nextcord.ui.Button):
    def __init__(self,player, label: str = "Show stats"):
        super().__init__(label=label, disabled=False)
        self.interface=DB()
        self.player = player

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.send(embed=stats_embed(self.player),view=Stats_Inventory_View(player=self.player),ephemeral=True)

class Stats_Inventory_Select(nextcord.ui.Select):
    def __init__(self, player:Player, custom_id: str = "Stats:Inventory:Select", placeholder: str = "Chose a stat to level up", min_values: int = 1, max_values: int = 1, disabled: bool = False, row:int = None) -> None:
        super().__init__(custom_id=custom_id+f":{player.name}", placeholder=placeholder, min_values=min_values, max_values=max_values, disabled=disabled, row=row)
        self.player = player
        self.interface = DB()
        if self.player.skill_tokens <= 0:
            self.add_option(label="No skilltoken left")
            return
        self.add_option(label="deff",value="deff",description="Select an stats to use an skill token")
        self.add_option(label="atk",value="atk",description="Select an stats to use an skill token")
        self.add_option(label="stamina",value="stamina",description="Select an stats to use an skill token")
        self.add_option(label="trading",value="trading",description="Select an stats to use an skill token")
        self.add_option(label="sneak",value="sneak",description="Select an stats to use an skill token")
        self.add_option(label="health",value="health",description="Select an stats to use an skill token")
        self.add_option(label="cook",value="cook",description="Select an stats to use an skill token")
        self.add_option(label="mana",value="mana",description="Select an stats to use an skill token")
        self.add_option(label="craft",value="craft",description="Select an stats to use an skill token")
        self.add_option(label="knowledge",value="knowledge",description="Select an stats to use an skill token")
        self.add_option(label="speed",value="speed",description="Select an stat to use an skill token")

    async def callback(self, interaction: nextcord.Interaction):
        if self.player.use_skill_token(self.values[0]):
            await interaction.edit(embed=stats_embed(self.player),view=Stats_Inventory_View(player=self.player))
        else:
            await interaction.edit(embed=stats_embed(self.player),view=Stats_Inventory_View(player=self.player))
        self.interface.store_player(self.player)

class Stats_Inventory_View(nextcord.ui.View):
    def __init__(self, player:Player, timeout:float = None):
        super().__init__(timeout=timeout)
        self.add_item(Stats_Inventory_Select(player))

class Item_Inventory_Detail_View(nextcord.ui.View):
    def __init__(self,i:Base_Item,player):
        self.item = i
        super().__init__(timeout=None)
        self.add_item(Craft_Item_Button(i))    
        self.add_item(Delete_Item_Button(i))
        self.add_item(Open_Trade_Button(i))
        self.add_item(Equip_Armor_Button(i))
        self.add_item(Equip_Weapon_Button(i))
        self.add_item(Equip_Artefact_Button(i))
        self.add_item(Use_Item_Button(i))

class Trade_Inventory_Detail_View(nextcord.ui.View):
    def __init__(self,t:Trade):
        super().__init__(timeout=None)
        self.add_item(Delete_Trade_Button(t))

class Bounty_Inventory_Detail_View(nextcord.ui.View):
    def __init__(self,b:Bounty):
        super().__init__(timeout=None)
        self.add_item(Remove_Bounty_Button(b))
        self.add_item(Complete_Bounty_Button(b))
        
class Inventory_View(nextcord.ui.View):
    def __init__(self,p:Player):
        self.p = p
        db = DB()
        self.p = db.load_player(self.p.name)
        super().__init__(timeout=None)
        self.add_item(Inventory_Select(p))
        self.add_item(Inventory_Trade_Select(p))
        self.add_item(Inventory_Bounty_Select(p))
        self.add_item(Work_Select(p))
        self.add_item(Unequip_Armor_Button())
        self.add_item(Unequip_Weapon_Button())
        #self.add_item(Unequip_Artefact_Button())
        self.add_item(Stats_Inventory_Button(p))
        self.add_item(Stop_Work_Button())
        self.add_item(Show_Poststelle(p))


class Work_Select(nextcord.ui.Select):
    def __init__(self,player) -> None:
        self.al = Asset_Loader()
        w = self.al.load_works()
        
        super().__init__(placeholder="Select the work for more details")
        for wo in w:
            if wo.level <= player.level:
                self.add_option(label=wo.name,value=wo.name,description=f"level:{wo.level}")

    async def callback(self, interaction: nextcord.Interaction):
        work = self.al.load_work(self.values[0])

        e = nextcord.Embed(title=work.name)
        e.add_field(name="Reward items",value=work.items)
        await interaction.send(embed=e,view=Work_View(work),ephemeral=True)

class Start_Work_Button(nextcord.ui.Button):
    def __init__(self, work, style: ButtonStyle = nextcord.ButtonStyle.green, label = "Start work"):
        self.work = work
        super().__init__(style=style, label=label)

    async def callback(self, interaction: nextcord.Interaction):
        Interface = DB()
        
        player:Player = Interface.load_player(str(interaction.user))
        player.start_work(self.work)
        Interface.store_player(player)
        await interaction.edit(embed=character_embed(interaction,player),view=Inventory_View(player))
        await interaction.send(f"Started working on {self.work.name}",ephemeral=True)

class Stop_Work_Button(nextcord.ui.Button):
    def __init__(self, style: ButtonStyle = nextcord.ButtonStyle.red, label = "Stop work"):
        super().__init__(style=style, label=label)

    async def callback(self, interaction: nextcord.Interaction):
        Interface = DB()
        player:Player = Interface.load_player(str(interaction.user))
        rew = player.stop_work()
        Interface.store_player(player)
        rew.sort()
        rew = str(rew)
        await interaction.edit(embed=character_embed(interaction,player),view=Inventory_View(player))

        if len(rew)<100:
            await interaction.send("Du hast viele Items gesammelt! Zu viele zum anzeigen schaue in dein Inventar.",ephemeral=True)
            return
        await interaction.send(f"Stoped working and got these rewards: {rew}",ephemeral=True)

class Work_View(nextcord.ui.View):
    def __init__(self,work):
        super().__init__(timeout=None)
        self.add_item(Start_Work_Button(work))
        self.add_item(Stop_Work_Button())

class Inventory_Select(nextcord.ui.Select):
    def __init__(self,p:Player):
        self.p = p
        self.items=[]
        self.Interface = DB()
        super().__init__(custom_id=f"Inventory:Embed:{p.name}", placeholder="Dein Inventar", min_values=1, max_values=1, options=self.items, disabled=False, row=None)
        if p.items == None:
            self.add_option(label="Keine Items vorhanden.")
            return
        for i in p.items:
            self.items.append(nextcord.SelectOption(label=f"{i.name}x{i.quantity}",description=i.description))
            
    
    async def callback(self, interaction: nextcord.Interaction):
        ph=self.Interface.load_player(str(interaction.user))
        for i in ph.items:
            if str(i.name) == str(self.values[0].split("x")[0]):
                e,r= item_embed(i)
                II = Item_Inventory_Detail_View(i,ph)
                if type(i)!= Potion:
                    II.remove_item(II.children[6])
                if type(i)!=Artefact:
                    II.remove_item(II.children[5])
                if type(i)!= Weapon:
                    II.remove_item(II.children[4])
                if type(i)!= Armor:
                    II.remove_item((II.children[3]))
                if r==True:
                    return await interaction.send(embed=e,view=II,ephemeral=True)
                else: 
                    II.remove_item(II.children[0])
                    return await interaction.send(embed=e,view=II,ephemeral=True)
        
class Inventory_Trade_Select(nextcord.ui.Select):    
    def __init__(self,p:Player) -> None:
        self.p = p
        self.trades=[]
        self.Interface = DB()
        i=0
        if p.trades !=[] and p.trades != None:
            for t in p.trades:
                self.trades.append(nextcord.SelectOption(label=f"{t.item.name}x{t.item.quantity}:{i}",description=f"{t.price}$\ntrade closed: {t.done}"))
                t.id=i
                i+=1
        else:
            self.trades.append(nextcord.SelectOption(label=f"Keine Trades vorhanden"))
        self.Interface.store_player(p)
        super().__init__(custom_id=f"Inventory:Embed:Trade:{p.name}", placeholder="Deine Trades", min_values=1, max_values=1, options=self.trades, disabled=False, row=None)
        
    async def callback(self, interaction: nextcord.Interaction):
        if self.p.trades==[]:
            return
        name=self.values[0].split("x")[0]
        quantity=self.values[0].split("x")[1].split(":")[0]    
        _id= self.values[0].split("x")[1].split(":")[1]
        for t in self.p.trades:
            if t.item.name==name and t.item.quantity==int(quantity)and t.id == int(_id):
                await interaction.send(embed=trade_embed(t),view=Trade_Inventory_Detail_View(t),ephemeral=True)
                self.__init__(self.p)

class Inventory_Bounty_Select(nextcord.ui.Select):
    def __init__(self,p:Player) -> None:
        self.p = p
        self.bountys=[]
        self.Interface = DB()
        i = 0   
        super().__init__(custom_id=f"Inventory:Select:Bounty:{p.name}", placeholder="Deine Bountys", min_values=1, max_values=1, options=self.bountys, disabled=False, row=None) 
        if p.bountys != [] and p.bountys != None:    
            for b in p.bountys:
                if i >=25:
                    return
                self.bountys.append(nextcord.SelectOption(label=f"{b.name}:id {i}",description=f"{b.reward_money}$ wird bearbeitet:{b.worked_on}"))
                i+=1
        else:
            self.bountys.append(nextcord.SelectOption(label=f"keine bountys vorhanden"))
                
        
    async def callback(self, interaction: nextcord.Interaction):
        if self.p.bountys==[]:
            return
        for b in self.p.bountys:
            if b.name == self.values[0].split(":")[0]:
                await interaction.send(embed=bounty_embed(b),view=Bounty_Inventory_Detail_View(b),ephemeral=True)
                return
