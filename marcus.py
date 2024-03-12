# import modules
# from tkinter import Tk

# class for player includes attributes: name, attack, and defence
# TODO Finish player object
class Player:
    """docstring for Player"""
    # _ (underscore) signals that a given attr is non-public and can only be accessed to class it was derived from

    def __init__(self, name, attack, defence, location):
        self._name = name
        self._attack = attack
        self._defence = defence
        self._location = location
        # spells
        # xp
        # luck

    # Getter: A method that allows you to access an attribute in a given class
    # Setter: A method that allows you to set or mutate the value of an attribute in a class
    @property
    def name(self): return self._name

    @name.setter
    def name(self, newname): self._name = newname

    @property
    def attack(self): return self._attack

    @attack.setter
    def attack(self, newattack): self._attack = newattack

    @property
    def defence(self): return self._defence

    @defence.setter
    def defence(self, newdefence): self._defence = newdefence

    @property
    def location(self): return self._location

    @location.setter
    def location(self, newlocation): self._location = newlocation

    # TODO create move method
    def move(self, loc_list):
        """
            moves the player
        """
        dest = str(input("Where would you like to move?")).upper()

        for loc in loc_list:
            if loc["name"] == self._location:
                if dest in loc["dest"]:
                    self._location = dest
                    return dest

        return False


class Location:
    """docstring for Location"""

    def __init__(self, name, desc, dest):
        self.name = name
        self.desc = desc
        self.dest = dest

    @property
    def name(self): return self._name

    @property
    def desc(self): return self._desc

    @property
    def dest(self): return self._dest

    @name.setter
    def name(self, value):
        self._name = value

    @desc.setter
    def desc(self, value):
        self._desc = value

    @dest.setter
    def dest(self, value):
        self._dest = value

    def __str__(self):
        """prints the location name, desc, and possible dest"""
        return f'You moved to {self._name}.\n{self._desc}.\nYou can move to {self._dest}.'


# TODO create map
loc_list = [{"name": "A", "desc": "Room", "dest": ["B", "C", "D"]},
            {"name": "B", "desc": "Path", "dest": ["C"]},
            {"name": "C", "desc": "Path 2", "dest": []},
            {"name": "D", "desc": "", "dest": []}]


class Map:
    """docstring for Map"""

    def __init__(self):
        self.map = []
        self.add_location()

    def add_location(self):
        self.map = [Location(**loc) for loc in loc_list]


current_location = "A"
m = Map()


# test player
player = Player('test', 10, 10, current_location)

while not player.move(loc_list):
    print("Invalid command/Location not in destination")

