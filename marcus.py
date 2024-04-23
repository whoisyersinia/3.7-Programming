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

# from pprint import pprint

NPC_DIALOGUE = [{"name": "Test", "": ""}]

# TODO finish map
LOC_LIST = [{"name": "A", "desc": "Start", "dest": ["B", "C", "D"], "npc": "Test", "item": [1]},
            {"name": "B", "desc": "Path", "dest": ["C", "D"], "npc": "Hi", "item": ""},
            {"name": "C", "desc": "Path 2", "dest": ["D"], "npc": "", "item": ""},
            {"name": "D", "desc": "End", "dest": ["A"], "npc": "", "item": ""}]


class Character:
    """
    Represents a character in the game.

    Attributes:
        _name (str): The name of the character.
        _attack (int): The attack power of the character.
        _defence (int): The defence power of the character.
        _location (str): The current location of the character.
    """

    def __init__(self, name, health, attack, defence, location, coins, inv):
        self._name = name
        self._health = health
        self._attack = attack
        self._defence = defence
        self._location = location
        self._coins = coins
        self._inv = inv


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

    def __init__(self, name, health, attack, defence, location, coins, inv):
        super().__init__(name, health, attack, defence, location, coins, inv)
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
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, new_coins):
        self._inv = new_coins

    @property
    def inv(self):
        return self._inv

    @inv.setter
    def inv(self, new_inv):
        self._inv = new_inv

    def current_location(self, locations):
        """take the current location and return it as an object from the locations list."""
        for loc in locations:
            if loc.name == self._location:
                return loc

    def take_item(self, location):
        """take item and add to player inventory"""
        add_item = location.item[0]
        self._inv.append(add_item)
        print(f"Successfully added {add_item.name} to inventory!")
        location.item.pop(0)
        return add_item.name


class Enemy(Character):
    def __init__(self, name, health, attack, defence, location, coins, inv):
        super().__init__(name, health, attack, defence, location, coins, inv)

    pass


class Item:
    """A class representing the items in the game"""

    def __init__(self, item_id, name, desc, value):
        self.id = int(item_id)
        self.name = name
        self.desc = desc
        self.value = value


class Weapon(Item):
    """A class inheriting the item class to represent the weapons in the game"""

    def __init__(self, item_id, name, desc, value, attack):
        super().__init__(item_id, name, desc, value)
        self.attack = attack

    @classmethod
    def generate_from_file(cls, in_file):
        with open(in_file) as weapons:
            for weapon in weapons:
                yield Weapon(*weapon.strip().split(","))


class Location:
    """A class representing a location in a game world.

    Attributes:
        name (str): The name of the location.
        desc (str): The description of the location.
        dest (list): A list of possible destinations from the location.
        npc (bool): Indicates whether the location has a non-player character.
        item (list): A list of items present in the location.

    Methods:
        check_npc(): Checks if the location has a non-player character.
        dest_name(map_dest): Returns a list of destination names based on the given map.
        print_location_info(dest_list): Prints the location information, including name, description, and possible
        destinations.
    """

    def __init__(self, name, desc, dest, npc, item):
        self._name = name
        self._desc = desc
        self._dest = dest
        self._npc = npc
        self._item = item

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, new_desc):
        self._desc = new_desc

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, new_dest):
        self._dest = new_dest

    @property
    def npc(self):
        return self._npc

    @npc.setter
    def npc(self, new_npc):
        self._npc = new_npc

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, new_item):
        self._item = new_item

    @item.deleter
    def item(self):
        del self._item

    def link_item(self, items):
        """link item id to item object"""
        new_item_list = []

        for item in items:
            if item.id in self._item:
                new_item_list.append(item)

        self._item = new_item_list

    def check_npc(self):
        """Check if the current location has a non-player character.

        Returns:
            bool: True if the location has a non-player character, False otherwise.
        """
        if self._npc:
            return True
        return False

    def check_item(self):
        """Check if the current location has an item.

        Returns:
            bool: True if the location has an item, False otherwise.
        """
        if self._item:
            return True
        return False

    def dest_name(self, locations):
        """Maps the desc of the destinations to the id (name) based on the given map.

        Args:
            locations (list): A list of locations objects.

        Returns:
            dict: A dict of destination names mapped to its id.
        """
        dest_dict = dict()
        for location in locations:
            if location.name in self._dest:
                if location.name in dest_dict:
                    dest_dict[location.name].append(location.desc)
                else:
                    dest_dict[location.name] = location.desc

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
        if self.check_npc() and self.check_item():
            return (f'You moved to {self.desc}.\nYou can move to {dest}.\nSomeone is waving at you!\n'
                    f'There is an item here!\n\n')
        elif self.check_item():
            return f'You moved to {self.desc}.\nYou can move to {dest}.There is an item here!\n\n'
        elif self.check_npc():
            return f'You moved to {self.desc}.\nYou can move to {dest}.\nSomeone is waving at you!\n\n'
        else:
            return f'You moved to {self.desc}.\nYou can move to {dest}.\n\n'


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
        self.player = player
        self.locations = location
        self.current_location = self.player.current_location(self.locations)

        self.style = tb.Style(theme="darkly")
        self.geometry("600x600")
        self.resizable(False, False)
        self.title("Hello World!")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._frame = None

        self.switch_frame(Menu)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


