"""
An RPG text-adventure game written in Python with a GUI using Tkinter.
Made for the 3.7 Assessment Standard in NCEA Level 3.
Copyright (c)

Github: https://github.com/whoisyersinia/3.7-Programming
Author: Marcus Demafeliz
Date: 30 March 2024
"""

import sys
import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk
from itertools import islice, chain
import random
import math
import json

# from pprint import pprint

# TODO finish map
LOC_LIST = [{"name": "A", "desc": "Start", "dest": ["B", "C", "D"], "npc": "Arthur", "enemy": [1], "item": [3, 1]},
            {"name": "B", "desc": "Path", "dest": ["C", "D"], "npc": "", "enemy": "", "item": [2]},
            {"name": "C", "desc": "Path 2", "dest": ["D"], "npc": "", "enemy": "", "item": [1]},
            {"name": "D", "desc": "End", "dest": ["A"], "npc": "", "enemy": "", "item": ""}]


class Character:
    """
    Represents a character in the game.

    Attributes:
        _name (str): The name of the character.
        _attack (int): The attack power of the character.
        _defence (int): The defence power of the character.
    """

    def __init__(self, name, level, xp, health, attack, defence, coins, inv, max_hp, spells):
        self._name = name
        self._level = int(level)
        self._xp = int(xp)
        self._health = int(health)
        self._max_hp = int(max_hp)
        self._attack = int(attack)
        self._defence = int(defence)
        self._coins = int(coins)
        self._inv = inv
        self._spells = spells
        self._block = False
        self._buff_duration = 0

        self.attk_buff = 0
        self.def_buff = 0

    @property
    def block(self):
        return self._block

    @property
    def buff_duration(self):
        return int(self._buff_duration)

    @buff_duration.setter
    def buff_duration(self, new_buff_duration):
        self._buff_duration = new_buff_duration

    def is_alive(self):
        """checks if character is still alive"""
        return self._health > 0

    def take_damage(self, raw_damage):
        """takes damage calculating raw_damage - defence"""
        defence = self._defence
        if self._block:
            defence = self._defence * 2
        realised_damage = raw_damage - defence
        math.ceil(realised_damage)
        if realised_damage < 0:
            realised_damage = 0
        self._health -= realised_damage
        return realised_damage

    def action_block(self):
        if not self._block:
            self._block = True
        else:
            self._block = False

    def get_xp(self, xp):
        """add xp"""
        self._xp += xp
        if self._xp >= self.xp_required():
            self.level_up()
            return True

    def level_up(self):
        """level up character if xp meets threshold"""
        self._xp = self._xp - self.xp_required()
        self._level += 1
        self._attack += 2
        self._defence += 1
        if self._level % 5 == 0:
            self._max_hp += 20

    def xp_required(self):
        """calculates the amount of xp required for level up"""
        if self._level == 1:
            xp_required = 1
        else:
            xp_required = 100 + (self._level * 50)
        return int(xp_required)

    def link_spells(self):
        """link item id to item object"""
        new_spell_list = []
        for i in range(len(ALL_SPELLS)):
            for spell_id in self._spells:
                if spell_id == ALL_SPELLS[i].id:
                    new_spell_list.append(ALL_SPELLS[i])

        self._spells = new_spell_list

    def use_spell(self, spell):
        if isinstance(spell, Buff):
            if self._buff_duration == 0:
                if spell.attack > 0:
                    self._attack += spell.attack
                    self._buff_duration = spell.duration
                    self.attk_buff = spell.attack
                if spell.defence > 0:
                    self._defence += spell.defence
                    self._buff_duration = spell.duration
                    self.def_buff = spell.defence
            else:
                return False
        elif isinstance(spell, Heal):
            if self._health != self._max_hp:
                old_health = self._health
                self._health += spell.health
                if self._health > self._max_hp:
                    self._health = self._max_hp
                print(f"Healed {self._health - old_health} health!")
            else:
                print("Already max health!")
                return False
        return True

    def revert_spell(self):
        self._attack -= self.attk_buff
        self._defence -= self.def_buff
        self.attk_buff = 0
        self.def_buff = 0


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

    def __init__(self, name, level, xp, health, attack, defence, location, coins, inv, weapon, armour, spells,
                 max_hp=20):
        super().__init__(name, level, xp, health, attack, defence, coins, inv, max_hp, spells)

        self._weapon = weapon
        self._armour = armour
        self._location = location
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
    def level(self):
        return self._level

    @property
    def xp(self):
        return self._xp

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
    def spells(self):
        return self._spells

    @spells.setter
    def spells(self, new_spells):
        self._spells = new_spells

    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, new_max_hp):
        self._max_hp = new_max_hp

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
        consumable_list = [item.name for item in self._inv if isinstance(item, Consumable)]
        other_item_list = [item.name for item in self._inv if not isinstance(item, Consumable)]
        consumable_list = set(consumable_list)
        inv_size = len(consumable_list) + len(other_item_list)
        if inv_size > self.max_inv_size:
            return True
        else:
            return False

    def take_item(self, item, location):
        """take item and add to player inventory"""
        if not self.check_max_inv():
            items_in_loc = location.item
            if item in items_in_loc:
                item = item
            add_item = item
            self._inv.append(add_item)
            print(f"Successfully added {add_item.name} to inventory!")
            location.item.remove(item)
            return add_item.name
        return False

    def combat_take_item(self, item):
        """take item from enemy inv"""
        self._inv.append(item)
        print(f"Successfully added {item.name} to inventory!")

    def heal(self, healing):
        """heals the player based on certain amount of health prevent overhealing"""
        if self._health == self._max_hp:
            print("Already max health!")
            return False
        old_health = self._health
        self._health += healing
        if self._health > self._max_hp:
            self.health = self._max_hp
        print(f"Healed {self._health - old_health} health!")

    def use_item(self, item):
        """use item in player inv - only consumable type"""
        print(f"Used {item.name}")
        self._attack += item.attack
        self._defence += item.attack
        self.heal(item.health)
        self._inv.remove(item)

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
    def __init__(self, enemy_id, name, level, xp, health, attack, defence, coins, inv, max_hp, spells):
        super().__init__(name, level, xp, health, attack, defence, coins, inv, max_hp, spells)
        self._id = int(enemy_id)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_level):
        self._level = new_level

    @property
    def xp(self):
        return self._xp

    @xp.setter
    def xp(self, new_xp):
        self._xp = new_xp

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
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, new_coins):
        self._coins = new_coins

    @property
    def inv(self):
        return self._inv

    @inv.setter
    def inv(self, new_inv):
        self._inv = new_inv

    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, new_max_hp):
        self._max_hp = new_max_hp

    @property
    def spells(self):
        return self._spells

    @spells.setter
    def spells(self, new_spells):
        self._spells = new_spells

    @classmethod
    def generate_from_file(cls, in_file):
        """ generate enemies from enemy.csv file """
        with open(in_file, 'r') as enemies:
            for enemy in enemies:
                data = enemy.strip().split(',')

                enemy_id = data[0].strip()
                enemy_name = data[1].strip()
                enemy_level = data[2].strip()

                xp_range = data[3].strip().split('(')[1].split(')')[0].split('-')
                min_xp = int(xp_range[0].strip())
                max_xp = int(xp_range[1].strip())
                enemy_xp = random.randint(min_xp, max_xp)

                health_range = data[4].strip().split('(')[1].split(')')[0].split('-')
                min_health = int(health_range[0].strip())
                max_health = int(health_range[1].strip())
                enemy_health = random.randint(min_health, max_health)

                attack_range = data[5].strip().split('(')[1].split(')')[0].split('-')
                min_attack = int(attack_range[0].strip())
                max_attack = int(attack_range[1].strip())
                enemy_attack = random.randint(min_attack, max_attack)

                defence_range = data[6].strip().split('(')[1].split(')')[0].split('-')
                min_defence = int(defence_range[0].strip())
                max_defence = int(defence_range[1].strip())
                enemy_defence = random.randint(min_defence, max_defence)

                coins_range = data[7].strip().split('(')[1].split(')')[0].split('-')
                min_coins = int(coins_range[0].strip())
                max_coins = int(coins_range[1].strip())
                enemy_coins = random.randint(min_coins, max_coins)

                enemy_inv = [item.strip() for item in data[8].strip().split(';')]

                new_item_list = []
                for i in range(len(ALL_ITEMS)):
                    for item_id in enemy_inv:
                        if int(item_id) == ALL_ITEMS[i].id:
                            new_item_list.append(ALL_ITEMS[i])

                enemy_inv = new_item_list
                enemy_chance = data[9].strip()

                enemy_spells = [item.strip() for item in data[10].strip().split(';')]
                new_spell_list = []
                for i in range(len(ALL_SPELLS)):
                    for spell_id in enemy_spells:
                        if int(spell_id) == ALL_SPELLS[i].id:
                            new_spell_list.append(ALL_SPELLS[i])

                enemy_spells = new_spell_list

                if random.randint(1, int(enemy_chance)) == 1:
                    enemy_inv = random.choice(enemy_inv)
                else:
                    enemy_inv = None

                yield Enemy(enemy_id, enemy_name, enemy_level, enemy_xp, enemy_health, enemy_attack, enemy_defence,
                            enemy_coins, enemy_inv, enemy_health, enemy_spells)


