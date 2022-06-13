import sqlite3 as sl
import pickle
from typing import List
from src.Scripts.Classes.Suggsetion.suggsetion import Suggsestion
from src.Scripts.Classes.Guild.guild import Guild

from src.Scripts.Functions import log
"""V1.0.0
Authors: Noah Schneider
Date: 31.05.21
Description: DB Class to load and store objects from the DB    
"""

class DB():
    def __init__(self):
        self.con = sl.connect('Data.db',check_same_thread=False)
        self.cur = self.con.cursor()

    def load_all_names(self,):
        """
        Description:
            Loads all names of the players
        Return:
            All names in the DB
        """
        self.cur.execute("SELECT _name FROM player")
        r = self.cur.fetchall()
        return(r)

    def del_player(self,name:str):
        """Deletes a Player out of the DB with the given name.

        Args:
            name (str): Name of the player (Discord name and id)
        """
        self.cur.execute(f"DELETE FROM player WHERE _name=?",(name,))
        self.con.commit()


    def load_player(self,name:str=None,id:int=None):
        """Loads a Player with the given name or id.
        
        Args:
            name (str, optional): Discord name and ID. Defaults to None.
            id (int, optional): id from the DB. Defaults to None.

        Returns:
            player: Player object bzw. Character objekt.
        """
        try:
            p=None
            if id != None:
                self.cur.execute("SELECT * FROM player WHERE _id = ?",(id,))
                r = self.cur.fetchone()
                p = pickle.loads(r[2])
            elif name != None:
                self.cur.execute("SELECT * FROM player WHERE _name = ?",(name,))
                r = self.cur.fetchone()
                p = pickle.loads(r[2])
            return p     
        except Exception as e:
            log(4,f"Spieler {name}:{id} konnte nicht geladen werden \nFehler im Inerface Load_Character: {e}")
        finally:
            self.con.commit()
  
    def store_player(self,p):
        """Stores a Player Object as an Pickel string

        Args:
            player (player): The player object to be stored

        """
        try:
            pickled_player = pickle.dumps(p)
            self.cur.execute("""UPDATE player
            SET
                _character=?
            WHERE id = ? Or _name =?""",(
                pickled_player,
                p.id,
                p.name
            ))
            self.con.commit()

        except Exception as e:
            log(3,f"Spieler {p.name} konnte nicht gespeichert werden\nFehler im Interface Store_Player {e}")
        finally:
            self.con.commit()
            log(1,f"Ein Spieler {p.name} wurde gespeichert")

    def create_character(self,p):
        """Creates a character in the DB
        
        Args:
            p (player): Player created from the discord input
        """
        try:
            if self.load_player(name=p.name)!=None:
                log(2,f"Spieler {p.name} hat schon einen Character")
                return False
            pickled_player = pickle.dumps(p)
            self.cur.execute("""INSERT INTO player (_name,_character) VALUES (?,?)""",(p.name,pickled_player))
            self.con.commit()
            log(1,f"Spieler {p.name} wurde erstellt")
            return True
        except Exception as e:
            log(3,f"Spieler {p.name} konnte nicht erstellt werden \nFehler im Inerface Create_Character: {e}")
        finally:
            self.con.commit()

    def commit(self):
        self.con.commit()
        return True

    def del_db(self):
        #Creating tables deleting tables
        with open('docs\schema.sql') as f:
            self.con.executescript(f.read())

    def create_guild(self,name:str,leader:str="",emblem:str="",house:str="",voicechannel:str="",textchannel:str="",category:str=""):
        """Creates an guild in the database.

        Args:
            name (str): Guild name
            leader (str, optional): Leader name. Defaults to "".
            emblem (str, optional): emblem img url. Defaults to "".
            house (str, optional): house img url. Defaults to "".
            voicechannel (str, optional): voicechannel id. Defaults to "".
            textchannel (str, optional): textchannel id. Defaults to "".
            category (str, optional): category id. Defaults to "".
        """
        self.cur.execute("""INSERT INTO guild (_name,_leader,_emblem,_house,_voicechannel,_textchannel,_category,_pnames,_exp,_level) VALUES (?,?,?,?,?,?,?,?,?,?)""",(name,leader,emblem,house,voicechannel,textchannel,category,"",0.0,1))
        self.con.commit()

    def load_guild(self,name) -> Guild:
        self.cur.execute("SELECT * FROM guild WHERE _name = ?",(name,))
        r = self.cur.fetchone()
        if r == None:
            return False
        guild = Guild(name=r[1],
                    players=[x for x in str(r[2]).removeprefix(",").removesuffix(",").split(',')],
                    leader=r[3],
                    exp=r[4],                    
                    level=r[5],
                    emblem=r[6],
                    house=r[7],
                    voicechannel=r[8],
                    textchannel=r[9],
                    category=r[10])
        return guild

    def del_guild(self,name:str):
        self.cur.execute(f"DELETE FROM guild WHERE _name=?",(name,))
        self.con.commit()

    def store_guild(self,guild:Guild)->None:
        player = guild.get_player_names_str()
        
        self.cur.execute("""UPDATE guild
            SET
                _pnames=?,
                _leader=?,
                _exp=?,
                _level=?,
                _emblem=?,
                _house=?,
                _voicechannel=?,
                _textchannel=?,
                _category=?
            WHERE _name = ? """,(
                player,
                guild.leader,
                guild.exp,
                guild.level,
                guild.emblem,
                guild.house,
                guild.voicechannel,
                guild.textchannel,
                guild.category,
                guild.name
            ))
        self.con.commit()

    def get_all_leaders(self)->List[str]:
        self.cur.execute("SELECT _leader FROM guild")
        r = self.cur.fetchall()
        return r

    def store_suggsetion(self,suggsetion:Suggsestion):
        self.cur.execute("""INSERT INTO suggsetions (type_,player,data,payed) VALUES (?,?,?,?)""",(suggsetion.type_,suggsetion.player,suggsetion.data,suggsetion.payed))
        self.con.commit()
