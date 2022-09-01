from os import name
import sys
import nextcord
from nextcord.ext import commands
from src.Scripts.Discord_Gui_Bot.Cogs.fight_cog import Fight_Cog
from src.Scripts.Discord_Gui_Bot.Cogs.suggsetion_cog import Suggsetion_Cog
from src.Scripts.Discord_Gui_Bot.Cogs.guild_cog import Guild_Cog
from docs.conf import TOKEN
from src.Scripts.Discord_Gui_Bot.Cogs.admin_cog import admin
#from src.Scripts.Discord_Gui_Bot.Cogs.rollplay_cog import Rollplay
from src.Scripts.Discord_Gui_Bot.Cogs.bot_info_cog import infos
from src.Scripts.Discord_Gui_Bot.Cogs.craft_cog import Crafting_Cog
from src.Scripts.Discord_Gui_Bot.Cogs.create_character_cogs import character
from src.Scripts.Discord_Gui_Bot.Cogs.event_cog import Events
from src.Scripts.Discord_Gui_Bot.Cogs.gameplay_cog import Gameplay
from src.Scripts.Discord_Gui_Bot.Cogs.markt_cog import Market_Trading
from src.Scripts.Discord_Gui_Bot.Cogs.player_infos_cog import player_infos
from src.Scripts.Classes.Output_Beautifer.loadbar import LoadBar
#from src.Scripts.Discord_Gui_Bot.Cogs.test_cog import test


intents = nextcord.Intents.all()

bot = commands.Bot(intents=intents)#
#bot.activity = nextcord.Game(name="RPG")

lb = LoadBar(title="Cogs registered")
bot.remove_command("help")

def run_bot():
    lb.write(1/9*100)   
    bot.add_cog(character(bot))
    lb.write(2/9*100) 
    bot.add_cog(admin(bot))
    lb.write(3/9*100) 
    bot.add_cog(Events(bot))
    lb.write(4/9*100) 
    bot.add_cog(Gameplay(bot))
    lb.write(5/9*100) 
    bot.add_cog(player_infos(bot))
    #bot.add_cog(Rollplay(bot))
    lb.write(6/9*100) 
    bot.add_cog(infos(bot))
    lb.write(7/9*100) 
    bot.add_cog(Crafting_Cog(bot))
    lb.write(8/9*100) 
    bot.add_cog(Market_Trading(bot))
    #bot.add_cog(test(bot))
    bot.add_cog(Guild_Cog(bot))
    lb.write(9/9*100) 
    bot.add_cog(Suggsetion_Cog(bot))
    bot.add_cog(Fight_Cog(bot))
    bot.run(TOKEN)

def restart():
    bot.close()
    run_bot()
