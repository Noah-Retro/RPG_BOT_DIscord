import nextcord
from nextcord.ui import View,Button,Select

from src.Scripts.Classes.Database.db import DB



class Trade_Embed(nextcord.Embed):
    def __init__(self,pagenumber, *, colour=nextcord.Colour.blue(), color=nextcord.Color.green(), title="Open trades", type = 'rich'):
        super().__init__(colour=colour, color=color, title=title, type=type)
        self.add_field(name="Tefjdksha dafshjfdaksl fhajdks",value="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.")
        self.set_footer(text=str(pagenumber))
        
        self.Interface=DB()
        self.trades=[]
        names = self.Interface.load_all_names()
        for name in names:
            for i in range(len(name)):
                ph = self.Interface.load_player(name[i])
                self.trades.append(ph.inventory.trades)
        print(self.trades)

class Trade_View(View):
    def __init__(self,pagenumber):
        self.pagenumber=pagenumber
        super().__init__()
        self.add_item(Trade_Select(pagenumber))
        self.add_item(Prev_Page_Button(pagenumber))
        self.add_item(Next_Page_Button(pagenumber))

class Next_Page_Button(Button):
    def __init__(self,pagenumber,label = "Next page"):
        super().__init__(label = label)
        self.pagenumber = pagenumber
        
    async def callback(self, interaction: nextcord.Interaction):
        self.pagenumber+=1
        #Check over length if pagenumber > len(Trades)/25:
        #self.pagenumber = 0

        await interaction.edit(embed=Trade_Embed())

class Prev_Page_Button(Button):
    def __init__(self,pagenumber,label = "Prev page"):
        super().__init__(label = label)
        self.pagenumber=pagenumber

    async def callback(self, interaction: nextcord.Interaction):
        self.pagenumber-=1
        #if self.pagnumber < 0:
        #    self.pagenumber = #max length of trades / 25

        await interaction.edit(embed=Trade_Embed())

class Trade_Select(Select):
    def __init__(self, placeholder = "Select a trade to accept it", min_values: int = 1, max_values: int = 1) -> None:
        super().__init__(placeholder= placeholder)
        for i in range(24):
            self.add_option(label=f"Trade:{i}",value=i)
            
