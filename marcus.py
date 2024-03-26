# import modules
import tkinter as tk
from tkinter import ttk


class Character:
    """
    Represents a character in the game.

    Attributes:
        _name (str): The name of the character.
        _attack (int): The attack power of the character.
        _defence (int): The defence power of the character.
        _location (str): The current location of the character.
    """

    def __init__(self, name, attack, defence, location):
        self._name = name
        self._attack = attack
        self._defence = defence
        self._location = location


# TODO Finish player object  
class Player(Character):
    """Player class.

    This class represents a player in the game. It inherits from the Character class.

    Attributes:
        _name (str): The name of the player.
        _attack (int): The attack power of the player.
        _defence (int): The defence power of the player.
        _location (str): The current location of the player.
        _inv (list): The inventory of the player.

    Methods:
        move(): Moves the player to a new location.
        move_validator(location_list): Validates the destination location.
        print_help(): Prints the available commands and instructions.
    """

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

    # action methods
    def move(self):
        # input validator
        check_loc = self.move_validator(LOC_LIST)

        if check_loc == "exit":
            print("go back")

        while not check_loc:
            print("Invalid command/Location not in destination")
            check_loc = self.move_validator(LOC_LIST)

        # prints current_loc
        for locs in LOC_LIST:
            if check_loc == locs["name"]:
                new_location = Location(check_loc, locs["desc"], locs["dest"], locs["npc"], locs["items"])
                destinations = new_location.dest_name(LOC_LIST)
                print(new_location.print_location_info(destinations))

    def move_validator(self, location_list):
        """
            moves the player by checking if the dest is a valid dest
        """
        dest = str(input("Where would you like to move? (Type 'Exit' or 'e' to go back)\n")).upper()

        if dest in ["EXIT", "E"]:
            return "exit"

        for loc in location_list:
            if loc["name"] == self._location:
                if dest in loc["dest"]:
                    self._location = dest
                    return dest

        return False

    @staticmethod
    def print_help():
        return print(f"To move: move or m\n"
                     f"To exit: exit\n")


class Enemy(Character):
    def __init__(self, name, attack, defence, location):
        super().__init__(name, attack, defence, location)

    pass


class Location:
    """A class representing a location in a game world.

    Attributes:
        name (str): The name of the location.
        _desc (str): The description of the location.
        _dest (list): A list of possible destinations from the location.
        _npc (bool): Indicates whether the location has a non-player character.
        _items (list): A list of items present in the location.

    Methods:
        check_npc(): Checks if the location has a non-player character.
        dest_name(map_dest): Returns a list of destination names based on the given map.
        print_location_info(dest_list): Prints the location information, including name, description, and possible
        destinations.
    """

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

    def check_npc(self):
        """Check if the current location has a non-player character.

        Returns:
            bool: True if the location has a non-player character, False otherwise.
        """
        if self._npc:
            return True
        return False

    def dest_name(self, map_dest):
        """Get the names of the destinations based on the given map.

        Args:
            map_dest (list): A list of destination dictionaries.

        Returns:
            list: A list of destination names.
        """
        dest_name_list = []
        for dest in map_dest:
            if dest["name"] in self._dest:
                dest_name_list.append(dest["desc"])

        return dest_name_list

    def print_location_info(self, dest_list):
        """Print the location information, including name, description, and possible destinations.

        Args:
            dest_list (list): A list of destination names.

        Returns:
            str: The formatted location information.
        """
        dest = ", ".join(dest_list)
        if self.check_npc():
            return (f'You moved to {self._name}.\n{self._desc}.\nYou can move to {dest}.\nSomeone is waving at you!\n'
                    f'(Talk)')
        else:
            return f'You moved to {self._name}.\n{self._desc}.\nYou can move to {dest}.\n '


class Npc:
    def __init__(self, name, location, dialogue=None):
        """
        Initializes an instance of the Npc class.

        Args:
            name (str): The name of the NPC.
            location (str): The location of the NPC.
            dialogue (str, optional): The dialogue of the NPC. Defaults to None.
        """
        self.name = name
        self.location = location
        self.dialogue = dialogue

    def interact(self):
        """
        Returns the name of the NPC.

        Returns:
            str: The name of the NPC.
        """
        return self.name

    def print_dialogue(self):
        """ 
        Prints the dialogue of the NPC.
        """
        pass


class Map:
    """A class representing a map.

    Attributes:
        _map (str): The map data.
        _npc (str): The NPC data.

    """

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

m = Map([Location(**loc) for loc in LOC_LIST], [Npc(loc["npc"], loc["name"], ) for loc in LOC_LIST])


def action_validator():
    """checks if action is valid and returns the action or False"""
    valid_inputs = ["move", "m", "help", "m"]

    print("What are you going do?")
    player_input = input("> ").lower()

    while player_input not in valid_inputs:
        print("Input not recognised. Try again! Type 'Help' if you need all the valid actions!")
        print("\nWhat are you going do?")
        player_input = input("> ").lower()

    return player_input


def return_action(player, action):
    """returns the action """
    action_dict = {"move": ["move", "m"], "help": ["help", "m"]}
    if action in action_dict["move"]:
        player.move()

    elif action in action_dict["help"]:
        player.print_help()


class App(tk.Tk):
    """ Main application gui"""

    def __init__(self):
        super().__init__()
        self.title("Hello World!")
        self.geometry("600x600")

        self.menu = Menu(self)
        self.mainloop()

        # self.label = ttk.Label(self, text="")
        # self.label.pack()
    # def update_label(self, newText):
    #     self.label["text"] = newText


class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, background='red')

        self.pack()
    #     self.create_widgets()
    #
    # def create_widgets(self):
    #     button_1 = ttk.Button(self, text="Button 1")
    #
    #     entry = ttk.Entry(self)


App()

# def main():
#     """ main game loop """
#     # test player
#     if __name__ == "__main__":
#
#         player = Player('test', 10, 10, current_location)
#
#         App()
#
#         # while True:
#         #     action = action_validator()
#         #     return_action(player, action)
#         #     app.update_label(player.location)
#
#
# main()
