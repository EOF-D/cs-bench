class Wizard:
    """A general object for describing Wizards, including their name, age, and spell list."""

    def __init__(self, name, age):
        """Creates a new Wizard with the specified name and age and a blank spell list."""
        self.set_name(name)
        self.set_age(age)
        self.spells = []

    def get_name(self):
        """Returns the Wizard's name."""
        return self.name

    def set_name(self, name):
        """Changes the Wizard's name, after checking that name is a string."""
        if not isinstance(name, str):
            raise TypeError(
                "Name must be of type string, instead type " + str(type(name))
            )
        self.name = name

    def get_age(self):
        """Returns the Wizard's age."""
        return self.age

    def set_age(self, age):
        """Changes the Wizard's age, after checking that name is a nonzero integer."""
        if not isinstance(age, int):
            raise TypeError("Age must be of type int, instead type " + str(type(age)))
        if age < 0:
            raise ValueError("Wizard must have age zero or greater.")
        self.age = age

    def add_spell(self, spell):
        """Adds a spell to the Wizard's spell list. Spells are strings."""
        if not isinstance(spell, str):
            raise TypeError(
                "Spell must be of type string, instead type " + str(type(spell))
            )
        self.spells.append(spell)

    def remove_spell(self, spell):
        """Removes a spell from the Wizard's spell list (if present). Spells are strings."""
        if not isinstance(spell, str):
            raise TypeError(
                "Spell must be of type string, instead type " + str(type(spell))
            )
        if spell in self.spells:
            self.spells.remove(spell)

    def get_spells(self):
        """Returns a list of the Wizard's spells (as strings)."""
        return self.spells

    def __str__(self):
        """Returns the Wizard's name as a string."""
        return self.get_name()