class Menu(ttk.Frame):
    """main menu for player interaction"""

    def __init__(self, parent):
        super().__init__(parent)

        self.locations = parent.locations
        self.player = parent.player
        self.current_location = parent.current_location

        self.statusbar = StatusBar(self)

        self.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(list(range(3)), weight=1, uniform="Silent_Creme")
        self.rowconfigure(list(range(5)), weight=1)
        self.rowconfigure(6, weight=3)

        self.label_location = tk.Label(self, text=f"Location: {self.player.location}", font="Helvetica", fg='#FF0000')
        self.label_location.grid(row=0, column=0, sticky="nsew", columnspan=3)

        self.info_location = tk.Label(self, text=f"You are in {self.current_location.desc}", font="Helvetica")
        self.info_location.grid(row=1, column=0, sticky="nsew", columnspan=3)

        # self.info = ttk.Label(self, text="Nothing currently happening...", font="Helvetica", style="info.TLabel",
        #                       background="black", padding=5, justify="center", borderwidth=2, relief="solid")

        self.info = tk.Text(self, height=10, relief="ridge", font="Helvetica", state="disabled")
        self.info.grid(row=2, column=0, pady=(10, 20), columnspan=3)

        self.dest = self.current_location.dest_name(self.locations)

        self.buttons = []
        self.move_header = ttk.Label(self, text="Where to?", font="Helvetica", style="info.TLabel")
        self.move_header.grid(row=3, column=0, pady=(0, 5), columnspan=3)

        col_num = 0
        for i in range(len(self.dest)):
            if i == 0:
                col_num = 1
            else:
                col_num = 0

        for dest_id, dest_desc in self.dest.items():
            self.move_button = ttk.Button(self, style="primary.Outline.TButton", text=f"Move to {dest_desc}",
                                          command=lambda dest=dest_id: self.move(dest))
            self.move_button.grid(row=4, ipadx=10, ipady=2, padx=4, pady=50, column=col_num, sticky="nsew",
                                  columnspan=1)
            col_num += 1
            self.buttons.append(self.move_button)

        if not self.current_location.check_npc() and not self.current_location.check_item():
            self.filler = tk.Label(self)
            self.filler.grid(row=5, column=0, pady=60)

        if self.current_location.check_npc():
            self.talk_button = ttk.Button(self, style="success.Outline.TButton", text=f"Talk")
            self.talk_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=0, pady=50, sticky="nsew", columnspan=1)
            self.buttons.append(self.talk_button)

        if self.current_location.check_item():
            self.take_button = ttk.Button(self, style="success.Outline.TButton", text=f"Take Item(s)",
                                          command=lambda: self.take_item())
            self.take_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=1, pady=50, sticky="nsew", columnspan=1)
            self.buttons.append(self.take_button)

    def move(self, dest):
        """moves the player"""
        self.player.location = dest
        self.current_location = self.player.current_location(self.locations)
        self.info.grid(row=2)
        self.label_location.config(text=f"Location: {self.player.location}")
        self.info_location.config(text=f"You are in {self.current_location.desc}")
        self.dest = self.current_location.dest_name(self.locations)
        self.info.config(state="normal")
        self.info.insert(tk.END, self.current_location.print_location_info(self.dest))
        self.info.config(state="disabled")
        self.info.see("end")

        self.update_widgets()

    def take_item(self):
        item_name = self.player.take_item(self.current_location)
        add_item_prompt = f"Successfully added {item_name} to inventory!\n\n"
        self.info.config(state="normal")
        self.info.insert(tk.END, add_item_prompt)
        self.info.config(state="disabled")
        self.info.see("end")
        self.update_widgets()

    def update_widgets(self):
        """update widgets"""

        for b in self.buttons:
            b.destroy()
        self.buttons.clear()

        col_num = 0
        for i in range(len(self.dest)):
            if i == 0:
                col_num = 1
            else:
                col_num = 0

        for dest_id, dest_desc in self.dest.items():
            self.move_button = ttk.Button(self, style="primary.Outline.TButton", text=f"Move to {dest_desc}",
                                          command=lambda dest=dest_id: self.move(dest))
            self.move_button.grid(row=4, ipadx=10, ipady=2, padx=4, pady=50, column=col_num, sticky="nsew",
                                  columnspan=1)
            col_num += 1
            self.buttons.append(self.move_button)

            self.statusbar = StatusBar(self)

        if not self.current_location.check_npc() and not self.current_location.check_item():
            self.filler = tk.Label(self)
            self.filler.grid(row=5, column=0, pady=60)

        if self.current_location.check_npc():
            self.talk_button = ttk.Button(self, style="success.Outline.TButton", text=f"Talk")
            self.talk_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=0, pady=50, sticky="nsew", columnspan=1)
            self.buttons.append(self.talk_button)

        if self.current_location.check_item():
            self.take_button = ttk.Button(self, style="success.Outline.TButton", text=f"Take Item(s)",
                                          command=lambda: self.take_item())

            self.take_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=1, pady=50, sticky="nsew", columnspan=1)
            self.buttons.append(self.take_button)


class StatusBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.location = parent.location
        self.player = parent.player

        self.health = ttk.Label(parent, text=f"{self.player.health} HP", font="Helvetica",
                                style="secondary.Inverse.TLabel")
        self.health.grid(row=6, column=0, sticky="nsew", columnspan=3)

        self.attack = ttk.Label(parent, text=f"{self.player.coins} coins", font="Helvetica",
                                style="secondary.Inverse.TLabel", justify="center")
        self.attack.grid(row=6, column=1, sticky="nsew", columnspan=3)

        self.name = ttk.Button(parent, text=f"{self.player.name}")
        self.name.grid(row=6, column=2, sticky="nsew", columnspan=3)
        self.grid(row=1, column=0, sticky="nsew")


# class PlayerStatsMenu(ttk.Frame):
#     def __init__(self, parent, player):
#         super().__init__(parent)
#         self.player = player
#         self.bg = tk.Label(text="red")
#         self.bg.grid(row=0, column=2, sticky="e")
#         self.grid()


def main():
    """ Main game loop """
    # test player
    player = Player('test', 100, 10, 10, "A", 10, [])
    weapons = Weapon.generate_from_file("items.txt")
    locations = [Location(**loc) for loc in LOC_LIST]
    for location in locations:
        location.link_item(weapons)

    app = App(player, locations)
    app.mainloop()


if __name__ == '__main__':
    main()
