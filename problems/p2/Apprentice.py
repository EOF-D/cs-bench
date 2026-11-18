from Wizard import Wizard
from Master import Master


class Apprentice(Wizard):
    """A Wizard who studies under a Master."""

    def __init__(self, name, age, master):
        """Creates a new Apprentice with the specified name, age, and master, and a blank spell list."""
        self.set_master(master)
        super().__init__(name, age)

    def get_master(self):
        """Returns the Master this Apprentice belongs to."""
        return self.master

    def set_master(self, master):
        """Changes the Apprentice's master, after checking that master is a Master object."""
        if not isinstance(master, Master) and master != None:
            raise TypeError("Master must be of type Master or None, instead \
                 type " + str(type(master)))
        self.master = master

    def __str__(self):
        """Returns the Wizard's name and master's name as a string."""
        return super().__str__() + ", apprentice of " + self.master.get_name()
