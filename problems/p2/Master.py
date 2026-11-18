from Wizard import Wizard

class Master(Wizard):
    """A Wizard who teaches at a school."""

    def __init__(self, name, age, school):
        """Creates a new Master with the specified name, age, and school, and a blank spell list."""
        self.set_school(school)
        super().__init__(name, age)

    def get_school(self):
        """Returns the name of the Master's school."""
        return self.school

    def set_school(self, school):
        """Changes the Master's school, after checking that school is a string."""
        if not isinstance(school, str):
            raise TypeError("School must be of type string, instead type " \
                 + str(type(school)))
        self.school = school

    def __str__(self):
        """Returns the Wizard's name and school as a string."""
        return super().__str__() + " of " + self.get_school()
