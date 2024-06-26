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


class Character:
    """Character class that represents the player and enemy stats
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

    def get_coins(self, coins):
        """add coins"""
        self._coins += coins

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
            xp_required = 30 + (self._level * 10)  # increase threshold depending on current level
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
        """uses the spell and updates character stats depending on the spell type"""
        if isinstance(spell, Buff):
            if self._buff_duration == 0:
                # set buff durations and buff amount
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
        # if heal add heal amount to current health
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
        """revert spell effects"""
        self._attack -= self.attk_buff
        self._defence -= self.def_buff
        self.attk_buff = 0
        self.def_buff = 0


class Player(Character):
    """Player class that represents the player character"""

    def __init__(self, name, level, xp, health, attack, defence, location, coins, inv, weapon, armour, spells, floor,
                 max_hp=20):
        super().__init__(name, level, xp, health, attack, defence, coins, inv, max_hp, spells)

        self._weapon = weapon
        self._armour = armour
        self._location = location
        self.max_inv_size = 9
        self._floor = floor

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
        self._coins = new_coins

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

    @property
    def floor(self):
        return self._floor

    @floor.setter
    def floor(self, new_floor):
        self._floor = new_floor

    def current_location(self):
        """take the current location and return it as an object from the locations list."""
        for loc in LOCATIONS:
            if loc.id == self._location:
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
        self._defence += item.defence
        self.heal(item.health)
        self._inv.remove(item)

    def unequip_item(self, item):
        """unequip item from inventory"""
        if isinstance(item, Weapon) and self._weapon:
            self._attack -= item.attack
            self._weapon = None
            print(f"Successfully unequipped {item.name}!")
            return True
        elif isinstance(item, Armour):
            self._defence -= item.defence
            self._armour = None
            print(f"Successfully unequipped {item.name}!")
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
        elif isinstance(item, Armour):
            self._defence += item.defence
            self._armour = item
        else:
            print(f"Item {item.name} cannot be equipped!")
            return False


class Enemy(Character):
    """Enemy class that represents the enemy character"""

    def __init__(self, enemy_id, name, level, xp, health, attack, defence, coins, inv, max_hp, spells, boss):
        super().__init__(name, level, xp, health, attack, defence, coins, inv, max_hp, spells)
        self._id = int(enemy_id)
        self._boss = boss

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

    @property
    def boss(self):
        return self._boss

    @boss.setter
    def boss(self, new_boss):
        self._boss = new_boss

    @classmethod
    def generate_from_file(cls, in_file):
        """ generate enemies from enemy.csv file """
        with open(in_file, 'r') as enemies:
            for enemy in enemies:
                data = enemy.strip().split(',')

                enemy_id = data[0].strip()
                enemy_name = data[1].strip()
                enemy_level = data[2].strip()

                # randomises enemy stats depending on the range supplied by the enemy.txt file
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

                # puts all the items into enemy inventory
                enemy_inv = [item.strip() for item in data[8].strip().split(';')]

                # uses the item_id to link with item object then append to enemy inventory
                new_item_list = []
                for i in range(len(ALL_ITEMS)):
                    for item_id in enemy_inv:
                        if int(item_id) == ALL_ITEMS[i].id:
                            new_item_list.append(ALL_ITEMS[i])

                enemy_inv = new_item_list

                # gets the chance of getting an item from an enemy
                enemy_chance = data[9].strip()

                # uses the spell_id to link with spell object then append to the enemy spells
                enemy_spells = [item.strip() for item in data[10].strip().split(';')]
                new_spell_list = []
                for i in range(len(ALL_SPELLS)):
                    for spell_id in enemy_spells:
                        if int(spell_id) == ALL_SPELLS[i].id:
                            new_spell_list.append(ALL_SPELLS[i])

                enemy_spells = new_spell_list

                enemy_boss = data[11].strip()
                if int(enemy_boss) == 1:  # checks if enemy is boss
                    enemy_boss = True
                else:
                    enemy_boss = False

                # random number generator if player can get item from enemy inventory
                if random.randint(1, int(enemy_chance)) == 1:
                    enemy_inv = random.choice(enemy_inv)
                else:
                    enemy_inv = None

                # returns the Enemy object one at a time
                yield Enemy(enemy_id, enemy_name, enemy_level, enemy_xp, enemy_health, enemy_attack, enemy_defence,
                            enemy_coins, enemy_inv, enemy_health, enemy_spells, enemy_boss)


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
            for heal in islice(heals, 4, 7):
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
        elif isinstance(self, Armour):
            return "armour"
        elif isinstance(self, Consumable):
            return "consumable"
        elif isinstance(self, Key):
            return "key"


class Consumable(Item):
    """A class inheriting the item class to represent the consumable items in the game"""

    def __init__(self, item_id, name, desc, value, attack, defence, health):
        super().__init__(item_id, name, desc, value)
        self.attack = int(attack)
        self.defence = int(defence)
        self.health = int(health)

    @classmethod
    def generate_from_file(cls, in_file):
        """ generate items from items.txt file """
        with open(in_file, 'r') as consumables:
            for consumable in islice(consumables, 4, 5):
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
            for weapon in islice(weapons, 0, 4):
                yield Weapon(*weapon.strip().split(","))


class Armour(Item):
    """A class inheriting the item class to represent the armour in the game"""

    def __init__(self, item_id, name, desc, value, defence):
        super().__init__(item_id, name, desc, value)
        self.defence = int(defence)

    @classmethod
    def generate_from_file(cls, in_file):
        """ generate items from items.txt file """
        with open(in_file, 'r') as armours:
            for armour in islice(armours, 8, 10):
                yield Armour(*armour.strip().split(","))


class Key(Item):
    """A class inheriting the item class to represent the keys in the game"""

    def __init__(self, item_id, name, desc, value):
        super().__init__(item_id, name, desc, value)

    @classmethod
    def generate_from_file(cls, in_file):
        """ generate items from items.txt file """
        with open(in_file, 'r') as keys:
            for key in islice(keys, 5, 8):
                yield Key(*key.strip().split(","))


class Location:
    """A class representing the locations in the game
    """

    def __init__(self, location_id, name, desc, dest, npc, enemy, item, key):
        self._id = location_id
        self._name = name
        self._desc = desc
        self._dest = dest
        self._npc = npc
        self._enemy = enemy
        self._item = item
        self._key = key
        # link ids to their respective objects
        self.link_npc()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

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

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_key):
        self._key = new_key

    def link_npc(self):
        """link npc name to npc object"""
        for npc in ALL_NPCS:
            if npc.name == self._npc:
                self._npc = npc

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

    def link_dest(self):
        """Maps the destinations to their location objects"""
        new_dest_list = []
        for i in range(len(LOCATIONS)):
            for location_name in self._dest:
                if location_name == LOCATIONS[i].id:
                    new_dest_list.append(LOCATIONS[i])
        self._dest = new_dest_list

    @staticmethod
    def parse_location_data(line):
        """Split the line into individual values"""
        parts = line.strip().split(',')
        # Extract values for each argument
        location_id = parts[0].strip('"')
        name = parts[1].strip('"')
        desc = parts[2].strip('"')
        dest = parts[3].strip('[]').split('-')
        npc = parts[4].strip('"')
        enemy = parts[5].strip('[]')
        new_enemy_list = []
        # link enemy id to enemy
        for i in range(len(ALL_ENEMIES)):
            for enemy_id in enemy:
                if int(enemy_id) == ALL_ENEMIES[i].id:
                    new_enemy_list.append(ALL_ENEMIES[i])
        enemy = new_enemy_list
        item = parts[6].strip('[]').split('-')
        key = parts[7].strip('"')

        if "False" in item:
            item = None
        else:
            # link item id to item object
            new_item_list = []
            for i in range(len(ALL_ITEMS)):
                for item_id in item:
                    if int(item_id) == ALL_ITEMS[i].id:
                        new_item_list.append(ALL_ITEMS[i])
            item = new_item_list

        new_key = None
        if key == "False":
            new_key = None
        else:
            for i in range(len(ALL_ITEMS)):
                if int(key) == ALL_ITEMS[i].id:
                    new_key = ALL_ITEMS[i]

        # Return a dictionary with the extracted values
        return {
            "location_id": location_id,
            "name": name,
            "desc": desc,
            "dest": dest,
            "npc": npc,
            "enemy": enemy,
            "item": item,
            "key": new_key
        }

    @classmethod
    def generate_from_file(cls, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                # Parse each line to extract the values
                location_data = cls.parse_location_data(line)
                yield Location(**location_data)
                # Append the extracted data to LOC_LIST

    @staticmethod
    def dest_locked(dest):
        """checks if destination is locked"""
        for location in LOCATIONS:
            if location.id == dest:
                if location.key:
                    return location.key
        return False

    def print_location_info(self, dests):
        """Print the location information, including name, description, and possible destinations.

        Args:
            dests (list): A list of destinations.

        Returns:
            str: The formatted location information.
        """

        dest_list_names = [dest.name for dest in dests if not dest.key]
        locked_loc_names = [dest.name for dest in dests if dest.key]  # compile a list of dest that are locked

        dest = ", ".join(dest_list_names)

        prompt = f"\nYou moved to {self.name}.\n{self.desc}\nYou can move to {dest}.\n"
        # prints the locations that are locked
        if locked_loc_names:
            lock_dest = ", ".join(locked_loc_names)
            prompt = prompt + f"{lock_dest} is locked!\n"
        if self.check_npc():
            prompt = prompt + "Someone is waving at you!\n"
        if self.check_item():
            prompt = prompt + "There is an item here!\n"
        if self.check_enemy():
            prompt = prompt + "You sense an evil presence!\n"
        return prompt


class NPC:
    """NPC class that represents the non-player characters in the game
    """

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


class Shop(NPC):
    """Initializes an instance of the Shop class which inherits from npc"""

    def __init__(self, name, dialogue_tree, shop_stock):
        super().__init__(name, dialogue_tree)
        self.name = name
        self.dialogue_tree = dialogue_tree
        self.shop_stock = shop_stock

    @classmethod
    def generate_from_file(cls, filename):
        with open(filename, "r") as file:
            dialogue_tree = json.load(file)
            npc_dialogue = random.choice(["We have great items!", "Welcome!", "I hope you have money"])
            for npc_name, shop_stock in dialogue_tree.items():
                # link the item_ids to their respective item classes
                linked_shop_stock = dict()
                for str_item_id, item_price in shop_stock.items():
                    item_id = int(str_item_id)
                    for i in range(len(ALL_ITEMS)):
                        if item_id == ALL_ITEMS[i].id:
                            linked_shop_stock[ALL_ITEMS[i]] = item_price
                yield Shop(npc_name, npc_dialogue, linked_shop_stock)


class App(tk.Tk):
    """ App class that represents the main application window"""

    def __init__(self):
        super().__init__()
        self.player = None
        self.previous_frame = ["MainMenu"]

        self.style = tb.Style(theme="darkly")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.title("ReLIFE 1.0")
        # grid config
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
        self.frame_name = frame_class.__name__  # set the frame name to the frame class name to be used later
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
        """update the info widget in Menu"""
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

        # labels
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
        self.spells_list = [spell.name for spell in self.player.spells]
        self.spell = ", ".join(self.spells_list)
        self.item_widget = []
        self.cons_list = [item.name for item in self.player.inv if isinstance(item, Consumable)]
        self.create_widgets()
        self.create_item_widget()

    def create_widgets(self):
        """ create widgets for the inventory frame """
        self.name = ttk.Label(self, text=f"LV.{self.player.level} {self.player.name}", style="info.TLabel",
                              font="Helvetica 30 bold")
        self.name.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.stats = ttk.Label(self,
                               text=f"XP {self.player.xp}/{self.player.xp_required()}  | "
                                    f"HP {self.player.health}/{self.player.max_hp} | Attack: {self.player.attack} | "
                                    f"Defence: {self.player.defence} | {self.player.coins} coins.",
                               font="Helvetica 15")
        self.stats.grid(row=1, column=0, columnspan=3)

        # player equipped items section
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

        self.skills = ttk.Label(self, text=f"Spells: {self.spell}")
        self.skills.grid(row=5, column=0, columnspan=3)

        # separates player stats and player inventory
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

            # generates a different type of widget depending on item type
            if item.get_item_type() == "weapon":
                self.create_weapon_item_widget(item, row_num, col_num)
                col_num += 1

            elif item.get_item_type() == "armour":
                self.create_armour_item_widget(item, row_num, col_num)
                col_num += 1

            elif item.get_item_type() == "key":
                self.create_item_info_widget(item, row_num, col_num)
                col_num += 1

            elif item.get_item_type() == "consumable":
                uses = self.cons_list.count(item.name)  # count how many of the same consumable item
                if item.name not in duplicate_consumables_widgets:  # check if the widget has been created
                    if uses > 1:  # if more than one of the same item, display uses
                        self.create_consumable_item_widget(item, row_num, col_num, False, uses)
                        duplicate_consumables_widgets.append(item.name)
                        col_num += 1
                    else:  # if only one of the item, don't display uses
                        self.create_consumable_item_widget(item, row_num, col_num, True, uses)
                        col_num += 1

        if not self.player.inv:
            # if player has no items, display message
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
        """create widgets for weapon items"""
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

    def create_armour_item_widget(self, item, row_num, col_num):
        """create widgets for armour items"""
        self.create_item_info_widget(item, row_num, col_num)
        if self.player.armour == item:
            self.unequip_button = ttk.Button(self, text="Unequip", style="danger.Outline.TButton", width=10,
                                             command=lambda items=item: self.unequip_item(items))
            self.unequip_button.grid(row=16 + row_num, column=col_num, pady=(0, 50))
            self.item_widget.append(self.unequip_button)
        elif not self.player.armour:
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
        self.stats.config(text=f"XP {self.player.xp}/{self.player.xp_required()}  | "
                               f"HP {self.player.health}/{self.player.max_hp} | Attack: {self.player.attack} | "
                               f"Defence: {self.player.defence} | {self.player.coins} coins.")
        self.skills.config(text=f"Spells: {self.spell}")
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
    """generate frame for game over screen/respawn screen"""

    def __init__(self, parent):
        super().__init__(parent)
        self.font = "VCR OSD MONO"
        self.parent = parent
        self.current_widgets = []

        self.game_over = ttk.Label(text="You died!", font=(self.font, 40), style="danger.TLabel")
        self.game_over.grid(row=0, column=0)
        self.current_widgets.append(self.game_over)

        self.new_game = ttk.Button(self, text="Respawn to Floor One: City", style="info.outline.TButton",
                                   command=lambda: self.respawn())
        self.new_game.grid(row=1, column=0, pady=(30, 50))
        self.current_widgets.append(self.new_game)

    def respawn(self):
        """respawn player"""
        for w in self.current_widgets:
            w.destroy()
        self.parent.player.location = "G"
        self.parent.switch_frame(Menu)


class CombatScreen(ttk.Frame):
    """tk frame for the combat """

    def __init__(self, parent):
        super().__init__(parent)
        self.player = parent.player
        self.current_location = self.player.current_location()
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

        # widgets 
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
        self.info = tk.Text(self, height=10, relief="ridge", font=("Helvetica", 16), state="disabled")
        self.info.grid(row=2, column=0, pady=(10, 20), columnspan=3, sticky="nsew")

        self.create_widgets()

    def create_widgets(self):
        """creates the widgets for the combat screen"""

        # destroy the current widgets
        for b in self.spells_button:
            b.destroy()

        if self.enemy.buff_duration > 0:
            self.fight.config(text=f"LV.{self.enemy.level} {self.enemy.name}\n"
                                   f"Buff duration: {self.enemy.buff_duration} turn(s)")
        else:
            self.fight.config(text=f"LV.{self.enemy.level} {self.enemy.name}\n")
        self.fight.grid(row=0, column=0, sticky="nsew", columnspan=3, pady=(0, 10))

        # display enemy stats
        self.enemy_health = tk.Label(self, text=f"HP {self.enemy.health}/{self.enemy.max_hp}", font=(self.font, 16))
        self.enemy_health.grid(row=1, column=0, sticky="nsew")

        self.enemy_attack.grid(row=1, column=1)

        self.enemy_defence.grid(row=1, column=2)

        # if player has a buff active, display the buff duration
        if not self.buff_active():
            self.player_name.config(text=f"{self.player.name}'s Stats")
            self.player_name.grid(row=3, column=0, sticky="nsew", columnspan=3)
        else:
            self.player_name.config(text=f"{self.player.name}'s Stats\n "
                                         f"Buff duration: {self.player.buff_duration} turn(s)")

        # display player stats
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

        # if enemy is not a boss, display flee button
        if not self.enemy.boss:
            self.flee = ttk.Button(self, style="success.Outline.TButton", text=f"Flee",
                                   command=lambda: self.parent.switch_frame(Menu))
            self.flee.grid(row=6, column=2, sticky="nsew", padx=5)
            self.default_menu.append(self.flee)

        self.spells = ttk.Button(self, style="info.Outline.TButton", text=f"Open spell book",
                                 command=lambda: self.open_spells_menu())
        self.spells.grid(row=7, column=1, sticky="nsew", padx=5, pady=50)

    def open_spells_menu(self):
        """open spells menu which displays all the spells the player can use"""
        for widget in self.default_menu:
            widget.destroy()  # destroys all widgets that's in the current menu

        self.actions.config(text="Spellbook")
        self.spells.config(text="Go back", command=lambda: self.create_widgets())
        row_num = 0
        col_num = 0

        for spell in self.player.spells:
            # configure grid
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

            # if player already at max hp disabled button
            if self.player.max_hp == self.player.health:
                if isinstance(spell, Heal):
                    self.spell.config(state="disabled")

            if spell.cooldown > 0:  # spell on cooldown disable button
                self.spell.config(state="disabled", text=f"{spell.name}\n"
                                                         f"{spell.cooldown} cooldown\n"
                                                         f"{spell.description}")

            self.spell.grid(row=6, ipadx=10, ipady=2, padx=4, column=col_num, sticky="nsew",
                            columnspan=1)

            self.spells_button.append(self.spell)
            col_num += 1

    def use_spell(self, spell):
        """use spell which checks wht type of spell was cast and update combat info based on that"""
        if self.player.use_spell(spell):
            self.update_info(f"You used {spell.name}.\n")
            spell.cooldown = spell.max_cd
            if isinstance(spell, Buff):
                if spell.attack > 0:
                    self.player_attack.config(text=f"{self.player.attack}(+{spell.attack}) ATK",
                                              style="danger.TLabel")
                    self.update_info(f"Increased ATK by {spell.attack} for {spell.duration} turns!\n\n")

                if spell.defence > 0:
                    self.player_defence.config(text=f"{self.player.defence}(+{spell.defence}) DEF",
                                               style="info.TLabel")
                    self.update_info(f"Increased DEF by {spell.attack} for {spell.duration} turns!\n\n")
            if isinstance(spell, Heal):
                self.update_info(f"Healed for {spell.health} HP!\n\n")

            self.create_widgets()
        # if player tries to use a buff while a buff is active
        else:
            if isinstance(spell, Buff):
                self.update_info(f"Already using a buff!\n")

    def end_combat(self):
        """end combat and get xp"""
        self.player.get_coins(self.enemy.coins)
        self.enemy.health = self.enemy.max_hp
        if not self.player.get_xp(self.enemy.xp):
            self.parent.update_info_widget(
                f"Successfully defeated {self.enemy.name}!\nYou have gained {self.enemy.xp} XP!\n"
                f"You got {self.enemy.coins} coins!\n")
        else:
            if self.player.level % 5 != 0:  # change print text depending on what level the player leveled up
                self.parent.update_info_widget(f"Successfully defeated {self.enemy.name}!\n"
                                               f"You got {self.enemy.coins} coins!\n"
                                               f"You have gained {self.enemy.xp} XP!\n\n"
                                               f"You have leveled up!!!\n"
                                               f"You are now Level {self.player.level}!\n"
                                               f"Attack and Defence have increased!\n")
            else:
                self.parent.update_info_widget(f"Successfully defeated {self.enemy.name}!\n"
                                               f"You got {self.enemy.coins} coins!\n"
                                               f"You have gained {self.enemy.xp} XP!\n\n"
                                               f"You have leveled up!!!\n"
                                               f"You are now Level {self.player.level}!\n"
                                               f"All stats increased!\n")
        # if enemy has an item, player gets the item
        if self.enemy.inv:
            self.player.combat_take_item(self.enemy.inv)
            self.parent.update_info_widget(f"You got {self.enemy.inv.name} from {self.enemy.name}!")

        self.current_location.enemy.remove(self.enemy)
        self.parent.switch_frame(Menu)

    def player_is_dead(self):
        """checks if player is dead"""
        if self.player.is_alive():
            self.add_turn()
            self.update_widgets()  # combat continues one more turn
        else:
            self.player.health = self.player.max_hp  # respawn player
            self.enemy.health = self.enemy.max_hp  # reset enemy
            self.parent.switch_frame(GameOver)  # game over screen once dead

    def enemy_is_dead(self):
        """check if the (enemy) is dead"""
        if self.enemy.is_alive():
            self.update_widgets()
            self.enemy_action()  # enemy attacks
        else:
            self.end_combat()  # if dead end combat

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
            if spell.cooldown <= 0:  # cast enemy spell when the cooldown is 0
                self.enemy.use_spell(spell)
                spell.cooldown = spell.max_cd

                # updates text
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
        # checks if player is dead
        self.player_is_dead()

    def combat_basic_attack(self):
        """perform basic attack"""
        damage = self.enemy.take_damage(self.player.attack)
        self.update_info(f"You attacked {self.enemy.name} for {damage} damage.\n\n")
        self.enemy_is_dead()

    def combat_block(self):
        """perform block - halves damage"""
        self.player.action_block()
        self.update_info(f"You are now blocking!\n\n")
        self.enemy_is_dead()
        self.player.action_block()  # disable block

    def buff_active(self):
        """if buff is active change the labels to show that"""

        # if buff is active
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
        self.main_menu_widgets = []
        self.parent = parent

        self.columnconfigure(list(range(3)), weight=1, uniform="Silent_Creme")
        self.rowconfigure(list(range(6)), weight=1)
        self.rowconfigure(6, weight=3)
        self.grid(row=1, column=0, sticky="nsew")

        self.title = ttk.Label(self, text="ReLife", font=(self.font, 40), style="danger.TLabel")
        self.title.grid(row=0, column=1)
        self.main_menu_widgets.append(self.title)

        self.by = ttk.Label(self, text="by Marcus", font=(self.font, 26), style="info.TLabel")
        self.by.grid(row=1, column=1)
        self.main_menu_widgets.append(self.by)

        self.new_game = ttk.Button(self, text="New Game", style="info.outline.TButton",
                                   command=lambda: self.create_new_game())
        self.new_game.grid(row=3, column=1, pady=(30, 50))
        self.main_menu_widgets.append(self.new_game)

        self.last_updated = ttk.Label(self, text="Last Updated: May 2024", font=(self.font, 12),
                                      style="secondary.TLabel")
        self.last_updated.grid(row=5, column=1, pady=(200, 5))
        self.main_menu_widgets.append(self.last_updated)

    def create_new_game(self):
        """destroy current widgets and create new game"""
        for w in self.main_menu_widgets:
            w.destroy()
            self.parent.switch_frame(NewGame)


class NewGame(ttk.Frame):
    """create new game"""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.font = "VCR OSD MONO"
        self.player_name = None
        self.columnconfigure(list(range(3)), weight=1, uniform="Silent_Creme")
        self.rowconfigure(list(range(3)), weight=1)
        self.current_question = []
        self.player_class = None
        self.line_index = 0
        self.current_line = None
        self.story_line = None
        self.story = None
        self.okay = None
        self.current_okay_button_text = 0

        self.new_game = ttk.Label(self, text="What is your name?", font=(self.font, 40), style="danger.TLabel")
        self.new_game.grid(row=0, column=0, pady=(0, 50), columnspan=3)
        self.current_question.append(self.new_game)

        self.name = ttk.Entry(self, style="danger.TEntry", width=30)
        self.name.grid(row=1, column=1)
        self.current_question.append(self.name)

        self.submit = ttk.Button(self, style="danger.Outline.TButton", text="Confirm",
                                 command=lambda: self.name_confirm())
        self.submit.grid(row=2, column=1, pady=(10, 350))
        self.current_question.append(self.submit)

    def name_confirm(self):
        """checks the name if valid and goes to the next question"""
        self.player_name = self.name.get()
        if not self.player_name:
            self.new_game.config(text="Hey, put your actual name!")
        elif len(self.player_name) > 15:
            self.new_game.config(text="Name too long!")
        elif len(self.player_name) == 1:
            self.new_game.config(text="Name too short!")
        else:
            for w in self.current_question:
                w.destroy()
            self.current_question.clear()
            self.mage_or_warrior()

    def mage_or_warrior(self):
        """changes the stats"""
        self.new_game = ttk.Label(self, text=f"{self.player_name}, are you a mage or a warrior?", font=(self.font, 40),
                                  style="danger.TLabel")
        self.new_game.grid(row=0, column=1, pady=0, columnspan=3)
        self.current_question.append(self.new_game)

        mage = ttk.Button(self, style="info.outline.TButton", text="I am a Mage",
                          command=lambda: self.mage())
        mage.grid(row=1, column=1, pady=(10, 10), columnspan=3)
        self.current_question.append(mage)

        warrior = ttk.Button(self, style="danger.outline.TButton", text="I am a Warrior",
                             command=lambda: self.warrior())
        warrior.grid(row=2, column=1, pady=(10, 350), columnspan=3)
        self.current_question.append(warrior)

    def mage(self):
        """set mage to player"""

        self.player_class = "Mage"
        spells = [1, 2, 8]
        attack = 6
        defence = 5

        player = Player(self.player_name, 1, 0, 20, attack, defence, "A", 0, [],
                        None, None, spells, 1, 20)
        player.link_spells()
        self.parent.player = player
        self.your_player()

    def warrior(self):
        """set warrior to player"""

        self.player_class = "Warrior"
        spells = [8]
        max_health = 30
        attack = 10
        defence = 5

        player = Player(self.player_name, 1, 0, max_health, attack, defence, "A", 0, [],
                        None, None, spells, 1, max_health)
        player.link_spells()
        self.parent.player = player
        self.your_player()

    def your_player(self):
        """show player stats"""
        for w in self.current_question:
            w.destroy()
        self.new_game = ttk.Label(self, text=f"Welcome {self.player_name}!", font=(self.font, 40),
                                  style="danger.TLabel")
        self.new_game.grid(row=0, column=1, pady=0, columnspan=3)
        self.current_question.append(self.new_game)

        show_player_class = ttk.Label(self, text=f"{self.player_class}", font=(self.font, 24),
                                      style="info.TLabel")
        show_player_class.grid(row=1, column=1, pady=0, columnspan=3)
        self.current_question.append(show_player_class)

        stats = ttk.Label(self, text=f"Stats:", font=(self.font, 30),
                          style="success.TLabel")
        stats.grid(row=2, column=1, columnspan=3, pady=(30, 10))
        self.current_question.append(stats)

        health = ttk.Label(self, text=f"{self.parent.player.health} HP", font=(self.font, 18),
                           style="info.TLabel")
        health.grid(row=3, column=1, columnspan=3, pady=(5, 0))
        self.current_question.append(health)

        attack = ttk.Label(self, text=f"{self.parent.player.attack} ATK", font=(self.font, 18),
                           style="info.TLabel")
        attack.grid(row=4, column=1, columnspan=3, pady=5)
        self.current_question.append(attack)

        defence = ttk.Label(self, text=f"{self.parent.player.defence} DEF", font=(self.font, 18),
                            style="info.TLabel")
        defence.grid(row=5, column=1, columnspan=3, pady=5)
        self.current_question.append(defence)

        spells_list = [spell.name for spell in self.parent.player.spells]
        spell = ", ".join(spells_list)

        spells = ttk.Label(self, text=f"Spells: {spell}", font=(self.font, 18),
                           style="info.TLabel")
        spells.grid(row=6, column=1, columnspan=3, pady=5)
        self.current_question.append(spells)

        start_game = ttk.Button(self, style="success.outline.TButton", text="Good to go!",
                                command=lambda: self.start_story(), width=20)
        start_game.grid(row=7, column=1, pady=(10, 350), columnspan=3)
        self.current_question.append(start_game)

    def start_story(self):
        """start story """
        for w in self.current_question:
            w.destroy()
        self.story_line = ["You work a 9 to a 5 job at Noodle Union.",
                           "It was your typical night, you were going home...",
                           "You tried to cross the street.",
                           "One step, and-",
                           "- It was all over...",
                           "...",
                           "...",
                           ".....",
                           "Hey! Wake up!",
                           "You seem disorientated. Here take this...",
                           "The figure hands you a pot with blue liquid.",
                           "You gulp down the potion."
                           "..."
                           "....",
                           "....."
                           "You immediately feel better.",
                           "Okay. Let me explain your current situation.",
                           "You were crossing the street and a truck hit you.",
                           "You died.",
                           "You're dead.",
                           "I felt so bad for you. So I brought you here.",
                           "I'll transport you to another world",
                           "You will have a more meaningful life there.",
                           "Climb the tower and see me at the end!",
                           "Suddenly, light flashes your eyes.",
                           "Floor One: The City"]

        # prints story and add okay button
        self.story = ttk.Label(self, text=self.story_line[0], font=(self.font, 34),
                               style="info.TLabel")
        self.story.grid(row=1, column=1, columnspan=3, pady=5)
        self.current_line = self.story

        self.okay = ttk.Button(self, text=f"Okay.", style="success.outline.TButton", command=lambda: self.next_line(),
                               width=25)
        self.okay.grid(row=2, column=1, columnspan=3, pady=10)
        self.current_question.append(self.okay)

        skip = ttk.Button(self, text=f"Skip Story", style="danger.outline.TButton", command=lambda: self.start_game(),
                          width=10)
        skip.grid(row=3, column=1, columnspan=3, pady=(20, 350))
        self.current_question.append(skip)

    def next_line(self):
        """prints next line of story"""
        okay_button = ["What!?", "...", "....", "What...", "Drink Mysterious Liquid", "What do you mean I died?",
                       "Huh!?", "What world?", "what???", "Tower???", "WAITTTTT!"]
        okay_button_line_changes = [4, 6, 7, 8, 10, 15, 17, 18, 19, 20, 21]
        self.current_line.destroy()
        self.line_index += 1
        self.story = ttk.Label(self, text=self.story_line[self.line_index], font=(self.font, 34),
                               style="info.TLabel")
        self.story.grid(row=1, column=1, columnspan=3, pady=5)

        if self.line_index == len(self.story_line) - 1:  # if story ends
            self.okay.config(text="Start game", command=lambda: self.start_game())
        elif self.line_index == okay_button_line_changes[self.current_okay_button_text]:
            self.okay.config(text=okay_button[self.current_okay_button_text])
            if self.current_okay_button_text != len(okay_button_line_changes) - 1:
                self.current_okay_button_text += 1
        else:
            self.okay.config(text="Okay.")
        self.current_line = self.story

    def start_game(self):
        for w in self.current_question:
            w.destroy()
        self.current_line.destroy()
        self.parent.switch_frame(Dialogue)


class Dialogue(ttk.Frame):
    """ Tkitner frame for npc dialogue """

    def __init__(self, parent):
        super().__init__(parent)
        self.player = parent.player
        self.current_location = self.player.current_location()
        self.npc = self.current_location.npc
        self.parent = parent
        self.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(list(range(3)), weight=1, uniform="Silent_Creme")
        self.rowconfigure(list(range(5)), weight=1)
        self.rowconfigure(6, weight=3)
        self.info = tk.Text(self, height=10, relief="ridge", font=("Helvetica", 16), state="disabled")
        self.info.grid(row=2, column=0, pady=(10, 20), columnspan=3, sticky="nsew")
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
            button.grid(row=3 + i, ipadx=10, ipady=2, padx=4, pady=10, column=0, sticky="nsew", columnspan=3)
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


class Store(ttk.Frame):
    """Class for store"""

    def __init__(self, parent):
        super().__init__(parent)
        self.player = parent.player
        self.current_location = self.player.current_location()
        self.npc = self.current_location.npc
        self.parent = parent
        self.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(list(range(3)), weight=1, uniform="Silent_Creme")
        self.rowconfigure(list(range(5)), weight=1)
        self.rowconfigure(6, weight=3)
        self.font = "VCR OSD MONO"

        # all widgets
        self.shop_name = ttk.Label(self, text=f"{self.npc.name}", font=(self.font, 28))
        self.shop_name.grid(row=0, column=0, pady=(10, 20), columnspan=3)

        self.player_coins = ttk.Label(self, text=f"{self.player.coins} COINS", font=(self.font, 18),
                                      style="warning.TLabel")
        self.player_coins.grid(row=1, column=0, pady=(10, 20), columnspan=3)

        self.info = tk.Text(self, height=1, relief="ridge", font=("Helvetica", 16), state="disabled")
        self.info.grid(row=2, column=0, columnspan=3, sticky="nsew")

        self.leave = ttk.Button(self, text=f"Leave", style="danger.outline.TButton", width=10,
                                command=lambda: self.parent.switch_frame(Menu))
        self.leave.grid(row=3, column=0, pady=(10, 20), columnspan=3)
        ttk.Separator(self, orient='horizontal').grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(5, 10))
        self.update_info(f"{self.npc.name}: {self.npc.dialogue_tree}")

        self.shop_widgets = []
        self.sell_widgets = []

        self.swap_screen = ttk.Button(self, text=f"Sell Your Stuff!", style="success.outline.TButton",
                                      command=lambda: self.sell())
        self.swap_screen.grid(row=20, column=0, columnspan=3, pady=(50, 100))
        self.create_shop()

    def create_shop(self):
        """create shop widgets"""
        for w in self.sell_widgets:
            w.destroy()

        self.swap_screen.config(text=f"Sell Your Stuff!", command=lambda: self.sell())

        row_num = 0
        col_num = 0

        for item, item_price in self.npc.shop_stock.items():
            if col_num == 0:
                row_num = 0
            elif col_num % 3 == 0:
                row_num += 5
                col_num = 0

            name = ttk.Label(self, text=f"{item.name}", style="success.TLabel", justify="left",
                             font="Helvetica 18")
            name.grid(row=5 + row_num, column=col_num)
            self.shop_widgets.append(name)

            desc = ttk.Label(self, text=f"{item.desc}", style="info.TLabel", justify="left",
                             font="Helvetica 12")
            desc.grid(row=6 + row_num, column=col_num)
            self.shop_widgets.append(desc)

            value = ttk.Button(self, text=f"Buy for: {item_price} coins", style="primary.TButton",
                               command=lambda stock_item=item, price=item_price: self.buy_item(stock_item, price))
            if self.player.coins < item_price or self.player.check_max_inv():
                value.config(state="disabled", text=f"Buy for: {item_price} coins")
            if self.player.check_max_inv():
                self.update_info(f"\nMax inventory! Sell or remove items!")
            value.grid(row=7 + row_num, column=col_num, pady=(0, 20))
            self.shop_widgets.append(value)

            col_num += 1

    def sell(self):
        """create items to sell"""
        for w in self.shop_widgets:
            w.destroy()

        for w in self.sell_widgets:
            w.destroy()

        self.swap_screen.config(text="Return to store", command=lambda: self.create_shop())

        row_num = 0
        col_num = 0
        # create sell widgets
        for item in self.player.inv:
            if col_num == 0:
                row_num = 0
            elif col_num % 3 == 0:
                row_num += 5
                col_num = 0

            sell_name = ttk.Label(self, text=item.name, style="success.TLabel", justify="left",
                                  font="Helvetica 18")
            sell_name.grid(row=5 + row_num, column=col_num)
            self.sell_widgets.append(sell_name)

            sell_desc = ttk.Label(self, text=f"{item.desc}", style="info.TLabel", justify="left",
                                  font="Helvetica 12")
            sell_desc.grid(row=6 + row_num, column=col_num)
            self.sell_widgets.append(sell_desc)

            sell_value = ttk.Button(self, text=f"Sell for: {item.value} coins", style="primary.TButton",
                                    command=lambda stock_item=item: self.sell_item(stock_item))

            if item.value <= 0:
                sell_value.config(state="disabled", text=f"No value!")

            sell_value.grid(row=7 + row_num, column=col_num)
            self.sell_widgets.append(sell_value)

    def buy_item(self, item, item_price):
        """buy item adds to player inv"""
        self.update_info(f"\nBought {item.name}!")
        self.player.combat_take_item(item)
        self.player.coins -= item_price
        self.player_coins.config(text=f"{self.player.coins} COINS")
        self.create_shop()

    def sell_item(self, item):
        """buy item adds to player inv"""
        self.update_info(f"\nSold {item.name}!")
        self.player.inv.remove(item)
        self.player.coins += item.value
        self.player_coins.config(text=f"{self.player.coins} COINS")
        self.sell()

    def update_info(self, content):
        """update information """
        self.info.config(state="normal")
        self.info.insert(tk.END, content)
        self.info.config(state="disabled")
        self.info.see("end")


class FloorCut(ttk.Frame):
    """when the player changes floor add extra frame"""

    def __init__(self, parent):
        super().__init__(parent)
        self.player = parent.player
        self.current_location = self.player.current_location()
        self.font = "VCR OSD MONO"
        self.parent = parent
        self.columnconfigure(list(range(3)), weight=1, uniform="Silent_Creme")
        self.rowconfigure(list(range(3)), weight=1)
        self.grid(row=1, column=0, sticky="nsew")

        if self.current_location.id == "BA":
            self.current_floor = ttk.Label(self, text=f"You've reached the\n top of the tower!", font=(self.font, 34),
                                           style="info.TLabel")
            self.current_floor.grid(row=0, column=1, sticky="ns")
            self.okay = ttk.Button(self, text=f"Quit!", style="success.outline.TButton",
                                   command=lambda: quit(),
                                   width=25)
            self.okay.grid(row=1, column=1, sticky="nsew", pady=(30, 350))
        else:
            self.current_floor = ttk.Label(self, text=f"Entering Floor {self.player.floor}", font=(self.font, 34),
                                           style="info.TLabel")
            self.current_floor.grid(row=0, column=1, sticky="ns")

            self.okay = ttk.Button(self, text=f"Confirm", style="success.outline.TButton",
                                   command=lambda: self.parent.switch_frame(Menu),
                                   width=25)
            self.okay.grid(row=1, column=1, sticky="nsew", pady=(30, 350))


class Menu(ttk.Frame):
    """the menu for player interaction"""

    def __init__(self, parent):
        super().__init__(parent)
        self.player = parent.player
        self.current_location = self.player.current_location()
        self.font = "VCR OSD MONO"
        self.parent = parent
        self.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(list(range(4)), weight=1, uniform="Silent_Creme")
        self.rowconfigure(list(range(5)), weight=1)
        self.rowconfigure(6, weight=3)

        self.label_location = tk.Label(self, text=f"Floor {self.player.floor}", font=(self.font, 15))
        self.label_location.grid(row=0, column=0, sticky="nsew", columnspan=4)

        self.info_location = tk.Label(self, text=f"You are in {self.current_location.name}", font=(self.font, 20))
        self.info_location.grid(row=1, column=0, sticky="nsew", columnspan=4)

        self.info = tk.Text(self, height=10, relief="ridge", font=("Helvetica", 16), state="disabled")
        self.info.grid(row=2, column=0, pady=(5, 20), columnspan=4, sticky="nsew")

        self.take_button = None
        self.move_header = ttk.Label(self, text="Where to?", font="Helvetica", style="info.TLabel")
        self.take_dropdown = None
        self.buttons = []
        self.move_header.grid(row=3, column=0, pady=(0, 5), columnspan=4)

        col_num = 0
        for i in range(len(self.current_location.dest)):
            if i == 0:
                col_num = 1
            else:
                col_num = 0
        # create buttons for destinations
        for dest in self.current_location.dest:
            self.move_button = ttk.Button(self, style="primary.Outline.TButton", text=f"Move to {dest.name}",
                                          command=lambda destination=dest: self.move(destination))

            if self.check_boss(dest):  # if dest has a boss warn player
                self.move_button.config(style="danger.Outline.TButton", text=f"Move to {dest.name}\n"
                                                                             f"Fight will begin immediately!")
            elif self.check_locked(dest.id):  # if dest is locked
                self.move_button.config(state="disabled", text=f"{dest.name} is locked!")

            self.move_button.grid(row=4, ipadx=10, ipady=2, padx=4, pady=(0, 50), column=col_num, sticky="nsew",
                                  columnspan=1)
            col_num += 1
            self.buttons.append(self.move_button)

        # if there is no npc or item
        if not self.current_location.check_npc() and not self.current_location.check_item():
            self.filler = tk.Label(self)
            self.filler.grid(row=5, column=0, pady=60)

        # if there is a npc
        if self.current_location.check_npc():
            self.talk_button = ttk.Button(self, style="success.Outline.TButton", text=f"Talk",
                                          command=lambda: self.parent.switch_frame(Dialogue))
            if isinstance(self.current_location.npc, Shop):  # if npc is a shop
                self.talk_button.config(text="Enter Store", command=lambda: self.parent.switch_frame(Store))
            self.talk_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=0, pady=50, sticky="nsew", columnspan=1)
            self.buttons.append(self.talk_button)

        # if there is an item 
        if self.current_location.check_item() == 1:
            self.take_button = ttk.Button(self, text=f"Take {self.current_location.item[0].name}",
                                          style="success.Outline.TButton",
                                          command=lambda: self.take_item(self.current_location.item[0]))
            self.take_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=1, pady=50, sticky="nsew", columnspan=1)
            self.can_take()
            self.buttons.append(self.take_button)

        # if there are multiple items
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

        # if there is an enemy
        if self.current_location.check_enemy():
            self.fight_button = ttk.Button(self, style="success.Outline.TButton", text=f"Fight",
                                           command=lambda: self.parent.switch_frame(CombatScreen))
            self.fight_button.grid(row=5, ipadx=10, ipady=2, padx=4, column=2, pady=50, sticky="nsew", columnspan=1)
            self.buttons.append(self.fight_button)

    def update_info(self, content):
        """update current status info"""
        self.info.config(state="normal")
        self.info.insert(tk.END, content)
        self.info.config(state="disabled")
        self.info.see("end")  # automatically goes to bottom

    def can_take(self):
        """checks if player can take"""
        if self.player.check_max_inv():
            if self.take_button:
                self.take_button.config(state="disabled", text="Max inventory!")
            else:
                self.take_dropdown.config(state="disabled", text="Max inventory!")

    def check_locked(self, dest_name):
        """ checks if the player has key for locked location """
        key = self.current_location.dest_locked(dest_name)
        if key:  # if a key is required
            if key in self.player.inv:  # if the key is in player_inv
                return False
        else:
            return False
        return True

    @staticmethod
    def check_boss(dest):
        """checks if dest has a boss"""
        if dest.enemy:
            boss = dest.enemy[0].boss
            if boss:
                return True
            else:
                return False
        return False

    def fight_start_immediately(self):
        """immediately start fight if enemy is a boss type"""
        if self.current_location.enemy:
            if self.current_location.enemy[0].boss:
                self.parent.switch_frame(CombatScreen)

    def unlock(self):
        """unlocks locked location and removes key from inv"""
        key = self.current_location.key
        if key:
            self.update_info(f"Unlocked {self.current_location.desc} with {self.current_location.key.name}!")
            self.player.inv.remove(key)
            self.current_location.key = None
        else:
            return False

    def move(self, dest):
        """moves the player to destination"""
        previous_pos = self.player.location
        self.player.location = dest.id
        self.current_location = self.player.current_location()
        self.unlock()
        self.label_location.config(text=f"Floor {self.player.floor}")
        self.info_location.config(text=f"You are in {self.current_location.name}")
        self.update_info(self.current_location.print_location_info(self.current_location.dest))
        self.update_widgets()
        self.floor_change_cut_scene(previous_pos)
        self.fight_start_immediately()

    def floor_change_cut_scene(self, previous_pos):
        """change to cut scene"""
        floor_changes = ["I", "AA", "AS", "BA"]
        floor_dict = {
            1: ["I"],
            2: ["AA", "AS"],
            3: ["BA"]
        }
        if self.current_location.id in floor_changes:
            if previous_pos in floor_changes:
                for floor, staircases in floor_dict.items():
                    for staircase in staircases:
                        if self.current_location.id == staircase:
                            self.player.floor = floor
                            self.parent.switch_frame(FloorCut)

    def take_item(self, item):
        """take item"""
        item_name = self.player.take_item(item, self.current_location)
        add_item_prompt = f"Added {item_name} to inventory!\n\n"
        self.update_info(add_item_prompt)
        self.update_widgets()

    def update_widgets(self):
        """update widgets to current info"""
        for b in self.buttons:
            b.destroy()
        self.buttons.clear()

        col_num = 0
        for i in range(len(self.current_location.dest)):
            if i == 0:
                col_num = 1
            else:
                col_num = 0

        for dest in self.current_location.dest:
            self.move_button = ttk.Button(self, style="primary.Outline.TButton", text=f"Move to {dest.name}",
                                          command=lambda destination=dest: self.move(destination))
            if self.check_boss(dest):  # if dest has a boss warn player
                self.move_button.config(style="danger.Outline.TButton", text=f"Move to {dest.name}\n"
                                                                             f"Fight will begin immediately!")
            elif self.check_locked(dest.id):
                self.move_button.config(state="disabled", text=f"{dest.name} is locked!")

            self.move_button.grid(row=4, ipadx=10, ipady=2, padx=4, pady=(0, 50), column=col_num, sticky="nsew",
                                  columnspan=1)
            col_num += 1
            self.buttons.append(self.move_button)

        if not self.current_location.check_npc() and not self.current_location.check_item():
            self.filler = tk.Label(self)
            self.filler.grid(row=5, column=0, pady=60)

        if self.current_location.check_npc():
            self.talk_button = ttk.Button(self, style="success.Outline.TButton", text=f"Talk",
                                          command=lambda: self.parent.switch_frame(Dialogue))
            if isinstance(self.current_location.npc, Shop):  # if npc is a shop
                self.talk_button.config(text="Enter Store", command=lambda: self.parent.switch_frame(Store))

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
    """frame to represent the status bar"""

    def __init__(self, parent):
        super().__init__(parent)
        self.player = parent.player
        self.parent = parent
        self.previous_frame = parent.previous_frame[-1]

        no_status_bar = ["NewGame", "GameOver", "MainMenu", "FloorCut"]
        frame_inv = ["Menu", "CombatScreen", "Store"]

        if parent.frame_name not in no_status_bar:
            if parent.frame_name == "Dialogue":
                self.inv = ttk.Button(parent, text=f"Bye.", style="danger.Outline.TButton",
                                      command=lambda: self.switch_frame(Menu))
                parent.previous_frame.append(getattr(sys.modules[__name__], parent.frame_name))
                self.inv.grid(row=6, column=0, sticky="nsew")

            elif parent.frame_name in frame_inv:
                self.inv = ttk.Button(parent, text=f"Open {self.player.name}'s Inventory",
                                      command=lambda: self.switch_frame(Inventory))
                parent.previous_frame.append(getattr(sys.modules[__name__], parent.frame_name))
                self.inv.grid(row=6, column=0, sticky="nsew")

            elif parent.frame_name not in frame_inv:
                self.inv = ttk.Button(parent, text=f"Back to game", style="danger.Outline.TButton",
                                      command=lambda: self.switch_frame(self.previous_frame))
                self.inv.grid(row=6, column=0, sticky="nsew")

        self.grid(row=6, column=0, sticky="nsew")

    def switch_frame(self, frame):
        """switch the frame"""
        self.parent.switch_frame(frame)
        self.inv.destroy()


# generate all items, enemies, spells, npcs, and locations and create an object for each
# noinspection PyTypeChecker
ITEMS = chain(Consumable.generate_from_file("items.txt"), Weapon.generate_from_file("items.txt"),
              Key.generate_from_file("items.txt"), Armour.generate_from_file("items.txt"))
ALL_ITEMS = [item for item in ITEMS]
ENEMIES = Enemy.generate_from_file("enemy.txt")
# noinspection PyTypeChecker
SPELLS = chain(Buff.generate_from_file("spells.txt"), Heal.generate_from_file("spells.txt"))
ALL_SPELLS = [spell for spell in SPELLS]
ALL_ENEMIES = [enemy for enemy in ENEMIES]

NPCS = chain(NPC.generate_from_file("npc.json"), Shop.generate_from_file("shop.json"))
ALL_NPCS = [npc for npc in NPCS]

location_generator = Location.generate_from_file("map.txt")
LOCATIONS = [loc for loc in location_generator]
for loc in LOCATIONS:
    loc.link_dest()


def main():
    """ Start game """
    open('infosave.txt', 'w').close()

    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
