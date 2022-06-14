import nextcord
from click import option
from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader
from src.Scripts.Classes.Database.db import DB
from src.Scripts.Classes.Items.base_item import Base_Item
from src.Scripts.Classes.Market.base_market import Market

#Update to View
#Bounty select
    #Bounty Get
#Trade select
    #Trade Get
    #Bulk Get

class Market_Detail_View(nextcord.ui.View):
    def __init__(self,ma:Market):
        self.ma = ma
        super().__init__(timeout=None)
        self.add_item(Market_Detail_Select_Bounty(ma=self.ma))
        self.add_item(Market_Detail_Select_Trade(ma=self.ma))

class Market_Detail_Select_Trade(nextcord.ui.Select):
    def __init__(self, ma:Market, custom_id: str = "Market:Detail:Trade:Select", placeholder:str="Item select", min_values: int = 1, max_values: int = 1, options = None, disabled: bool = False, row:int = None) -> None:
        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, options=options, disabled=disabled, row=row)
        self.ma = ma
        self.Interface = DB()
        self.Al = Asset_Loader()

        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, disabled=disabled, row=row)

        for trade in self.ma.trades:
            self.add_option(label=trade.item.name,value=trade.item.name,description="Click the trade you want to claim")        
        
    async def callback(self,interaction:nextcord.Interaction):
        mh = self.ma
        item = self.values[0]
        player = self.Interface.load_player(str(interaction.user))
        done,cost= mh.trade(item=item,player=player)
        if done:
            await interaction.send(f'{interaction.user} hat {item} bei {mh.name} gekauft zum preis von {cost}',ephemeral=True)
        else:
            await interaction.send(f'Etwas ist schief gelaufen. Kontrolliere nochmals ob alle Angaben richtig sind.',ephemeral=True)
        self.Interface.store_player(player)

class Market_Detail_Select_Bounty(nextcord.ui.Select):
    def __init__(self, ma:Market, custom_id: str = "Market:Detail:Bounty:Select", placeholder:str="Bounty select", min_values: int = 1, max_values: int = 1, disabled: bool = False, row:int = None) -> None:
        self.ma = ma
        self.Interface = DB()
        self.Al = Asset_Loader()

        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, disabled=disabled, row=row)

        for bounty in self.ma.bountys:
            self.add_option(label=bounty.name,value=bounty.name,description="Click the bounty you want to claim")        
        
    async def callback(self, interaction: nextcord.Interaction):
        player=self.Interface.load_player(name=str(interaction.user))
        if self.ma.give_bounty(bounty=self.Al.load_bounty(self.values[0]),player=player):
            await interaction.send(f'{self.values[0]} wurde {interaction.user} gegeben',ephemeral=True)
        else:
            await interaction.send(f'Etwas ist schief gelaufen. Kontrolliere nochmals ob du genügend Platz im Inventar hast.',ephemeral=True)
        self.Interface.store_player(player)

def Market_Embed(m:Market):
    e = nextcord.Embed(title=m.name)
    st=""
    sb=""
    for t in m.trades:
        st+=f'{t.item.quantity}x{t.item.name} {t.price}$\n'
    for b in m.bountys:
        sb+=f'Bounty: **{b.name}**\n reward: {b.reward_money}$ und '
        for i in b.reward_items:
            sb+=f'{i.name}x{i.quantity} \n'
    e.add_field(name=m.name+" trades",value=st,inline=False)
    e.add_field(name=m.name + " bountys",value=sb,inline=True)
    return e


class Market_View(nextcord.ui.View):
    def __init__(self,ma:Market,msg=None):
        self.ma =ma
        super().__init__(timeout=None)
        self.add_item(Market_Select(ma))
        
class Market_Select(nextcord.ui.Select):
    def __init__(self,ma, custom_id: str = "Market:Select", placeholder="Wähle einen Markt", min_values: int = 1, max_values: int = 1) -> None:
        op=[]
        for m in ma:
            op.append(nextcord.SelectOption(label=str(m.name),description=f"min level: {m.level}"))
        self.Al = Asset_Loader()
        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, options=op)
           
    async def callback(self, interaction: nextcord.Interaction):
        Interface= DB()
        player = Interface.load_player(str(interaction.user))
        m = self.Al.load_market(str(self.values[0]))
        if player.level <  m.level:
            await interaction.send("Du bist noch ein zu niedriges Level um den Markt zu betreten",ephemeral=True)
            return
        await interaction.send(embed=Market_Embed(m),view=Market_Detail_View(self.Al.load_market(str(self.values[0]))),ephemeral=True) 
        


        
        