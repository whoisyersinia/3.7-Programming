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

    def __init__(self, name, health, attack, defence, location, coins, inv, weapon, armour, skills):
        super().__init__(name, health, attack, defence, location, coins, inv)

        self._weapon = weapon
        self._armour = armour
        self._skills = skills
        self.max_inv_size = 6
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

    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, new_weapon):
        self._weapon = new_weapon

    @property
    def armour(self):
        return self._armour

    @armour.setter
    def armour(self, new_armour):
        self._armour = new_armour

    @property
    def skills(self):
        return self._skills

    @skills.setter
    def skills(self, new_skills):
        self._skills = new_skills

    # def get_skills(self, skill):
    #     """get skill objects"""
    #     skill_list = []
    #
    #     for item in items:
    #         if item.id in self._item:
    #             new_item_list.append(item)
    #
    #     self._item = new_item_list
    #

    def current_location(self, locations):
        """take the current location and return it as an object from the locations list."""
        for loc in locations:
            if loc.name == self._location:
                return loc

    def check_max_inv(self):
        """checks if player is over the max inventory size"""
        if len(self._inv) > self.max_inv_size:
            print('max')
            return True
        else:
            return False

    def take_item(self, location):
        """take item and add to player inventory"""
        if not self.check_max_inv():
            add_item = location.item[0]
            self._inv.append(add_item)
            print(f"Successfully added {add_item.name} to inventory!")
            location.item.pop(0)
            return add_item.name
        return False

    def unequip_item(self, item):
        """unequip item from inventory"""
        if isinstance(item, Weapon) and self._weapon:
            self._attack -= item.attack
            self._weapon = None
            print(f"Successfully unequipped {item.name}!")
            # elif isinstance(item, Armour):
            #     self._defence += item.defence
            #     self._defence = item
            # elif isinstance(item, Charm):
            #     self._luck += item.luck
            #     self._charm = item
            return True
        else:
            print(f"Item {item.name} cannot be unequipped!")
            return False

    def remove_item(self, item):
        """unequip item from inventory"""
        self._inv.remove(item)

    def equip_item(self, item):
        """equips item and change player attributes"""
        if isinstance(item, Weapon) and not self._weapon:
            self._attack += item.attack
            self._weapon = item
            print(f"Successfully equipped {item.name}!")
            return True
        # elif isinstance(item, Armour):
        #     self._defence += item.defence
        #     self._defence = item
        # elif isinstance(item, Charm):
        #     self._luck += item.luck
        #     self._charm = item
        else:
            print(f"Item {item.name} cannot be equipped!")
            return False


class Enemy(Character):
    def __init__(self, name, health, attack, defence, location, coins, inv):
        super().__init__(name, health, attack, defence, location, coins, inv)

    pass


class Skills:
    pass


class Item:
    """A class representing the items in the game"""

    def __init__(self, item_id, name, desc, value):
        self.id = int(item_id)
        self.name = name
        self.desc = desc
        self.value = int(value)

    def get_item_type(self):
        if isinstance(self, Weapon):
            return "weapon"
        # elif isinstance(self, Armour):
        #     return "armour"
        #


class Weapon(Item):
    """A class inheriting the item class to represent the weapons in the game"""

    def __init__(self, item_id, name, desc, value, attack):
        super().__init__(item_id, name, desc, value)
        self.attack = int(attack)

    @classmethod
    def generate_from_file(cls, in_file):
        with open(in_file) as weapons:
            for weapon in weapons:
                yield Weapon(*weapon.strip().split(","))