class Spells:
    """A class representing the spells in the game"""

    def __init__(self, spell_id, name, description, cooldown, max_cd):
        self.id = int(spell_id)
        self.name = name
        self.description = description
        self._cooldown = int(cooldown)
        self._max_cd = int(max_cd)

    @property
    def cooldown(self):
        return self._cooldown

    @cooldown.setter
    def cooldown(self, new_cooldown):
        self._cooldown = new_cooldown

    @property
    def max_cd(self):
        return self._max_cd

    @max_cd.setter
    def max_cd(self, new_max_cd):
        self.max_cd = new_max_cd


class Buff(Spells):
    """A class representing the buffs in the game inherited from the spells"""

    def __init__(self, spell_id, name, description, cooldown, attack, defence, duration, max_cd):
        super().__init__(spell_id, name, description, cooldown, max_cd)
        self.attack = int(attack)
        self.defence = int(defence)
        self.duration = int(duration)

    @classmethod
    def generate_from_file(cls, in_file):
        """ generate spells from spells.txt file """
        with open(in_file, 'r') as buffs:
            for buff in islice(buffs, 0, 3):
                yield Buff(*buff.strip().split(","))


class Heal(Spells):
    """A class representing heal spells"""

    def __init__(self, spell_id, name, description, cooldown, health, max_cd):
        super().__init__(spell_id, name, description, cooldown, max_cd)
        self.health = int(health)

    @classmethod
    def generate_from_file(cls, in_file):
        """ generate spells from spells.txt file """
        with open(in_file, 'r') as heals:
            for heal in islice(heals, 7, 8):
                yield Heal(*heal.strip().split(","))


