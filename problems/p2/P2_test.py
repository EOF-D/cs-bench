import unittest
from Wizard import Wizard
from Master import Master
from Apprentice import Apprentice

# human took ~75 minutes to write code and tests

class TestWizard(unittest.TestCase):
    def test_name(self):
        w = Wizard("Rose",555)
        self.assertEqual(w.get_name(), "Rose", "Incorrect name")

    def test_blank_name(self):
        w = Wizard("",555)
        self.assertEqual(w.get_name(), "", "Incorrect name")

    def test_set_name(self):
        w = Wizard("",555)
        w.set_name("Kiara")
        self.assertEqual(w.get_name(), "Kiara", "Incorrect name")

    def test_set_blank_name(self):
        w = Wizard("Kiara",555)
        w.set_name("")
        self.assertEqual(w.get_name(), "", "Incorrect name")

    def test_nonstring_name(self):
        self.assertRaises(TypeError, Wizard, 10, 555)

    def test_set_nonstring_name(self):
        w = Wizard("Rose",555)
        self.assertRaises(TypeError, w.set_name, 10)

    def test_age(self):
        w = Wizard("Rose",555)
        self.assertEqual(w.get_age(), 555, "Incorrect age")

    def test_set_age(self):
        w = Wizard("Rose",555)
        w.set_age(600)
        self.assertEqual(w.get_age(), 600, "Incorrect age")

    def test_zero_age(self):
        w = Wizard("Rose",0)
        self.assertEqual(w.get_age(), 0, "Incorrect age")

    def test_negative_age(self):
        self.assertRaises(ValueError, Wizard, "", -1)

    def test_set_negative_age(self):
        w = Wizard("Rose",555)
        self.assertRaises(ValueError, w.set_age, -1)

    def test_very_large_age(self):
        w = Wizard("Rose",9223372036854775808)
        self.assertEqual(w.get_age(), 9223372036854775808, "Incorrect age")

    def test_nonnumber_age(self):
        self.assertRaises(TypeError, Wizard, "Rose", "old as the mountains")

    def test_set_nonnumber_age(self):
        w = Wizard("Rose",555)
        self.assertRaises(TypeError, w.set_age, "old as the mountains")

    def test_spells(self):
        w = Wizard("Rose",555)
        self.assertEqual(w.get_spells(), [], "Spell list not blank at start")
        w.add_spell("Fireball")
        self.assertEqual(w.get_spells(), ["Fireball"], "Spell list did not accept new spell")

    def test_spell_remove(self):
        w = Wizard("Rose",555)
        self.assertEqual(w.get_spells(), [], "Spell list not blank at start")
        w.add_spell("Fireball")
        self.assertEqual(w.get_spells(), ["Fireball"], "Spell list did not accept new spell")
        w.remove_spell("Fireball")
        self.assertEqual(w.get_spells(), [], "Spell list did not accept new spell")

    def test_spell_remove_empty(self):
        w = Wizard("Rose",555)
        self.assertEqual(w.get_spells(), [], "Spell list not blank at start")
        w.remove_spell("Fireball")
        self.assertEqual(w.get_spells(), [], "Spell list is not blank after removal")

    def test_nonstring_spell(self):
        w = Wizard("Rose",555)
        self.assertRaises(TypeError, w.add_spell, 10)

    def test_nonstring_remove_spell(self):
        w = Wizard("Rose",555)
        self.assertRaises(TypeError, w.remove_spell, 10)

    def test_string_convert(self):
        w = Wizard("Rose",555)
        self.assertEqual(str(w), "Rose", "Wizard did not print correctly.")

