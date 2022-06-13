import unittest
from src.Scripts.Classes.Stats.player_stat import Stat
from src.Scripts.Classes.Items.base_item import Base_Item
from docs.conf import LEVEL_UP_EXP
from src.Scripts.Classes.Items.base_item import Base_Item
from src.Scripts.Classes.Informations.informations import Informations
from src.Scripts.Classes.Inventory.player_inventory import Player_Inventory
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Classes.Stats.player_stat import Stat
from src.Scripts.Classes.Database.db import DB

class TestStats(unittest.TestCase):
    def test_add_exp_level_up(self):
        test_level=1
        test_exp=10
        stat = Stat(level=test_level,exp=0,skill_tokens=test_level)
        stat.add_exp(test_exp)
        while test_exp >= LEVEL_UP_EXP**test_level :
            test_exp -= LEVEL_UP_EXP**test_level
            test_level += 1
        
        self.assertEqual(test_level, stat.level)
        self.assertEqual(test_exp, stat.exp)
        self.assertEqual(test_level, stat.skill_tokens)
        self.assertEqual(LEVEL_UP_EXP**test_level, stat.next_level)

class TestItem(unittest.TestCase):
    def test_remove_item_quantity(self):
        item = Base_Item(name="test",value=1,quantity=2,description="lol test")
        
        self.assertEqual(item.remove_quantity(2),True)
        self.assertEqual(item.quantity,0)

    def test_subtract_item_quantity(self):
        item = Base_Item(name="test",value=1,quantity=3,description="lol test")
        
        self.assertEqual(item.remove_quantity(2),True)
        self.assertEqual(item.quantity,1)

    def test_add_item_quantity(self):
        item = Base_Item(name="test",value=1,quantity=3,description="lol test")
        
        self.assertEqual(item.add_quantity(2),True)
        self.assertEqual(item.quantity,5)

class TestDB(unittest.TestCase):
    
    p = Player(id=0,name="Retro#5636",character_name="Schande",information=Informations(story="Hy ich bin die Story",looks="Das Aussehen",img="https://www.google.com/img=?jfdashgupheuigujasiuhgudhsajkhdjaklgjdlkaj.png",gender="Male",race="Mensch",p_class="Trader",working=False,age=20),inventory=Player_Inventory(items=[Base_Item(name="Apfel",value=1.0,quantity=10,description="Beschreibung eines Apfels",img="www.google.com/img=?apfel.png")]),stats=Stat)
    db = DB()
    
    def test_1create_character(self):
        self.db.create_character(self.p)
        self.db.commit()
        p1 = self.db.load_player(name=self.p.name)
        self.db.commit()  
        self.assertEqual(self.p,p1)

    def test_2store_load_player(self):
        self.db.store_player(self.p)
        self.db.commit()
        p1 = self.db.load_player(name=self.p.name)
        self.db.commit()
        self.assertEqual(self.p,p1)
        
    def test_3del_player(self):
        self.db.del_player(name=self.p.name)
        self.db.commit()
        
        self.assertRaisesRegex(Exception,self.db.load_player(name=self.p.name))
        self.db.commit()