class Location:
    """A class representing a location in a game world.

    Attributes:
        _name (str): The name of the location.
        _desc (str): The description of the location.
        _dest (list): A list of possible destinations from the location.
        _npc (bool): Indicates whether the location has a non-player character.
        _item (list): A list of items present in the location.

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

        self.frame_name = None
        self._frame = None
        self.statusbar = None

        self.switch_frame(Inventory)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self.frame_name = frame_class.__name__
        self._frame.grid()
        self.statusbar = StatusBar(self)


class Inventory(ttk.Frame):
    """ frame for the player inventory """

    def __init__(self, parent):
        super().__init__(parent)
        self.player = parent.player
        self.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(list(range(3)), weight=1, uniform="Silent_Creme")
        self.rowconfigure(list(range(5)), weight=1)
        self.rowconfigure(6, weight=3)
        self.name = None
        self.stats = None
        self.equipped_weapon = None
        self.equipped_armour = None
        self.skills = None
        self.item_name = None
        self.item_desc = None
        self.item_attack = None
        self.equip_button = None
        self.unequip_button = None
        self.item_value = None
        self.no_item_msg = None
        self.destroy_item_button = None
        self.item_widget = []
        self.create_widgets()
        self.create_item_widget()

    def create_widgets(self):
        """ create widgets for the inventory frame """
        self.name = ttk.Label(self, text=self.player.name, style="info.TLabel", font="Apple 30 bold")
        self.name.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.stats = ttk.Label(self, text=f"Level: ... | {self.player.health} HP | Attack: {self.player.attack} | "
                                          f"Defence: {self.player.defence} | {self.player.coins} coins.",
                               font="Apple 15")
        self.stats.grid(row=1, column=0, columnspan=3)

        eqiupped_title = ttk.Label(self, text="Your Items:", justify="right", style="info.TLabel")
        eqiupped_title.grid(row=2, column=0, columnspan=3, pady=(10, 5))
        if self.player.weapon:
            self.equipped_weapon = ttk.Label(self, text=f"Weapon: {self.player.weapon.name}")
        else:
            self.equipped_weapon = ttk.Label(self, text=f"Weapon: Your bare fists!")

        self.equipped_weapon.grid(row=3, column=0, columnspan=3)
        if self.player.armour:
            self.equipped_armour = ttk.Label(self, text=f"Armour: {self.player.armour.name}")
        else:
            self.equipped_armour = ttk.Label(self, text=f"Armour: Leisure Club Hoodie")
        self.equipped_armour.grid(row=4, column=0, columnspan=3)
        self.skills = ttk.Label(self, text=f"Skills: {self.player.skills}")
        self.skills.grid(row=5, column=0, columnspan=3)

        ttk.Separator(self, orient='horizontal').grid(row=10, column=0, columnspan=3, sticky="nsew", pady=(10, 3))

        inventory = ttk.Label(self, text="Inventory:", style="info.TLabel", justify="center",
                              font="Apple 20 bold")
        inventory.grid(row=11, column=0, columnspan=3, pady=(0, 5))

    def create_item_widget(self):
        row_num = 0
        col_num = 0
        item_num = 0

        for item in self.player.inv:
            if col_num == 0:
                row_num = 0
            elif col_num % 3 == 0:
                row_num += 5
                col_num = 0

            self.item_name = ttk.Label(self, text=f"{item.name}", style="success.TLabel", justify="left",
                                       font="Helvetica 15")
            self.item_name.grid(row=12 + row_num, column=col_num)
            self.item_widget.append(self.item_name)

            self.item_desc = ttk.Label(self, text=f"{item.desc}", style="primary.TLabel", justify="left",
                                       font="Helvetica 10")
            self.item_desc.grid(row=13 + row_num, column=col_num)
            self.item_widget.append(self.item_desc)

            if item.get_item_type() == "weapon":
                self.item_attack = ttk.Label(self, text=f"Attack +{item.attack}", style="primary.TLabel",
                                             justify="left", font="Helvetica 15")
                self.item_attack.grid(row=14 + row_num, column=col_num)
                self.item_widget.append(self.item_attack)

                if self.player.weapon == item:
                    self.unequip_button = ttk.Button(self, text="Unequip", style="danger.Outline.TButton", width=10,
                                                     command=lambda items=item: self.unequip_item(items))
                    self.unequip_button.grid(row=16 + row_num, column=col_num, pady=(0, 50))
                    self.item_widget.append(self.unequip_button)
                elif not self.player.weapon:
                    self.equip_button = ttk.Button(self, text="Equip", style="success.Outline.TButton", width=4,
                                                   command=lambda items=item:
                                                   self.equip_item(items))
                    self.equip_button.grid(row=16 + row_num, column=col_num, pady=(0, 50))
                    self.item_widget.append(self.equip_button)
                else:
                    self.destroy_item_button = ttk.Button(self, text="Remove", style="danger.TButton", width=6,
                                                          command=lambda items=item: self.remove_item(items))
                    self.destroy_item_button.grid(row=16 + row_num, column=col_num, pady=(0, 50))
                    self.item_widget.append(self.destroy_item_button)

            self.item_value = ttk.Label(self, text=f"Sell for: {item.value} coins", style="primary.TLabel",
                                        justify="left", font="Helvetica 15")
            self.item_value.grid(row=15 + row_num, column=col_num)
            self.item_widget.append(self.item_value)
            col_num += 1
            item_num += 1

        if not self.player.inv:
            self.no_item_msg = ttk.Label(self, text="You have no items", style="info.TLabel", font="Apple 15 bold")
            self.no_item_msg.grid(row=12, column=0, columnspan=3, pady=(0, 300))

    def destroy_item_widget(self):
        for widget in self.item_widget:
            widget.destroy()

    def remove_item(self, item):
        """removes item from inv"""
        self.player.remove_item(item)
        self.destroy_item_widget()
        self.create_item_widget()
        self.update_widgets()

    def equip_item(self, item):
        """equip item from equip button"""
        self.player.equip_item(item)
        self.destroy_item_widget()
        self.create_item_widget()
        self.update_widgets()

    def unequip_item(self, item):
        """equip item from equip button"""
        self.player.unequip_item(item)
        self.destroy_item_widget()
        self.create_item_widget()
        self.update_widgets()

    def update_widgets(self):
        self.stats.config(text=f"Level: ... | {self.player.health} HP | Attack: {self.player.attack} | "
                               f"Defence: {self.player.defence} | {self.player.coins} coins.")
        self.skills.config(text=f"Skills: {self.player.skills}")
        if self.player.weapon:
            self.equipped_weapon.config(text=f"Weapon: {self.player.weapon.name}")
        else:
            self.equipped_weapon.config(text=f"Weapon: Your bare fists")
        if self.player.armour:
            self.equipped_armour.config(text=f"Armour: {self.player.armour.name}")
        else:
            self.equipped_armour.config(text=f"Armour: Leisure Club Hoodie")
        if not self.player.inv:
            self.no_item_msg = ttk.Label(self, text="You have no items", style="info.TLabel", font="Apple 15 bold")
            self.no_item_msg.grid(row=12, column=0, columnspan=3, pady=(0, 300))
        else:
            if self.no_item_msg:
                self.no_item_msg.destroy()


class Menu(ttk.Frame):
    """main menu for player interaction"""

    def __init__(self, parent):
        super().__init__(parent)
        self.locations = parent.locations
        self.player = parent.player
        self.current_location = parent.current_location

        self.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(list(range(3)), weight=1, uniform="Silent_Creme")
        self.rowconfigure(list(range(5)), weight=1)
        self.rowconfigure(6, weight=3)

        self.label_location = tk.Label(self, text=f"Location: {self.player.location}", font="Helvetica", fg='#FF0000')
        self.label_location.grid(row=0, column=0, sticky="nsew", columnspan=3)

        self.info_location = tk.Label(self, text=f"You are in {self.current_location.desc}", font="Helvetica")
        self.info_location.grid(row=1, column=0, sticky="nsew", columnspan=3)

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
            self.can_take()
            self.buttons.append(self.take_button)

    def can_take(self):
        if self.player.check_max_inv():
            self.take_button.config(state="disabled", text="Max inventory!")

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
            self.can_take()

            self.take_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=1, pady=50, sticky="nsew", columnspan=1)
            self.buttons.append(self.take_button)


class StatusBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.player = parent.player
        self.parent = parent
        print("Current Frame:", parent.frame_name)

        if parent.frame_name == "Menu":
            self.inv = ttk.Button(parent, text=f"Open {self.player.name}'s Inventory",
                                  command=lambda: self.switch_frame(Inventory))
            self.inv.grid(row=6, column=0, sticky="nsew")

        if parent.frame_name == "Inventory":
            self.inv = ttk.Button(parent, text=f"Back to game", style="danger.Outline.TButton",
                                  command=lambda: self.switch_frame(Menu))
            self.inv.grid(row=6, column=0, sticky="nsew")

        self.grid(row=6, column=0, sticky="nsew")

    def switch_frame(self, frame):
        """switch the frame"""
        self.parent.switch_frame(frame)
        self.inv.destroy()


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
    player = Player('test', 100, 10, 10, "A", 10,
                    [Weapon(0, "hi", "hi", 0, 0)], None, None, [])
    weapons = Weapon.generate_from_file("items.txt")
    locations = [Location(**loc) for loc in LOC_LIST]
    for location in locations:
        location.link_item(weapons)

    app = App(player, locations)
    app.mainloop()


if __name__ == '__main__':
    main()