class TestMaster(unittest.TestCase):
    def test_name(self):
        w = Master("Rose",555, "Champlain College")
        self.assertEqual(w.get_name(), "Rose", "Incorrect name")

    def test_blank_name(self):
        w = Master("",555, "Champlain College")
        self.assertEqual(w.get_name(), "", "Incorrect name")

    def test_set_name(self):
        w = Master("",555, "Champlain College")
        w.set_name("Kiara")
        self.assertEqual(w.get_name(), "Kiara", "Incorrect name")

    def test_set_blank_name(self):
        w = Master("Kiara",555, "Champlain College")
        w.set_name("")
        self.assertEqual(w.get_name(), "", "Incorrect name")

    def test_nonstring_name(self):
        self.assertRaises(TypeError, Master, 10, 555, "Champlain College")

    def test_set_nonstring_name(self):
        w = Master("Rose",555, "Champlain College")
        self.assertRaises(TypeError, w.set_name, 10)

    def test_age(self):
        w = Master("Rose",555, "Champlain College")
        self.assertEqual(w.get_age(), 555, "Incorrect age")

    def test_set_age(self):
        w = Master("Rose",555, "Champlain College")
        w.set_age(600)
        self.assertEqual(w.get_age(), 600, "Incorrect age")

    def test_zero_age(self):
        w = Master("Rose",0, "Champlain College")
        self.assertEqual(w.get_age(), 0, "Incorrect age")

    def test_negative_age(self):
        self.assertRaises(ValueError, Master, "", -1, "")

    def test_set_negative_age(self):
        w = Master("Rose",555,"Champlain College")
        self.assertRaises(ValueError, w.set_age, -1)

    def test_very_large_age(self):
        w = Master("Rose",9223372036854775808,"Champlain College")
        self.assertEqual(w.get_age(), 9223372036854775808, "Incorrect age")

    def test_set_nonnumber_age(self):
        w = Master("Rose",555,"Champlain College")
        self.assertRaises(TypeError, w.set_age, "old as the mountains")

    def test_nonnumber_age(self):
        self.assertRaises(TypeError, Master, "Rose", "old as the mountains", "Champlain College")

    def test_spells(self):
        w = Master("Rose",555,"Champlain College")
        self.assertEqual(w.get_spells(), [], "Spell list not blank at start")
        w.add_spell("Fireball")
        self.assertEqual(w.get_spells(), ["Fireball"], "Spell list did not accept new spell")

    def test_spell_remove(self):
        w = Master("Rose",555,"Champlain College")
        self.assertEqual(w.get_spells(), [], "Spell list not blank at start")
        w.add_spell("Fireball")
        self.assertEqual(w.get_spells(), ["Fireball"], "Spell list did not accept new spell")
        w.remove_spell("Fireball")
        self.assertEqual(w.get_spells(), [], "Spell list did not accept new spell")

    def test_spell_remove_empty(self):
        w = Master("Rose",555,"Champlain College")
        self.assertEqual(w.get_spells(), [], "Spell list not blank at start")
        w.remove_spell("Fireball")
        self.assertEqual(w.get_spells(), [], "Spell list is not blank after removal")

    def test_school(self):
        w = Master("Rose",555,"Champlain College")
        self.assertEqual(w.get_school(), "Champlain College", "Incorrect school")

    def test_nonstring_spell(self):
        w = Master("Rose",555,"Champlain College")
        self.assertRaises(TypeError, w.add_spell, 10)

    def test_nonstring_remove_spell(self):
        w = Master("Rose",555,"Champlain College")
        self.assertRaises(TypeError, w.remove_spell, 10)

    def test_school_blank(self):
        w = Master("Rose",555,"")
        self.assertEqual(w.get_school(), "", "Incorrect school")

    def test_set_school(self):
        w = Master("Rose",555,"")
        w.set_school("Champlain College")
        self.assertEqual(w.get_school(), "Champlain College", "Incorrect school")

    def test_set_school_blank(self):
        w = Master("Rose",555,"Champlain College")
        w.set_school("")
        self.assertEqual(w.get_school(), "", "Incorrect school")

    def test_nonstring_school(self):
        self.assertRaises(TypeError, Master, "Rose", 555, 10)

    def test_set_nonstring_school(self):
        w = Master("Rose",555,"Champlain College")
        self.assertRaises(TypeError, w.set_school, 10)

    def test_string_convert(self):
        w = Master("Rose",555,"Champlain College")
        self.assertEqual(str(w), "Rose of Champlain College", "Master did not print correctly.")

