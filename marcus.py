"""
An RPG text-adventure game written in Python with a GUI using Tkinter.
Made for the 3.7 Assessment Standard in NCEA Level 3.
Copyright (c)

Github: https://github.com/whoisyersinia/3.7-Programming
Author: Marcus Demafeliz
Date: 30 March 2024
"""

import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk

NPC_DIALOGUE = [{"name": "Test", "": ""}]

# TODO create map
LOC_LIST = [{"name": "A", "desc": "Start", "dest": ["B", "C", "D"], "npc": "Test", "items": ""},
            {"name": "B", "desc": "Path", "dest": ["C", "D"], "npc": "Hi", "items": ""},
            {"name": "C", "desc": "Path 2", "dest": ["D"], "npc": "", "items": ""},
            {"name": "D", "desc": "End", "dest": ["A"], "npc": "", "items": ""}]

current_location = "A"


class Character:
    """
    Represents a character in the game.

    Attributes:
        _name (str): The name of the character.
        _attack (int): The attack power of the character.
        _defence (int): The defence power of the character.
        _location (str): The current location of the character.
    """

    def __init__(self, name, health, attack, defence, location):
        self._name = name
        self._health = health
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

    def __init__(self, name, health, attack, defence, location, inv=None):
        super().__init__(name, health, attack, defence, location)
        self._inv = inv
        # xp
        # luck

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new_health):
        self._health = new_health

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, new_attack):
        self._attack = new_attack

    @property
    def defence(self):
        return self._defence

    @defence.setter
    def defence(self, new_defence):
        self._defence = new_defence

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, new_location):
        self._location = new_location

    @property
    def inv(self):
        return self._inv

    @inv.setter
    def inv(self, new_inv):
        self._inv = new_inv

    def get_loc_info(self):
        for loc in LOC_LIST:
            if loc["name"] == self._location:
                location = Location(**loc)
                return location

    @staticmethod
    def print_help():
        return print(f"To move: move or m\n"
                     f"To exit: exit\n")


class Enemy(Character):
    def __init__(self, name, health, attack, defence, location):
        super().__init__(name, health, attack, defence, location)

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
        """Maps the desc of the destinations to the id (name) based on the given map.

        Args:
            map_dest (list): A list of destination dictionaries.

        Returns:
            dict: A dict of destination names mapped to its id.
        """
        dest_dict = dict()
        for dest in map_dest:
            if dest["name"] in self._dest:
                if dest["name"] in dest_dict:
                    dest_dict[dest["name"]].append(dest["desc"])
                else:
                    dest_dict[dest["name"]] = dest["desc"]

        return dest_dict

    def print_location_info(self, dest_dict):
        """Print the location information, including name, description, and possible destinations.

        Args:
            dest_dict (dict): A dict of destinations.

        Returns:
            str: The formatted location information.
        """
        dest_list_names = [dest_desc for dest_desc in dest_dict.values()]

        dest = ", ".join(dest_list_names)
        if self.check_npc():
            return (f'You moved to {self._desc}.\nYou can move to {dest}.\nSomeone is waving at you!\n'
                    f'(Talk)')
        else:
            return f'You moved to {self._desc}.\nYou can move to {dest}.\n '


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


class App(tk.Tk):
    """ Main application gui """

    def __init__(self, player, location):
        super().__init__()
        self.style = tb.Style(theme="darkly")
        self.title("Hello World!")
        self.geometry("600x600")
        self.menu = Menu(self, player, location)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)


class Menu(ttk.Frame):
    """main menu for player interaction"""

    def __init__(self, parent, player, location):
        super().__init__(parent)

        self.location = location
        self.player = player

        self.label_location = tk.Label(self, text=f"Location: {self.player.location}", font="Helvetica", fg='#FF0000')
        self.label_location.grid(row=0, column=0, sticky="ew", columnspan=3)

        self.info_location = tk.Label(self, text=f"You are in {self.location.desc}", font="Helvetica")
        self.info_location.grid(row=1, column=0, sticky="ew", columnspan=3)

        self.info = ttk.Label(self, text="Nothing currently happening...", font="Helvetica", style="info.TLabel",
                              background="black", padding=5, justify="center", borderwidth=2, relief="solid")
        self.info.grid(row=2, column=0, pady=(10, 20), columnspan=3)

        self.dest = self.location.dest_name(LOC_LIST)

        self.buttons = []
        self.move_header = ttk.Label(self, text="Where to?", font="Helvetica", style="info.TLabel")
        self.move_header.grid(row=3, column=0, pady=(0, 5), columnspan=3)
        i = 0
        for dest_id, dest_desc in self.dest.items():
            self.move_button = ttk.Button(self, style="primary.Outline.TButton", text=f"Move to {dest_desc}",
                                          command=lambda dest=dest_id: self.move(dest))
            self.move_button.grid(row=4, ipadx=10, ipady=2, padx=5, column=0 + i, sticky="nsew")
            i += 1
            self.buttons.append(self.move_button)

        self.grid()

    def move(self, dest):
        """moves the player"""
        self.player.location = dest
        self.location = self.player.get_loc_info()
        self.info.config(text=f"{self.location.print_location_info(self.dest)}")
        self.info.grid(row=2)
        self.update_widgets()

    def update_widgets(self):
        """update widgets"""
        self.label_location.config(text=f"Location: {self.player.location}")
        self.info_location.config(text=f"You are in {self.location.desc}")
        for b in self.buttons:
            b.destroy()
        self.buttons.clear()

        self.dest = self.location.dest_name(LOC_LIST)
        self.info.config(text=f"{self.location.print_location_info(self.dest)}")
        i = 0
        for dest_id, dest_desc in self.dest.items():
            self.move_button = ttk.Button(self, style="primary.Outline.TButton", text=f"Move to {dest_desc}",
                                          command=lambda dest=dest_id: self.move(dest))
            self.move_button.grid(row=4, ipadx=10, ipady=2, padx=5, column=0 + i, sticky="nsew")
            i += 1
            self.buttons.append(self.move_button)


def main():
    """ Main game loop """
    # test player
    player = Player('test', 100, 10, 10, current_location)

    app = App(player, player.get_loc_info())
    app.mainloop()


if __name__ == '__main__':
    main()