class Item:
    """A class representing the items in the game"""

    def __init__(self, item_id, name, desc, value):
        self.id = int(item_id)
        self.name = name
        self.desc = desc
        self.value = int(value)

    def get_item_type(self):
        """return the item type"""
        if isinstance(self, Weapon):
            return "weapon"
        # elif isinstance(self, Armour):
        #     return "armour"
        elif isinstance(self, Consumable):
            return "consumable"


class Consumable(Item):
    def __init__(self, item_id, name, desc, value, attack, defence, health):
        super().__init__(item_id, name, desc, value)
        self.attack = int(attack)
        self.defence = int(defence)
        self.health = int(health)

    @classmethod
    def generate_from_file(cls, in_file):
        """ generate items from items.txt file """
        with open(in_file, 'r') as consumables:
            for consumable in islice(consumables, 2, 3):
                yield Consumable(*consumable.strip().split(","))


class Weapon(Item):
    """A class inheriting the item class to represent the weapons in the game"""

    def __init__(self, item_id, name, desc, value, attack):
        super().__init__(item_id, name, desc, value)
        self.attack = int(attack)

    @classmethod
    def generate_from_file(cls, in_file):
        """ generate items from items.txt file """
        with open(in_file, 'r') as weapons:
            for weapon in islice(weapons, 0, 2):
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

    def __init__(self, name, desc, dest, npc, enemy, item):
        self._name = name
        self._desc = desc
        self._dest = dest
        self._npc = npc
        self._enemy = enemy
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

    @property
    def enemy(self):
        return self._enemy

    @enemy.setter
    def enemy(self, new_enemy):
        self._enemy = new_enemy

    def link_npc(self):
        """link npc name to npc object"""
        for npc in ALL_NPCS:
            if npc.name == self._npc:
                self._npc = npc

    def link_item(self):
        """link item id to item object"""
        new_item_list = []
        for i in range(len(ALL_ITEMS)):
            for item_id in self._item:
                if item_id == ALL_ITEMS[i].id:
                    new_item_list.append(ALL_ITEMS[i])

        self._item = new_item_list

    def link_enemies(self):
        """link item id to item object"""
        new_enemy_list = []
        for i in range(len(ALL_ENEMIES)):
            for enemy_id in self._enemy:
                if enemy_id == ALL_ENEMIES[i].id:
                    new_enemy_list.append(ALL_ENEMIES[i])

        self._enemy = new_enemy_list

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
            return len(self._item)
        return False

    def check_enemy(self):
        """Check if the current location has an item.

        Returns:
            bool: True if the location has an item, False otherwise.
        """
        if self._enemy:
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
            return f'You moved to {self.desc}.\nYou can move to {dest}.\nThere is an item here!\n\n'
        elif self.check_npc():
            return f'You moved to {self.desc}.\nYou can move to {dest}.\nSomeone is waving at you!\n\n'
        else:
            return f'You moved to {self.desc}.\nYou can move to {dest}.\n\n'


class NPC:
    def __init__(self, name, dialogue_tree):
        """
        Initializes an instance of the NPC class.
        """
        self.name = name
        self.dialogue_tree = dialogue_tree

    @classmethod
    def generate_from_file(cls, filename):
        with open(filename, "r") as file:
            dialogue_tree = json.load(file)
            for npc_name, dialogue_tree in dialogue_tree.items():
                yield NPC(npc_name, dialogue_tree)


class App(tk.Tk):
    """ Main application gui """

    def __init__(self, player, location):
        super().__init__()
        self.player = player
        self.locations = location
        self.previous_frame = ["MainMenu"]

        self.style = tb.Style(theme="darkly")
        self.geometry("600x600")
        self.resizable(False, False)
        self.title("Hello World!")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame_name = None
        self._frame = None
        self.statusbar = None

        self.switch_frame(MainMenu)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self.save_info()
            self._frame.destroy()
        self._frame = new_frame
        self.frame_name = frame_class.__name__
        self._frame.grid()
        self.open_info()
        self.statusbar = StatusBar(self)

    def save_info(self):
        """save text in info box"""
        if self.frame_name == "Menu":
            text_file = open("infosave.txt", "w")
            text_file.write(self._frame.info.get(1.0, tk.END))
            text_file.close()

    def open_info(self):
        """open_info"""
        if self.frame_name == "Menu":
            text_file = open("infosave.txt", "r")
            content = text_file.read()
            self._frame.info.config(state="normal")
            self._frame.info.insert(1.0, content)
            self._frame.info.config(state="disabled")
            self._frame.info.see("end")
            text_file.close()

    @staticmethod
    def update_info_widget(text):
        text_file = open("infosave.txt", "a")
        text_file.write(f"{text}\n")
        text_file.close()