class testApprentice(unittest.TestCase):
    def setUp(self):
        self.master = Master("Diane",555,"Champlain College")

    def test_name(self):
        w = Apprentice("Rose",555, self.master)
        self.assertEqual(w.get_name(), "Rose", "Incorrect name")

    def test_blank_name(self):
        w = Apprentice("",555, self.master)
        self.assertEqual(w.get_name(), "", "Incorrect name")

    def test_set_name(self):
        w = Apprentice("",555, self.master)
        w.set_name("Kiara")
        self.assertEqual(w.get_name(), "Kiara", "Incorrect name")

    def test_set_blank_name(self):
        w = Apprentice("Kiara",555, self.master)
        w.set_name("")
        self.assertEqual(w.get_name(), "", "Incorrect name")

    def test_nonstring_name(self):
        self.assertRaises(TypeError, Apprentice, 10, 555, self.master)

    def test_set_nonstring_name(self):
        w = Apprentice("Rose",555, self.master)
        self.assertRaises(TypeError, w.set_name, 10)

    def test_age(self):
        w = Apprentice("Rose",555, self.master)
        self.assertEqual(w.get_age(), 555, "Incorrect age")

    def test_set_age(self):
        w = Apprentice("Rose",555, self.master)
        w.set_age(600)
        self.assertEqual(w.get_age(), 600, "Incorrect age")

    def test_zero_age(self):
        w = Apprentice("Rose",0, self.master)
        self.assertEqual(w.get_age(), 0, "Incorrect age")

    def test_negative_age(self):
        self.assertRaises(ValueError, Apprentice, "", -1, self.master)

    def test_set_negative_age(self):
        w = Apprentice("Rose",555,self.master)
        self.assertRaises(ValueError, w.set_age, -1)

    def test_very_large_age(self):
        w = Apprentice("Rose",9223372036854775808,self.master)
        self.assertEqual(w.get_age(), 9223372036854775808, "Incorrect age")

    def test_nonnumber_age(self):
        self.assertRaises(TypeError, Apprentice, "Rose", "old as the mountains", self.master)

    def test_set_nonnumber_age(self):
        w = Apprentice("Rose",555,self.master)
        self.assertRaises(TypeError, w.set_age, "old as the mountains")

    def test_spells(self):
        w = Apprentice("Rose",555,self.master)
        self.assertEqual(w.get_spells(), [], "Spell list not blank at start")
        w.add_spell("Fireball")
        self.assertEqual(w.get_spells(), ["Fireball"], "Spell list did not accept new spell")

    def test_spell_remove(self):
        w = Apprentice("Rose",555,self.master)
        self.assertEqual(w.get_spells(), [], "Spell list not blank at start")
        w.add_spell("Fireball")
        self.assertEqual(w.get_spells(), ["Fireball"], "Spell list did not accept new spell")
        w.remove_spell("Fireball")
        self.assertEqual(w.get_spells(), [], "Spell list did not accept new spell")

    def test_spell_remove_empty(self):
        w = Apprentice("Rose",555,self.master)
        self.assertEqual(w.get_spells(), [], "Spell list not blank at start")
        w.remove_spell("Fireball")
        self.assertEqual(w.get_spells(), [], "Spell list is not blank after removal")

    def test_nonstring_spell(self):
        w = Apprentice("Rose",555,self.master)
        self.assertRaises(TypeError, w.add_spell, 10)

    def test_nonstring_remove_spell(self):
        w = Apprentice("Rose",555,self.master)
        self.assertRaises(TypeError, w.remove_spell, 10)

    def test_master(self):
        w = Apprentice("Rose",555,self.master)
        self.assertEqual(w.get_master(), self.master, "Master name did not match")

    def test_blank_master(self):
        w = Apprentice("Rose",555,None)
        self.assertEqual(w.get_master(), None, "Master is not blank")

    def test_set_master(self):
        w = Apprentice("Rose",555,None)
        w.set_master(self.master)
        self.assertEqual(w.get_master(), self.master, "Master name did not match")

    def test_set_master_blank(self):
        w = Apprentice("Rose",555,self.master)
        w.set_master(None)
        self.assertEqual(w.get_master(), None, "Master name did not match")

    def test_nonmaster_master(self):
        self.assertRaises(TypeError, Apprentice, "Rose", 555, "Dude Perfect")

    def test_set_nonmaster_master(self):
        w = Apprentice("Rose",555,self.master)
        self.assertRaises(TypeError, w.set_master, "Dude Perfect")

    def test_string_convert(self):
        w = Apprentice("Rose",555,self.master)
        self.assertEqual(str(w), "Rose, apprentice of Diane", "Apprentice did not print correctly.")

if __name__ == '__main__':
    unittest.main()
