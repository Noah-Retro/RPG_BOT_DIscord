from nextcord.ext import commands,tasks
import nextcord
from nextcord.ext.commands.core import has_permissions
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Classes.Database.db import DB
from src.Scripts.Functions.logger import log
from docs.conf import *


class Events(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.Interface = DB()
        self.status.start()
        self._help=False

    def cog_unload(self) -> None:
        self.status.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=nextcord.Game(name=f"{PREFIX}help"))
        print("Bot has successfully logged in as: {}".format(self.bot.user))
        print("Bot ID: {}\n".format(self.bot.user.id))
        log(1,"Bot has successfully logged in as: {}".format(self.bot.user),"Bot ID: {}\n".format(self.bot.user.id))


    @commands.Cog.listener()
    async def on_disconnect(self):
        log(1,"Bot ist disconnected von Discord")

    @commands.Cog.listener()
    async def on_error(self,event,*args, **kwargs):
        log(3,f"{event}:{args}:{kwargs}")

    @commands.Cog.listener()
    async def on_member_ban(self,guild,user):
        try:
            self.Interface.del_player(user)
            log(1,f"{user} ist gebannt worden und der character gelöscht.")
        except:
            pass
        
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        ph:Player=self.Interface.load_player(str(message.author))
        if ph != None:
            ph.add_exp(MESSAGE_EXP)
            self.Interface.store_player(ph)

    @commands.Cog.listener()
    async def on_command(self,ctx):
        pass#print("A command was invoked")

    @tasks.loop(minutes=5)
    async def status(self):
        try:
            if not self._help:
                self._help = True
                await self.bot.change_presence(activity=nextcord.Game(name=f"{PREFIX}help"))
            else:
                self._help=False
                await self.bot.change_presence(activity=nextcord.Game(name=f"{GAME}"))
        except:
            pass
    
