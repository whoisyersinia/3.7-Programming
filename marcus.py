# import modules
# from tkinter import Tk

# class for player includes attributes: name, attack, and defence

class Character:
    def __init__(self, name, attack, defence, location):
        self._name = name
        self._attack = attack
        self._defence = defence
        self._location = location


# TODO Finish player object
class Player(Character):
    """docstring for Player"""

    # _ (underscore) signals that a given attr is non-public and can only be accessed to class it was derived from

    def __init__(self, name, attack, defence, location, inv=None):
        super().__init__(name, attack, defence, location)
        self._inv = inv
        # xp
        # luck

    # Getter: A method that allows you to access an attribute in a given class
    # Setter: A method that allows you to set or mutate the value of an attribute in a class
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, newAttack):
        self._attack = newAttack

    @property
    def defence(self):
        return self._defence

    @defence.setter
    def defence(self, newDefence):
        self._defence = newDefence

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, newLocation):
        self._location = newLocation

    @property
    def inv(self):
        return self._inv

    @inv.setter
    def inv(self, newInv):
        self._inv = newInv

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

    def __init__(self, name, desc, dest, npc, items):
        self._name = name
        self._desc = desc
        self._dest = dest
        self._npc = npc
        self._items = items

    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def dest(self):
        return self._dest

    @property
    def items(self):
        return self._items

    @property
    def npc(self):
        return self._npc

    @name.setter
    def name(self, value):
        self._name = value

    @desc.setter
    def desc(self, value):
        self._desc = value

    @dest.setter
    def dest(self, value):
        self._dest = value

    @npc.setter
    def npc(self, value):
        self._npc = value

    @items.setter
    def items(self, value):
        self._items = value

    # check if current location has a npc
    def check_npc(self):
        if self._npc:
            return True
        return False

    def dest_name(self, map_dest):
        dest_name_list = []
        for dest in map_dest:
            if dest["name"] in self._dest:
                dest_name_list.append(dest["desc"])

        return dest_name_list

    def print_location_info(self, dest_list):
        """prints the location name, desc, and possible dest"""
        dest = ", ".join(dest_list)
        if self.check_npc():
            return f'You moved to {self._name}.\n{self._desc}.\nYou can move to {dest}.\nSomeone is waving at you!'
        else:
            return f'You moved to {self._name}.\n{self._desc}.\nYou can move to {dest}.\n '


class Npc(Character):
    def __init__(self, name, attack, defence, location, dialogue=None):
        super().__init__(name, attack, defence, location)
        self.dialogue = dialogue

    def interact(self):
        """ interact with npc """
        pass

    def print_dialogue(self):
        """ prints dialogue """
        pass


class Enemy(Character):
    def __init__(self, name, attack, defence, location):
        super().__init__(name, attack, defence, location)
    pass


class Map:
    """docstring for Map"""

    def __init__(self, maps, npc):
        self._map = maps
        self._npc = npc

    @property
    def map(self):
        return self._map

    @property
    def npc(self):
        return self._npc

    @map.setter
    def map(self, newMap):
        self._map = newMap

    @npc.setter
    def npc(self, newNpc):
        self._npc = newNpc


NPC_DIALOGUE = [{"name": "Test", "": ""}]

# TODO create map
LOC_LIST = [{"name": "A", "desc": "Room", "dest": ["B", "C", "D"], "npc": "Test", "items": ""},
            {"name": "B", "desc": "Path", "dest": ["C", "D"], "npc": "Hi", "items": ""},
            {"name": "C", "desc": "Path 2", "dest": [], "npc": "", "items": ""},
            {"name": "D", "desc": "Hello", "dest": [], "npc": "", "items": ""}]

current_location = "A"

m = Map([Location(**loc) for loc in LOC_LIST], [Npc(loc["npc"], loc["name"]) for loc in LOC_LIST])

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
        new_location = Location(check_loc, locs["desc"], locs["dest"], locs["npc"], locs["items"])
        destinations = new_location.dest_name(LOC_LIST)
        print(new_location.print_location_info(destinations))