class Inventory(ttk.Frame):
    """ frame for the player inventory """

    def __init__(self, parent):
        super().__init__(parent)
        self.player = parent.player
        self.parent = parent
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
        self.item_health = None
        self.equip_button = None
        self.unequip_button = None
        self.use_button = None
        self.item_value = None
        self.no_item_msg = None
        self.destroy_item_button = None
        self.item_widget = []
        self.cons_list = [item.name for item in self.player.inv if isinstance(item, Consumable)]
        self.create_widgets()
        self.create_item_widget()

    def create_widgets(self):
        """ create widgets for the inventory frame """
        self.name = ttk.Label(self, text=f"LV.{self.player.level} {self.player.name}", style="info.TLabel",
                              font="Apple 30 bold")
        self.name.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.stats = ttk.Label(self,
                               text=f"XP {self.player.xp}/{self.player.xp_required()}  | HP {self.player.health}/{self.player.max_hp} | Attack: {self.player.attack} | Defence: {self.player.defence} | {self.player.coins} coins.",
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
        self.skills = ttk.Label(self, text=f"Skills: {self.player.spells[0].name}")
        self.skills.grid(row=5, column=0, columnspan=3)

        ttk.Separator(self, orient='horizontal').grid(row=10, column=0, columnspan=3, sticky="nsew", pady=(10, 3))

        inventory = ttk.Label(self, text="Inventory:", style="info.TLabel", justify="center",
                              font="Apple 20 bold")
        inventory.grid(row=11, column=0, columnspan=3, pady=(0, 5))

    def create_item_widget(self):
        """creates the item widgets"""
        row_num = 0
        col_num = 0
        duplicate_consumables_widgets = []

        for item in self.player.inv:
            if col_num == 0:
                row_num = 0
            elif col_num % 3 == 0:
                row_num += 5
                col_num = 0

            if item.get_item_type() == "weapon":
                self.create_weapon_item_widget(item, row_num, col_num)
                col_num += 1

            elif item.get_item_type() == "armour":
                pass

            elif item.get_item_type() == "consumable":
                uses = self.cons_list.count(item.name)
                if item.name not in duplicate_consumables_widgets:
                    if uses > 1:
                        self.create_consumable_item_widget(item, row_num, col_num, False, uses)
                        duplicate_consumables_widgets.append(item.name)
                        col_num += 1
                    else:
                        self.create_consumable_item_widget(item, row_num, col_num, True, uses)
                        col_num += 1

        if not self.player.inv:
            self.no_item_msg = ttk.Label(self, text="You have no items", style="info.TLabel", font="Apple 15 bold")
            self.no_item_msg.grid(row=12, column=0, columnspan=3, pady=(0, 300))

    def create_item_info_widget(self, item, row_num, col_num):
        """ create the widget for the item's basic info """
        self.item_name = ttk.Label(self, text=f"{item.name}", style="success.TLabel", justify="left",
                                   font="Helvetica 18")
        self.item_name.grid(row=12 + row_num, column=col_num)
        self.item_widget.append(self.item_name)

        self.item_desc = ttk.Label(self, text=f"{item.desc}", style="info.TLabel", justify="left",
                                   font="Helvetica 12", )
        self.item_desc.grid(row=13 + row_num, column=col_num)
        self.item_widget.append(self.item_desc)
        self.item_value = ttk.Label(self, text=f"Sell for: {item.value} coins", style="primary.TLabel",
                                    justify="left", font="Helvetica 12")
        self.item_value.grid(row=15 + row_num, column=col_num)
        self.item_widget.append(self.item_value)

    def create_consumable_item_widget(self, item, row_num, col_num, one_use, uses):
        """create widgets for consumable items"""
        self.create_item_info_widget(item, row_num, col_num)
        if not one_use:
            self.use_button = ttk.Button(self, text=f"Use - {uses}", style="info.TButton", width=10,
                                         command=lambda items=item: self.use_item(items, uses))
        else:
            self.use_button = ttk.Button(self, text="Use", style="info.TButton", width=10,
                                         command=lambda items=item: self.use_item(items, uses))

        self.use_button.grid(row=16 + row_num, column=col_num, pady=(0, 50))
        self.item_widget.append(self.use_button)
        self.check_max_health(item)

    def check_max_health(self, item):
        """checks if the player is at max health and disable use button if true"""
        if item.health > 0 and self.player.health >= self.player.max_hp:
            self.use_button.config(text=f"Already at max HP!", state="disabled", width=13)

    def create_weapon_item_widget(self, item, row_num, col_num):
        self.create_item_info_widget(item, row_num, col_num)
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

    def destroy_item_widget(self):
        """destroy widgets item widgets"""
        for widget in self.item_widget:
            widget.destroy()

    def use_item(self, item, uses):
        """use item and configure the widgets"""
        self.player.use_item(item)
        if uses < 1:
            self.destroy_item_widget()
            self.create_item_widget()
        else:
            self.cons_list.remove(item.name)
            uses = self.cons_list.count(item)
            self.use_button.config(text=f"Use - {uses}")
            self.destroy_item_widget()
            self.create_item_widget()
            self.parent.update_info_widget(f"You used {item.name}")
        self.update_widgets()

    def remove_item(self, item):
        """removes item from inv"""
        self.player.remove_item(item)
        self.destroy_item_widget()
        self.create_item_widget()
        self.update_widgets()
        self.parent.update_info_widget(f"You discarded {item.name}")

    def equip_item(self, item):
        """equip item from equip button"""
        self.player.equip_item(item)
        self.destroy_item_widget()
        self.create_item_widget()
        self.update_widgets()
        self.parent.update_info_widget(f"You equipped {item.name}")

    def unequip_item(self, item):
        """equip item from equip button"""
        self.player.unequip_item(item)
        self.destroy_item_widget()
        self.create_item_widget()
        self.update_widgets()
        self.parent.update_info_widget(f"You unequipped {item.name}")

    def update_widgets(self):
        """updates the current state of widgets"""
        self.stats.config(text=f"Level: ... | {self.player.health} HP | Attack: {self.player.attack} | "
                               f"Defence: {self.player.defence} | {self.player.coins} coins.")
        self.skills.config(text=f"Skills: {self.player.spells[0]}")
        if self.player.weapon:
            self.equipped_weapon.config(text=f"Weapon: {self.player.weapon.name}")
        else:
            self.equipped_weapon.config(text=f"Weapon: Your bare fists!")
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


class GameOver(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.font = "VCR OSD MONO"

        self.game_over = ttk.Label(text="Game Over", font=(self.font, 40), style="danger.TLabel")
        self.game_over.grid(row=0, column=0)


class CombatScreen(ttk.Frame):
    """tk frame for the combat """

    def __init__(self, parent):
        super().__init__(parent)
        self.locations = parent.locations
        self.player = parent.player
        self.current_location = self.player.current_location(self.locations)
        self.parent = parent
        self.enemy = self.current_location.enemy[0]
        self.turn = 0
        self.default_menu = []
        self.spells_button = []
        self.font = "VCR OSD MONO"
        self.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(list(range(3)), weight=1, uniform="Silent_Creme")
        self.rowconfigure(list(range(5)), weight=1)
        self.rowconfigure(6, weight=3)

        self.spells = None
        self.flee = None
        self.block = None
        self.basic_attack = None
        self.actions = ttk.Label(self, text=f"Actions", font=(self.font, 20), style="info.TLabel")
        self.player_attack = ttk.Label(self, text=f"{self.player.attack} ATK", font=(self.font, 16))
        self.player_attack.grid(row=4, column=1)
        self.player_defence = ttk.Label(self, text=f"{self.player.defence} DEF", font=(self.font, 16))
        self.player_defence.grid(row=4, column=2)
        self.player_health = None
        self.player_name = tk.Label(self, text=f"{self.player.name}'s Stats", font=(self.font, 20))
        self.player_name.grid(row=3, column=1)
        self.enemy_defence = ttk.Label(self, text=f"{self.enemy.defence} DEF", font=(self.font, 16))
        self.enemy_attack = ttk.Label(self, text=f"{self.enemy.attack} ATK", font=(self.font, 16))
        self.enemy_health = None
        self.fight = tk.Label(self, text=f"LV.{self.enemy.level} {self.enemy.name}", font=(self.font, 24),
                              fg='#FF0000')
        self.spell = None
        self.info = tk.Text(self, height=10, relief="ridge", font="Helvetica", state="disabled")
        self.info.grid(row=2, column=0, pady=(10, 20), columnspan=3)

        self.create_widgets()

    def create_widgets(self):
        for b in self.spells_button:
            b.destroy()

        if self.enemy.buff_duration > 0:
            self.fight.config(text=f"LV.{self.enemy.level} {self.enemy.name}\n"
                                   f"Buff duration: {self.enemy.buff_duration} turn(s)")
        else:
            self.fight.config(text=f"LV.{self.enemy.level} {self.enemy.name}\n")
        self.fight.grid(row=0, column=0, sticky="nsew", columnspan=3, pady=(0, 10))

        self.enemy_health = tk.Label(self, text=f"HP {self.enemy.health}/{self.enemy.max_hp}", font=(self.font, 16))
        self.enemy_health.grid(row=1, column=0, sticky="nsew")

        self.enemy_attack.grid(row=1, column=1)

        self.enemy_defence.grid(row=1, column=2)

        if not self.buff_active():
            self.player_name.config(text=f"{self.player.name}'s Stats")
            self.player_name.grid(row=3, column=0, sticky="nsew", columnspan=3)
        else:
            self.player_name.config(text=f"{self.player.name}'s Stats\n "
                                         f"Buff duration: {self.player.buff_duration} turn(s)")

        self.player_health = tk.Label(self, text=f"HP {self.player.health}/{self.player.max_hp}", font=(self.font, 16))
        self.player_health.grid(row=4, column=0, sticky="nsew")

        self.actions.config(text=f"Actions")
        self.actions.grid(row=5, column=1, pady=(10, 5))

        self.basic_attack = ttk.Button(self, style="success.Outline.TButton", text=f"Attack {self.enemy.name}",
                                       command=lambda: self.combat_basic_attack())
        self.basic_attack.grid(row=6, column=0, sticky="nsew", padx=5)
        self.default_menu.append(self.basic_attack)

        self.block = ttk.Button(self, style="success.Outline.TButton", text=f"Block {self.enemy.name}",
                                command=lambda: self.combat_block())
        self.block.grid(row=6, column=1, sticky="nsew", padx=5)
        self.default_menu.append(self.block)

        self.flee = ttk.Button(self, style="success.Outline.TButton", text=f"Flee",
                               command=lambda: self.parent.switch_frame(Menu))
        self.flee.grid(row=6, column=2, sticky="nsew", padx=5)
        self.default_menu.append(self.flee)

        self.spells = ttk.Button(self, style="info.Outline.TButton", text=f"Open spell book",
                                 command=lambda: self.open_spells_menu())
        self.spells.grid(row=7, column=1, sticky="nsew", padx=5, pady=50)

    def open_spells_menu(self):
        for widget in self.default_menu:
            widget.destroy()

        self.actions.config(text="Spellbook")
        self.spells.config(text="Go back", command=lambda: self.create_widgets())
        row_num = 0
        col_num = 0

        for spell in self.player.spells:
            if col_num == 0:
                row_num = 0
            elif col_num % 3 == 0:
                row_num += 3
                col_num = 0

            self.spell = ttk.Button(self, style="primary.TButton", text=f"{spell.name}\n"
                                                                        f"{spell.description}",
                                    command=lambda use_spell=spell: self.use_spell(use_spell))

            if self.player.buff_duration > 0:
                if isinstance(spell, Buff):
                    self.spell.config(state="disabled")

            if self.player.max_hp == self.player.health:
                if isinstance(spell, Heal):
                    self.spell.config(state="disabled")

            if spell.cooldown > 0:
                self.spell.config(state="disabled", text=f"{spell.name}\n"
                                                         f"{spell.cooldown} cooldown\n"
                                                         f"{spell.description}")

            self.spell.grid(row=6, ipadx=10, ipady=2, padx=4, column=col_num, sticky="nsew",
                            columnspan=1)

            self.spells_button.append(self.spell)
            col_num += 1

    def use_spell(self, spell):
        if self.player.use_spell(spell):
            self.update_info(f"You used {spell.name}.\n\n")
            spell.cooldown = spell.max_cd
            if not self.is_dead(self.enemy):
                if isinstance(spell, Buff):
                    if spell.attack > 0:
                        self.player_attack.config(text=f"{self.player.attack}(+{spell.attack}) ATK",
                                                  style="danger.TLabel")
                    if spell.defence > 0:
                        self.player_defence.config(text=f"{self.player.defence}(+{spell.defence}) DEF",
                                                   style="info.TLabel")
                self.update_widgets()
                self.enemy_action()
                self.create_widgets()
        else:
            if isinstance(spell, Buff):
                self.update_info(f"Already using a buff!\n")

    def end_combat(self):
        """end combat and get xp"""
        if not self.player.get_xp(self.enemy.xp):
            self.parent.update_info_widget(
                f"Successfully defeated {self.enemy.name}!\nYou have gained {self.enemy.xp} XP!")
        else:
            if self.player.level % 5 != 0:
                self.parent.update_info_widget(f"Successfully defeated {self.enemy.name}!\n"
                                               f"You have gained {self.enemy.xp} XP!\n\n"
                                               f"You have leveled up!!!\n"
                                               f"You are now Level {self.player.level}!\n"
                                               f"Attack and Defence have increased!\n")
            else:
                self.parent.update_info_widget(f"Successfully defeated {self.enemy.name}!\n"
                                               f"You have gained {self.enemy.xp} XP!\n\n"
                                               f"You have leveled up!!!\n"
                                               f"You are now Level {self.player.level}!\n"
                                               f"All stats increased!\n")

        if self.enemy.inv:
            self.player.combat_take_item(self.enemy.inv)
            self.parent.update_info_widget(f"You got {self.enemy.inv.name} from {self.enemy.name}!")
        else:
            print("none taken")

        self.current_location.enemy.remove(self.enemy)
        self.parent.switch_frame(Menu)

    @staticmethod
    def is_dead(target):
        """check if the target (enemy or player) is dead"""
        if target.is_alive():
            return False
        else:
            return True

    def update_info(self, content):
        """update current status of combat"""
        self.info.config(state="normal")
        self.info.insert(tk.END, content)
        self.info.config(state="disabled")
        self.info.see("end")

    def add_turn(self):
        """reduces all cooldown add a turn"""
        for player_spell in self.player.spells:
            if player_spell.cooldown > 0:
                player_spell.cooldown -= 1
        if self.player.buff_duration > 0:
            self.player.buff_duration -= 1
        if self.player.buff_duration == 0:
            self.player.revert_spell()

        for enemy_spell in self.enemy.spells:
            if enemy_spell.cooldown > 0:
                enemy_spell.cooldown -= 1
        if self.enemy.buff_duration > 0:
            self.enemy.buff_duration -= 1
        if self.enemy.buff_duration == 0:
            self.enemy.revert_spell()
        self.turn += 1

    def enemy_spell(self):
        """enemy spell logic"""
        for spell in self.enemy.spells:
            if spell.cooldown <= 0:
                self.enemy.use_spell(spell)
                spell.cooldown = spell.max_cd

                if not isinstance(spell, Buff):
                    pass
                else:
                    if spell.attack > 0:
                        self.enemy_attack.config(text=f"{self.enemy.attack}(+{spell.attack}) ATK",
                                                 style="danger.TLabel")
                    if spell.defence > 0:
                        self.enemy_defence.config(text=f"{self.enemy.defence}(+{spell.defence}) DEF",
                                                  style="info.TLabel")

                self.update_info(f"{self.enemy.name} used {spell.name}!\n")

    def enemy_action(self):
        """enemy turn"""
        self.enemy_spell()
        damage = self.player.take_damage(self.enemy.attack)
        self.update_info(f"{self.enemy.name} attacked you for {damage} damage.\n\n")
        if not self.is_dead(self.player):
            self.add_turn()
            self.update_widgets()
        else:
            self.parent.switch_frame(GameOver)

    def combat_basic_attack(self):
        """perform basic attack"""
        damage = self.enemy.take_damage(self.player.attack)
        self.update_info(f"You attacked {self.enemy.name} for {damage} damage.\n\n")
        if not self.is_dead(self.enemy):
            self.enemy_action()
            self.update_widgets()

    def combat_block(self):
        """perform block - halves damage"""
        self.player.action_block()
        self.update_info(f"You are now blocking!\n\n")
        if not self.is_dead(self.enemy):
            self.player.action_block()
            self.update_widgets()
            self.enemy_action()

    def buff_active(self):
        if self.player.buff_duration > 0:
            for b in self.spells_button:
                b.destroy()

            row_num = 0
            col_num = 0

            for spell in self.player.spells:
                if col_num == 0:
                    row_num = 0
                elif col_num % 3 == 0:
                    row_num += 3
                    col_num = 0

                if isinstance(spell, Buff):
                    self.spell = ttk.Button(self, style="primary.TButton", text=f"{spell.name}\n{spell.description}",
                                            command=lambda use_spell=spell: self.use_spell(use_spell), state="disabled")
                    self.spell.grid(row=6, ipadx=10, ipady=2, padx=4, column=col_num, sticky="nsew",
                                    columnspan=1)
                    self.spells_button.append(self.spell)
                col_num += 1
            return True
        else:
            return False

    def update_widgets(self):
        """update widgets"""
        if self.player.buff_duration > 0:
            self.player_name.config(text=f"{self.player.name}'s Stats\n "
                                         f"Buff duration: {self.player.buff_duration} turn(s)")
        else:
            self.player_name.config(text=f"{self.player.name}'s Stats")
            self.player_attack.config(text=f"{self.player.attack} ATK", style="TLabel")
            self.player_defence.config(text=f"{self.player.defence} DEF", style="TLabel")

        if self.enemy.buff_duration > 0:
            self.fight.config(text=f"{self.enemy.name}'s Stats\n "
                                   f"Buff duration: {self.enemy.buff_duration} turn(s)")
        else:
            self.fight.config(text=f"LV.{self.enemy.level} {self.enemy.name}\n")
            self.enemy_attack.config(text=f"{self.enemy.attack} ATK", style="TLabel")
            self.enemy_defence.config(text=f"{self.enemy.defence} DEF", style="TLabel")

        self.player_health.config(text=f"HP {self.player.health}/{self.player.max_hp}")
        self.enemy_health.config(text=f"HP {self.enemy.health}/{self.enemy.max_hp}")


class MainMenu(ttk.Frame):
    """tk frame for the main menu """

    def __init__(self, parent):
        super().__init__(parent)
        self.font = "VCR OSD MONO"

        self.columnconfigure(list(range(3)), weight=1, uniform="Silent_Creme")
        self.rowconfigure(list(range(5)), weight=1)
        self.rowconfigure(6, weight=3)

        self.title = ttk.Label(text="Hello World!", font=(self.font, 40), style="danger.TLabel")
        self.title.grid(row=0, column=0)

        self.by = ttk.Label(text="by me", font=(self.font, 26), style="info.TLabel")
        self.by.grid(row=1, column=0)

        self.new_game = ttk.Button(text="new game", style="info.outline.TButton")
        self.new_game.grid(row=3, column=0, pady=10)

        self.load_game = ttk.Button(text="load game", style="info.outline.TButton")
        self.load_game.grid(row=4, column=0, pady=10)

        self.by = ttk.Label(text="Last Updated: April 2024", font=(self.font, 12), style="secondary.TLabel")
        self.by.grid(row=5, column=0, pady=(100, 5))



    pass


class Dialogue(ttk.Frame):
    """ Tkitner frame for npc dialogue """

    def __init__(self, parent):
        super().__init__(parent)
        self.player = parent.player
        self.locations = parent.locations
        self.current_location = self.player.current_location(self.locations)
        self.npc = self.current_location.npc
        self.parent = parent
        self.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(list(range(3)), weight=1, uniform="Silent_Creme")
        self.rowconfigure(list(range(5)), weight=1)
        self.rowconfigure(6, weight=3)
        self.info = tk.Text(self, height=10, relief="ridge", font="Helvetica", state="disabled")
        self.info.grid(row=2, column=0, pady=(10, 20), columnspan=3)
        self.update_info(f"You have engaged in conversation...\n")
        self.current_buttons = []
        self.current_node = self.npc.dialogue_tree
        self.create_dialogue_options()

    def create_dialogue_options(self):
        """create the dialogue options"""
        if self.current_buttons:
            for b in self.current_buttons:
                b.destroy()
        dialogue_options = self.current_node.keys()

        for i, option in enumerate(dialogue_options, 0):
            button = ttk.Button(self, text=option, style="primary.TButton",
                                command=lambda index=i: self.talk(dialogue_options, index))
            button.grid(row=3+i, ipadx=10, ipady=2, padx=4, pady=10, column=0, sticky="nsew", columnspan=3)
            self.current_buttons.append(button)

    def talk(self, option, index):
        """talk to the npc based on the option and index"""
        selected_option = list(option)[index]
        self.update_info(f"{self.player.name}: {selected_option}\n")
        self.current_node = self.current_node[selected_option]
        if isinstance(self.current_node, str):
            self.update_info(f"{self.npc.name}: {self.current_node}\n")
            self.current_node = self.npc.dialogue_tree
        self.create_dialogue_options()

    def update_info(self, content):
        """update current status of combat"""
        self.info.config(state="normal")
        self.info.insert(tk.END, content)
        self.info.config(state="disabled")
        self.info.see("end")

    def create_widgets(self):
        pass


class Menu(ttk.Frame):
    """menu for player interaction"""

    def __init__(self, parent):
        super().__init__(parent)
        self.locations = parent.locations
        self.player = parent.player
        self.current_location = self.player.current_location(self.locations)

        self.parent = parent

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
        self.take_button = None
        self.take_dropdown = None
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
            self.talk_button = ttk.Button(self, style="success.Outline.TButton", text=f"Talk",
                                          command=lambda: self.parent.switch_frame(Dialogue))
            self.talk_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=0, pady=50, sticky="nsew", columnspan=1)
            self.buttons.append(self.talk_button)

        if self.current_location.check_item() == 1:
            self.take_button = ttk.Button(self, text=f"Take {self.current_location.item[0].name}",
                                          style="success.Outline.TButton",
                                          command=lambda: self.take_item(self.current_location.item[0]))
            self.take_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=1, pady=50, sticky="nsew", columnspan=1)
            self.can_take()
            self.buttons.append(self.take_button)

        elif self.current_location.check_item() > 1:
            self.take_dropdown = ttk.Menubutton(self, text="Take Items", style="success.Outline.TButton")
            self.menu = tk.Menu(self.take_dropdown, tearoff=0)
            for item in self.current_location.item:
                self.menu.add_radiobutton(label=f"{item.name} - {item.desc}",
                                          command=lambda take_item=item: self.take_item(take_item))
            self.take_dropdown.grid(row=5, ipadx=10, ipady=2, padx=4, column=1, pady=50, sticky="nsew",
                                    columnspan=1)
            self.take_dropdown['menu'] = self.menu
            self.buttons.append(self.take_dropdown)
            self.buttons.append(self.menu)
            self.can_take()

        if self.current_location.check_enemy():
            self.fight_button = ttk.Button(self, style="success.Outline.TButton", text=f"Fight",
                                           command=lambda: self.parent.switch_frame(CombatScreen))
            self.fight_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=2, pady=50, sticky="nsew", columnspan=1)
            self.buttons.append(self.fight_button)

    def can_take(self):
        if self.player.check_max_inv():
            if self.take_button:
                self.take_button.config(state="disabled", text="Max inventory!")
            else:
                self.take_dropdown.config(state="disabled", text="Max inventory!")

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

    def take_item(self, item):
        item_name = self.player.take_item(item, self.current_location)
        add_item_prompt = f"Added {item_name} to inventory!\n\n"
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
            self.talk_button = ttk.Button(self, style="success.Outline.TButton", text=f"Talk",
                                          command=lambda: self.parent.switch_frame(Dialogue))
            self.talk_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=0, pady=50, sticky="nsew", columnspan=1)
            self.buttons.append(self.talk_button)

        if self.current_location.check_item() == 1:
            self.take_button = ttk.Button(self, text=f"Take {self.current_location.item[0].name}",
                                          style="success.Outline.TButton",
                                          command=lambda: self.take_item(self.current_location.item[0]))
            self.take_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=1, pady=50, sticky="nsew", columnspan=1)
            self.can_take()
            self.buttons.append(self.take_button)
        elif self.current_location.check_item() > 1:
            self.take_dropdown = ttk.Menubutton(self, text="Take Items", style="success.Outline.TButton")
            self.menu = tk.Menu(self.take_dropdown, tearoff=0)
            for item in self.current_location.item:
                self.menu.add_radiobutton(label=f"{item.name} - {item.desc}",
                                          command=lambda take_item=item: self.take_item(take_item))
            self.take_dropdown.grid(row=5, ipadx=10, ipady=2, padx=4, column=1, pady=50, sticky="nsew",
                                    columnspan=1)
            self.take_dropdown['menu'] = self.menu
            self.buttons.append(self.take_dropdown)
            self.buttons.append(self.menu)
            self.can_take()
        if self.current_location.check_enemy():
            self.fight_button = ttk.Button(self, style="success.Outline.TButton", text=f"Fight",
                                           command=lambda: self.parent.switch_frame(CombatScreen))
            self.fight_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=2, pady=50, sticky="nsew", columnspan=1)
            self.buttons.append(self.fight_button)


class StatusBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.player = parent.player
        self.parent = parent
        self.previous_frame = parent.previous_frame[-1]
        print("Current Frame:", parent.frame_name)

        frame_inv = ["Menu", "CombatScreen"]

        if parent.frame_name != "GameOver" and parent.frame_name != "MainMenu":
            if parent.frame_name in frame_inv:
                self.inv = ttk.Button(parent, text=f"Open {self.player.name}'s Inventory",
                                      command=lambda: self.switch_frame(Inventory))
                parent.previous_frame.append(getattr(sys.modules[__name__], parent.frame_name))
                self.inv.grid(row=6, column=0, sticky="nsew")

            if parent.frame_name not in frame_inv:
                self.inv = ttk.Button(parent, text=f"Back to game", style="danger.Outline.TButton",
                                      command=lambda: self.switch_frame(self.previous_frame))
                self.inv.grid(row=6, column=0, sticky="nsew")

        self.grid(row=6, column=0, sticky="nsew")

    def switch_frame(self, frame):
        """switch the frame"""
        self.parent.switch_frame(frame)
        self.inv.destroy()


# noinspection PyTypeChecker
ITEMS = chain(Consumable.generate_from_file("items.txt"), Weapon.generate_from_file("items.txt"))
ALL_ITEMS = [item for item in ITEMS]
ENEMIES = Enemy.generate_from_file("enemy.txt")
# noinspection PyTypeChecker
SPELLS = chain(Buff.generate_from_file("spells.txt"), Heal.generate_from_file("spells.txt"))
ALL_SPELLS = [spell for spell in SPELLS]
ALL_ENEMIES = [enemy for enemy in ENEMIES]

NPCS = NPC.generate_from_file("npc.json")
ALL_NPCS = [npc for npc in NPCS]


def main():
    """ Main game loop """
    # test player
    player = Player('test', 1, 0, 20, 10,
                    3, "A", 0, [], None, None, [1, 2, 8])
    player.link_spells()

    locations = [Location(**loc) for loc in LOC_LIST]
    for location in locations:
        location.link_item()
        location.link_enemies()
        location.link_npc()

    open('infosave.txt', 'w').close()

    app = App(player, locations)
    app.mainloop()


if __name__ == '__main__':
    main()
