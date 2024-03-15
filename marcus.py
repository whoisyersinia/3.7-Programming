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

    def move(self, location_list):
        """
            moves the player by checking if the dest is a valid dest
        """
        dest = str(input("Where would you like to move?")).upper()

        for loc in location_list:
            if loc["name"] == self._location:
                if dest in loc["dest"]:
                    self._location = dest
                    return dest

        return False


class Location:
    """docstring for Location"""

    def __init__(self, name, desc, dest):
        self._name = name
        self._desc = desc
        self._dest = dest

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

    def dest_name(self, map_dest):
        dest_name_list = []
        for dest in map_dest:
            if dest["name"] in self._dest:
                dest_name_list.append(dest["desc"])

        return dest_name_list

    def print_location_info(self, dest_list):
        """prints the location name, desc, and possible dest"""
        dest = ", ".join(dest_list)
        return f'You moved to {self._name}.\n{self._desc}.\nYou can move to {dest}.'


# TODO create map
LOC_LIST = [{"name": "A", "desc": "Room", "dest": ["B", "C", "D"]},
            {"name": "B", "desc": "Path", "dest": ["C", "D"]},
            {"name": "C", "desc": "Path 2", "dest": []},
            {"name": "D", "desc": "Hello", "dest": []}]


class Map:
    """docstring for Map"""

    def __init__(self):
        self.map = []
        self.add_location()

    def add_location(self):
        self.map = [Location(**loc) for loc in LOC_LIST]


current_location = "A"
m = Map()


# test player
player = Player('test', 10, 10, current_location)


# input validator
check_loc = player.move(LOC_LIST)

while not check_loc:
    print("Invalid command/Location not in destination")
    check_loc = player.move(LOC_LIST)

# prints current_loc
for locs in LOC_LIST:
    if check_loc == locs["name"]:

        new_location = Location(check_loc, locs["desc"], locs["dest"])
        destinations = new_location.dest_name(LOC_LIST)
        print(new_location.print_location_info(destinations))
