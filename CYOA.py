import time
import random

# colored text


def blue(string):
    return '\033[94m' + string + '\033[0m'


def red(string):
    return '\033[91m' + string + '\033[0m'


def redbold(string):
    return '\033[91m' + '\033[1m' + string + '\033[0m'


def greenbold(string):
    return '\033[92m' + '\033[1m' + string + '\033[0m'


def bluebold(string):
    return '\033[94m' + '\033[1m' + string + '\033[0m'


def yellowbold(string):
    return '\033[93m' + '\033[1m' + string + '\033[0m'


def cyanbold(string):
    return '\033[96m' + '\033[1m' + string + '\033[0m'


def purplebold(string):
    return '\033[95m' + '\033[1m' + string + '\033[0m'


def bold(string):
    return '\033[1m' + string + '\033[0m'


def boldline(string):
    return '\033[1m' + '\033[4m' + string + '\033[0m'


nii = redbold("That is not in your inventory.")  # not in inventory
ntii = redbold("You have nothing in your inventory.")  # nothing in inventory

# Extra stuff
counter = 0  # for oof (??)
inventory = []
invCapacity = 8
health = 100

ping_phrases = ['pls',
                'pls stop',
                'pls stop doing this',
                'pls just continue the game',
                'just play the game',
                'y u do dis',
                'stop',
                'stop doing this']
looping_oof = ["oof"]

# armor
head = None
chest = None
legs = None
feet = None

weapon = None
bp = None  # backpack

# classes


class Room(object):
    def __init__(self, name, description, north, south, east, west, up, down, character, items):
        self.NAME = name
        self.DESCRIPTION = description
        self.north = north
        self.south = south
        self.west = west
        self.east = east
        self.up = up
        self.down = down
        self.character = character
        self.items = items

    def print_descriptions(self):
        print(blue(self.NAME))
        print(self.DESCRIPTION)
        if not self.items:
            pass
        else:
            print("It seems you can take:")
            for items in self.items:
                if items == mechKeyboard or items == drawTablet:
                    print("\t" + redbold(items.name))
                else:
                    print("\t" + bold(items.name.lower()))

    def move(self, directions):
        global current_node
        current_node = globals()[getattr(self, directions)]

    def jump(self):
        if current_node == BEDROOM or current_node == LIVING_ROOM:
            time.sleep(.5)
            print(bold("oh woop there's a ceiling fan there"))
            time.sleep(1)
            print(red("You hit the ceiling fan while it was on. Your head gets chopped off"))
            quit(0)
        else:
            print(redbold("ow"))
            time.sleep(.5)

    def oof(self):
        print(bold("".join(looping_oof)))
        time.sleep(.5)
        looping_oof.append("oof")

    def ping(self):
        if counter <= 2:
            print(boldline("pong"))
        elif counter == 3:
            print(greenbold("don't waste your time doing this"))
        elif counter == 4:
            print(yellowbold("pls you have more important things other than this"))
        elif counter == 5:
            print(cyanbold("pls"))
        elif counter <= 9:
            print(purplebold(random.choice(ping_phrases)))
        elif counter == 10:
            print(redbold("You typed in ping too much that the game got tired of you and decided to quit"))
            quit(0)

    def flush(self):
        if current_node == BATHROOM:
            print(bold("..."))
            time.sleep(1)
            print(redbold("a man rises from the toilet and kills you"))
            quit(0)
        else:
            print(redbold("There's no toilet here u stupid"))

    def play(self):
        if current_node == COMPUTER:
            if head == cookieMask and mechKeyboard in current_node.items and drawTablet in current_node.items:
                print(yellowbold("You played so hard, you died."))
                quit(0)
            elif head == cookieMask or (mechKeyboard in current_node.items and drawTablet in current_node.items):
                print(purplebold("You're so good at this game that the computer exploded"))
                time.sleep(1)
                print(purplebold("And it pops back..."))
                time.sleep(.5)
            else:
                print(redbold("You play the game and rage in frustration at why you're so bad at it..."))
        else:
            print(redbold("You can't play with that."))


class Character(object):
    def __init__(self, name, description, dialogue, inv, hp):
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.inventory = inv
        self.health = hp
        self.isAlive = True
        self.hasTalked = False
        self.counter = 0  # counter for number of encounters of character

    def print_descriptions(self):
        print(greenbold(self.name))
        print(self.description)

    def talk(self):
        if self.dialogue is None:
            print(bluebold("This person doesn't seem to say anything."))
        else:
            print("He says...")
            time.sleep(1)
            print(self.dialogue)
            time.sleep(.5)
            self.hasTalked = True

    def kill(self):
        print(redbold("oh woops you killed " + self.name.lower()))
        self.isAlive = False
        # if None not in self.inventory:


class Enemy(Character):
    def __init__(self, name, description, dialogue, inv, hp, atk, weapon=None):
        super(Enemy, self).__init__(name, description, None, inv, hp)
        self.atk = atk
        self.weapon = weapon

    def print_descriptions(self):
        print(redbold(self.name))
        print(self.description)

    def attack(self):
        global health
        health -= self.atk
        print("You got attacked by %s." % self.name)


class Item(object):
    def __init__(self, name, desc):
        self.name = name
        self.description = desc

    def print_descriptions(self):
        print(purplebold(self.name))
        print(self.description)

    def take(self):
        if len(inventory) == invCapacity:
            print(redbold("Your inventory is full."))
        else:
            if self == mechKeyboard or self == drawTablet:
                inventory.append(self)
                current_node.items.pop(current_node.items.index(self))
                print(cyanbold("You take the " + self.name + "."))
            else:
                inventory.append(self)
                current_node.items.pop(current_node.items.index(self))
                print(cyanbold("You take the " + self.name.lower() + "."))

    def take_all(self):
        while len(current_node.items) != 0:
            for items in current_node.items:
                items.take()
            break

    def drop(self):
        if self == mechKeyboard or self == drawTablet:
            inventory.pop(inventory.index(self))
            current_node.items.append(self)
            print(cyanbold("You drop the " + self.name + '.'))
        else:
            inventory.pop(inventory.index(self))
            current_node.items.append(self)
            print(cyanbold("You drop the " + self.name.lower() + '.'))

    def drop_all(self):
        while len(inventory) != 0:
            for items in inventory:
                items.drop()


class Bed(Item):
    def __init__(self, name, desc):
        super(Bed, self).__init__(name, desc)
        self.body = head

    def equip(self):
        global head
        if head is not None:
            print(redbold("You're already wearing something."))
        else:
            time.sleep(1)
            print("ok")
            time.sleep(.5)
            head = bed
            print(bluebold("You wear the bed."))
            inventory.pop(inventory.index(self))

    def unequip(self):
        global head
        if head is None:
            print(redbold("You aren't wearing anything."))
        else:
            head = None
            inventory.append(bed)
            print(bluebold("You take off the bed."))

    def drink(self):
        time.sleep(1)
        print("ok")
        time.sleep(.5)
        print(bluebold("You drink the bed."))
        inventory.pop(inventory.index(bed))


class Weapon(Item):
    def __init__(self, name, desc, damage):
        super(Weapon, self).__init__(name, desc)
        self.damage = damage

    def equip(self):
        global weapon
        if weapon is None:
            inventory.poap(inventory.index(self))
            weapon = self
            print(cyanbold("You equipped the " + self.name.lower() + "."))
        else:
            print(redbold("You already have a weapon equipped."))

    def unequip(self):
        global weapon
        if weapon is not None:
            inventory.append(self)
            weapon = None
            print(redbold("You unequipped the " + self.name.lower() + '.'))
        else:
            print(redbold("You don't have a weapon to unequip."))


    def hit(self): current_node.character.health -= self.damage

    def check_stats(self): print(bluebold("Damage: ") + str(self.damage))


class Sword(Weapon):
    def __init__(self, name, desc, damage):
        super(Sword, self).__init__(name, desc, damage)

    def stats(self):
        print(bluebold(self.name + ":"))
        print("\t" + bold("Damage: %d" % self.damage))

    def hit(self):
        random_number = random.randint(0, 10)
        if random_number % 2 == 0:  # crit
            current_node.character.health -= damage * 2
        else:
            current_Node.character.health -= damage

    def equip(self):
        global weapon
        if weapon is None:
            inventory.pop(inventory.index(self))
            weapon = self
            print(cyanbold("You equipped the " + self.name.lower() + "."))
        else:
            print(redbold("You already have a weapon equipped."))

    def unequip(self):
        global weapon
        if weapon is not None:
            inventory.append(self)
            weapon = None
            print(cyanbold("You unequipped the " + self.name.lower() + '.'))
        else:
            print(redbold("You don't have a weapon to unequip."))


class BackwardsGun(Weapon):
    def __init__(self, name, desc):
        super(BackwardsGun, self).__init__(name, desc, 100)

    def shoot(self):
        print(redbold("you shot yourself and died"))
        quit(0)


class Hammer(Weapon):
    def __init__(self, name, desc):
        super(Hammer, self).__init__(name, desc, 1)

    def break_door(self):
        print(bold("..."))
        time.sleep(1)
        print(bluebold("Why is this hammer made of rubber?"))
        time.sleep(.5)


class Consumable(Item):
    def __init__(self, name, desc):
        super(Consumable, self).__init__(name, desc)

    def use(self):
        inventory.pop(inventory.index(self))


class Food(Consumable):
    def __init__(self, name, desc):
        super(Food, self).__init__(name, desc)

    def eat(self):
        inventory.pop(inventory.index(self))
        print(purplebold("yummy"))


class Drink(Consumable):
    def __init__(self, name, desc):
        super(Drink, self).__init__(name, desc)

    def drink(self):
        inventory.pop(inventory.index(self))
        print(bluebold("You drink the %s and its bottle disappears...") % self.name.lower())


class Container(Item):
    def __init__(self, name, desc, capacity):
        super(Container, self).__init__(name, desc)
        self.capacity = capacity

    def equip(self):
        global bp
        global invCapacity
        bp = self
        invCapacity += self.capacity
        inventory.pop(inventory.index(self))
        print(cyanbold("You equipped the %s. You got +%d inventory space." % (self.name.lower(), self.capacity)))

    def unequip(self):
        global bp
        global invCapacity
        bp = None
        invCapacity -= self.capacity
        inventory.append(self)
        print(cyanbold("You unequipped the %s. You now have -%d inventory space." % (self.name.lower(), self.capacity)))
        if len(inventory) > invCapacity:
            while len(inventory) > invCapacity:
                ri = random.choice(inventory)
                ri.drop()

    def stats(self):
        print(bluebold(self.name) + ":")
        print("\t" + bold("Capacity: +%d" % self.capacity))


class Box(Container):
    def __init__(self, name, desc):
        super(Box, self).__init__(name, desc, 4)

    def put_item_in(self, item_name):
        if self.inventory.len() == capacity:
            print(redbold("Your inventory is full."))
        else:
            self.inventory.append(item_name)
            print(cyanbold("You put the %s in the box") % item_name.lower())

    def wear(self):
        global head
        head = self


class Ball(Item):
    def __init__(self, name, desc):
        super(Ball, self).__init__(name, desc)

    def throw(self):
        inventory.pop(inventory.index(ball))
        print("You throw the ball and in a blink of "
              "an eye, one of the dogs zoom in a blink "
              "of an eye and catch the ball.")
        time.sleep(4)
        print(yellowbold("The dog then hovers and starts floating to orbit."))
        time.sleep(3)
        print(yellowbold("The dog comes back with a bucket with even more balls."))
        time.sleep(1)
        current_node.items.append(ball)


class Wearable(Item):
    def __init__(self, name, desc, body):
        super(Wearable, self).__init__(name, desc)
        self.body = body

    def equip(self):
        if self.body is not None:
            print(redbold("You're already wearing something."))
        else:
            self.body = self
            inventory.pop(inventory.index(self))
            print(bluebold("You wear the " + self.name))

    def unequip(self):
        if self.body is None:
            print(redbold("You aren't wearing anything."))
        else:
            self.body = None
            print(bluebold("You take off the " + self.name))
            inventory.append(self)


class Mask(Wearable):
    def __init__(self, name, desc):
        super(Mask, self).__init__(name, desc, head)

    def equip(self):
        global head
        if head is not None:
            print(redbold("You're already wearing something."))
        else:
            head = self
            inventory.pop(inventory.index(self))
            print(bluebold("You wear the " + self.name.lower() + "."))

    def unequip(self):
        global head
        if head is None:
            print(redbold("You aren't wearing anything."))
        else:
            head = None
            print(bluebold("You take off the " + self.name.lower() + "."))
            inventory.append(self)


class Shirt(Wearable):
    def __init__(self, name, desc):
        super(Shirt, self).__init__(name, desc, chest)

    def equip(self):
        global chest
        if chest is not None:
            print(redbold("You're already wearing something."))
        else:
            chest = self
            inventory.pop(inventory.index(self))
            print(bluebold("You wear the " + self.name.lower() + "."))

    def unequip(self):
        global chest
        if chest is None:
            print(redbold("You aren't wearing anything."))
        else:
            print(bluebold("You take off the " + self.name.lower() + "."))
            chest = None
            inventory.append(self)


class Book(Item):
    def __init__(self, name, desc, read_text):
        super(Book, self).__init__(name, desc)
        self.readText = read_text

    def read(self):
        print(self.read_text)


def attack():
    global eacn
    rn = random.randint(0, 5)  # random number
    atk = 1  # default damage (with no weapon)
    if weapon is not None:
        atk = weapon.damage

    if rn % 2 == 0:
        current_node.character.health -= atk
        if current_node.character.health == 0:
            print(cyanbold("You killed the %s." % current_node.character.name))
            current_node.character = None
            eacn = False
        else:
            print(cyanbold("You attacked the %s." % current_node.character.name))
            current_node.character.attack()
    else:
        print(redbold("You missed."))
        current_node.character.attack()


# Characters and Items


Cookie = Character("Cookiezi", "This person seems to be sitting behind a desk with a computer, mashing his keyboard\n"
                               "quietly, but you could definitely hear it. On his monitor, he seems to be clicking "
                               "circles...", None, None, None)
jeff = Character("jeff", "he's sitting on a chair playing a game on the left side of the room", "stop", ['pen'], 50)
spider = Enemy("Spider", "A fairly large spider with a venomous aura coming out of it.", None, [], 10, 3)

cookie = Food("Cookie", "A chocolate chip cookie. Seems delicious.")
bed = Bed("Bed", "Your average-looking bed.")
ball = Ball("Ball", "A regular, old tennis ball.")
techRoomKey = Item("Key", "The key has a message engraved that says 'Tech Room Key'...")
backwardsGun = BackwardsGun("Gun", "It's a gun, but its barrel is pointing the opposite way.")
water = Drink("Water Bottle", "A water bottle that has an off-center label that says 'Fiji'.")
cookieMask = Mask("Mask", "A mask of a smiling man wearing glasses with slits in the eyes. Wonder what you'd use it "
                          "for.")
shirt = Shirt("Shirt", "Just a plain white shirt.")
weirdBag = Container("Backpack", "Just a regular backpack.", 4)
sword = Sword("Iron Sword", "A normal iron sword.", 10)


mechKeyboard = Item("HyperX Alloy FPS Keyboard", "A mechanical keyboard with Cherry MX red switches.")
drawTablet = Item("Huion Graphics Tablet", "A normal graphics tablet. Seems cheap.")

testitem = Item("test item", "just a test item")

# Rooms

BEDROOM = Room("Bedroom",
               "You are in a bedroom full of anime posters, figures, etc."
               "\nYou have a computer sitting on a desk to your north, and a door to the east.",
               "COMPUTER", None, "HALLWAY", None, None, None, None, [bed, shirt, sword])
COMPUTER = Room("Computer",
                "On the desk lies a computer with a crappy membrane keyboard and a mouse. "
                "On the computer lies a weird game called 'osu!'...",
                None, "BEDROOM", "HALLWAY", None, None, None, None, [weirdBag])
HALLWAY = Room("Hallway",
               "The hallway has a few paintings with a dull red carpet on the wooden floor."
               "\nThere are stairs leading down to the south, as well as another room across yours.",
               "DINING_ROOM", "EMPTY_ROOM", "BATHROOM", "BEDROOM", None, "DINING_ROOM", spider, [])
EMPTY_ROOM = Room("Empty Room",
                  "You enter an empty room, but in the southern-most corner there's a table with what seems to be "
                  "a drawing tablet, as well as a keyboard.",
                  "HALLWAY", "TABLE", None, None, None, None, jeff, [backwardsGun])
TABLE = Room("Table",
             "On the table there is a key and empty boxes with labels saying "
             "'HyperX Alloy FPS Mechanical Gaming Keyboard' as well as another\n"
             "box that says 'Huion Graphics Tablet'...",
             "EMPTY_ROOM", None, None, None, None, None, None, [techRoomKey, mechKeyboard, drawTablet])
BATHROOM = Room("Bathroom",
                "The bathroom is set with two sinks, a bathtub and a toilet.\n"
                "There are also toiletries sitting on top of the sink counter.",
                None, None, None, "HALLWAY", None, None, None, [])
DINING_ROOM = Room("Dining Room",
                   "The dining room has a table with a fancy green cloth and a basket full of fake fruit."
                   "\nThe kitchen leads east, and the living room to the west.",
                   None, "HALLWAY", "KITCHEN1", "LIVING_ROOM", "HALLWAY", None, None, [cookie])
KITCHEN1 = Room("Entrance to Kitchen",
                "In the kitchen there's a refrigerator and a pantry full of "
                "food,\nas well as a long counter to eat food on. There's more stuff farther south.",
                "DINING_ROOM", "KITCHEN2", None, None, None, None, None, [])
KITCHEN2 = Room("Farther Side of Kitchen",
                "This side of the Kitchen has a flat screen tv mounted to the wall\nwith a smaller table below "
                "it that holds the cable box, and an old,\nuseless game console. There's what seems to be a "
                "laundry room to the\nwest as well as a slide door leading outside east.",
                "KITCHEN1", None, "BACKYARD1", "LAUNDRY_ROOM", None, None, None, [])
LAUNDRY_ROOM = Room("Laundry Room",
                    "The Laundry Room has a washing and drying machine, as well as a cabinet.",
                    "CABINET", None, "KITCHEN2", None, None, None, None, [water])
CABINET = Room("Inside of Cabinet",
               "Inside the cabinet contains jackets and sweaters. The shelf above it has a \n"
               "few boxes put for storage, but there's a paper mask of a man's face here...",
               # osu! joke, don't worry about it
               None, "LAUNDRY_ROOM", "KITCHEN2", None, None, None, None, [cookieMask])
BACKYARD1 = Room("Backyard",
                 "The empty backyard had little to no grass, making it look like a desert.\nNot only that, there "
                 "are two dogs that seem to not care about it at all\nand just have fun with the tennis balls "
                 "around them.",
                 "BACKYARD2", None, None, "KITCHEN2", None, None, None, [ball])
BACKYARD2 = Room("Farther side of the Backyard",
                 "This side of the backyard has an unused grill and a bench lying at the wall of the house. And "
                 "more tennis balls...", None, "BACKYARD1", None, None, None, None, None, [ball])
LIVING_ROOM = Room("Living Room",
                   "The living room has couches set with a large TV.\nThe exit seems to go the south.",
                   None, "DOOR", "DINING_ROOM", None, None, None, None, [])
DOOR = Room("Door",
            "You stand at the exit of the house, where lies a bunch of shoes.\nThe door faces west, "
            "and there's another door to the south.",
            "LIVING_ROOM", "LOCKED_DOOR", None, 'PORCH', None, None, None, [])
LOCKED_DOOR = Room("Locked Door", "This room's door is locked.", "DOOR", None, None, None, None, None, None, [])
PORCH = Room("Porch",
             "You exit the house into the porch, where there are short, dull, plants.\nYou can go more to "
             "the west to exit the porch and into the driveway.",
             None, None, "DOOR", "DRIVEWAY", None, None, None, [])
DRIVEWAY = Room("Driveway",
                "The drive way has a basketball hoop, but to the west you see a store with a sign that says... "
                "Walm.\nYou can go back north into the porch.", "PORCH", None, None, "STORE", None, None, None, [])
STORE = Room("Walm", "Sorry to keep your hopes up, this store is closed.",
             None, None, "DRIVEWAY", None, None, None, None, [])

TECH_ROOM = Room("Tech Room",
                 "The door you open leads you into room filled with bright looking technology.\n"
                 "The whole room seems to be white-ish. The whole room seems to be some sort of 'man cave'.\n"
                 "You feel so intimidated that you shouldn't touch any of the equipment.",
                 "DOOR", None, None, None, None, None, Cookie, [])

dir1 = ['north', 'south', 'east', 'west', 'up', 'down']
dir2 = ['n', 's', 'e', 'w', 'u', 'd']

current_node = BEDROOM
current_node_hasChanged = True
eacn = False  # enemy at current node

time.sleep(.5)

while True:
    if health == 0:
        print(redbold("you died"))
        break
    print(redbold("Health: ") + str(health))
    if current_node_hasChanged:
        current_node.print_descriptions()
        current_node_hasChanged = False
        if current_node.character is not None and current_node.character.isAlive:
            if isinstance(current_node.character, Enemy):
                print(redbold("You've walked into %s." % current_node.character.name.lower()))
                eacn = True
            else:
                current_node.character.print_descriptions()

    command = input('>').lower()

    if command == 'quit':
        quit(0)
    elif 'check' in command or 'look at' in command:
        if not inventory and weapon is None:
            print(ntii)
        else:
            if command.strip() == 'check' or command.strip() == 'look at':
                check_cmd = input("What do you want to check?\n>").lower()
                itm = None
                for item in inventory:
                    if item.name.lower() == check_cmd:
                        itm = item

                if check_cmd == 'nvm' or check_cmd == 'nothing':
                    print("ok")
                elif itm is None:
                    print(nii)
                else:
                    itm.print_descriptions()
            else:
                itm = None
                for item in inventory:
                    if item.name.lower() in command:
                        itm = item

                if itm is None:
                    print(nii)
                else:
                    itm.print_descriptions()
    elif 'inv' in command or 'inventory' in command:
        if not inventory:
            print(ntii)
        else:
            print("Your inventory:")
            for item in inventory:
                if item == mechKeyboard or item == drawTablet:
                    print("\t" + purplebold(item.name))
                else:
                    print("\t" + bold(item.name.lower()))
            if bp is not None:
                print("You have a base capacity of %d, but you have a backpack "
                      "that gives you +%d space." % (invCapacity, bp.capacity))
            else:
                print("You have a base capacity of %d." % invCapacity)
            print("You have %s spaces left." % (invCapacity - len(inventory)))
    elif 'armor' in command:
        if head is None and chest is None and legs is None and feet is None:
            print(redbold("You're wearing nothing."))
        else:
            print("You are wearing:")
            if head is not None:
                print("\t" "Head: " + bold(head.name.lower()))
            if chest is not None:
                print("\t" + "Chest: " + bold(chest.name.lower()))
            if legs is not None:
                print("\t" + "Legs: " + bold(legs.name.lower()))
            if feet is not None:
                print("\t" + "Feet: " + bold(feet.name.lower()))

            if weapon is not None:
                print("\t" + "Weapon: " + bold(weapon.name.lower()))
            if bp is not None:
                print("\t" + "Backpack: " + bold(bp.name.lower()) + " +" + bp.capacity)
    elif 'look' in command or command == 'l':
        current_node.print_descriptions()
        if current_node.character is None or not current_node.character.isAlive:
            continue
        else:
            current_node.character.print_descriptions()
    elif 'jump' in command:
        current_node.jump()
    elif 'yeet' in command:
        print(bold('yeet'))
    elif command == "oof":
        current_node.oof()
    elif command == "ping":
        current_node.ping()
        counter += 1
    elif command == 'flush':
        current_node.flush()
    elif command == 'beep':
        print('boop')
    elif command in dir2:
        if eacn:
            print(redbold("There's an enemy in the room. You can't leave unless you kill it."))
        else:
            pos = dir2.index(command)
            command = dir1[pos]
            try:
                current_node.move(command)
                current_node_hasChanged = True
            except KeyError:
                print(redbold("You can't go that way."))
                current_node_hasChanged = False
    elif command in dir1:
        if eacn:
            print(redbold("There's an enemy in the room. You can't leave unless you kill it."))
        else:
            try:
                current_node.move(command.lower())
                current_node_hasChanged = True
            except KeyError:
                print(red("You can't go that way."))
                current_node_hasChanged = False
    elif 'wear' in command:
        if not inventory:
            print(ntii)
        else:
            if command.strip() == 'wear':
                wear_cmd = input("What do you want to wear?\n>").lower().strip()
                itm = None
                for item in inventory:
                    if item.name.lower() in wear_cmd:
                        itm = item

                if wear_cmd == 'nvm' or wear_cmd == 'nothing':
                    print(ok)
                elif itm is None:
                    print(nii)
                else:
                    if issubclass(type(itm), Wearable) or isinstance(itm, Bed):
                        itm.equip()
                    else:
                        print(redbold("You can't wear that."))
            else:
                itm = None
                for item in inventory:
                    if item.name.lower() in command:
                        itm = item

                if itm is None:
                    print(nii)
                else:
                    if issubclass(type(itm), Wearable) or isinstance(itm, Bed):
                        itm.equip()
                    else:
                        print(redbold("You can't wear that."))
    elif 'take off' in command or 'unequip' in command:
        if head is None and chest is None and legs is None and feet is None and weapon is None and bp is None:
            print(redbold("You aren't wearing anything."))
        else:
            if command == 'take off' or command.strip() == 'unequip':
                unequip_command = input("What do you want to take off?\n>").lower()
                if head is not None:
                    if head.name.lower() in unequip_command:
                        head.unequip()
                elif chest is not None:
                    if chest.name.lower() in unequip_command:
                        chest.unequip()
                elif legs is not None:
                    if legs.name.lower() in unequip_command:
                        legs.unequip()
                elif feet is not None:
                    if feet.name.lower() in unequip_command:
                        feet.unequip()
                elif weapon is not None:
                    if weapon.name.lower() in unequip_command:
                        weapon.unequip()
                elif bp is not None:
                    if bp.name.lower() in unequip_command:
                        bp.unequip()
                else:
                    print(redbold("You aren't wearing that."))
            else:
                if head is not None:
                    if head.name.lower() in command:
                        head.unequip()
                elif chest is not None:
                    if chest.name.lower() in command:
                        chest.unequip()
                elif legs is not None:
                    if legs.name.lower() in command:
                        legs.unequip()
                elif feet is not None:
                    if feet.name.lower() in command:
                        feet.unequip()
                elif weapon is not None:
                    if weapon.name.lower() in command:
                        weapon.unequip()
                elif bp is not None:
                    if bp.name.lower() in command:
                        bp.unequip()
                else:
                    print(redbold("You aren't wearing anything."))
    elif 'equip' in command:
        if not inventory:
            print(ntii)
        else:
            if command.strip() == 'equip':
                equip_cmd = input("What do you want to equip?\n>").lower()
                itm = None
                for item in inventory:
                    if item.name.lower() in equip_cmd:
                        itm = item

                if itm is None:
                    print(nii)
                else:
                    if isinstance(itm, Container) or issubclass(type(itm), Weapon):
                        itm.equip()
                    else:
                        print(redbold("You can't equip that."))
            else:
                itm = None
                for item in inventory:
                    if item.name.lower() in command:
                        itm = item

                if itm is None:
                    print(nii)
                else:
                    if isinstance(itm, Container) or issubclass(type(itm), Weapon):
                        itm.equip()
                    else:
                        print(redbold("You can't equip that."))
    elif 'take' in command or 'pickup' in command.strip():
        if not current_node.items:
            print(redbold("There is nothing here to take."))
        else:
            if command.strip() == 'take' or command.strip() == 'pickup':
                take_command = input("What do you want to take?\n>").lower().strip()
                for i, item in enumerate(current_node.items):
                    if 'all' in take_command:
                        item.take_all()
                    elif take_command == item.name.lower():
                        item.take()
                    elif 'nothing' in take_command or 'nevermind' in take_command or 'nvm' in take_command:
                        print("ok")
                        break
                    else:
                        if len(current_node.items) == 1:
                            print(redbold("That item isn't here."))
                        else:
                            if i != len(current_node.items) - 1:
                                print(redbold("That item isn't here."))
            else:
                for i, item in enumerate(current_node.items):
                    if 'all' in command:
                        item.take_all()
                    elif item.name.lower() in command:
                        item.take()
                    else:
                        if len(current_node.items) == 1:
                            print(redbold("That item isn't here."))
                        else:
                            if i != len(current_node.items) - 1:
                                pass
                            else:
                                print(redbold("That item isn't here."))
    elif 'drop' in command:
        if not inventory:
            print(ntii)
        else:
            if command.strip() == 'drop':
                drop_command = input("What do you want to drop?\n>").lower()
                for i, item in enumerate(inventory):
                    if 'all' in command:
                        item.drop_all()
                    elif drop_command == item.name.lower():
                        item.drop()
                    elif 'nothing' in drop_command or 'nevermind' in drop_command or 'nvm' in drop_command:
                        print("ok")
                        break
                    else:
                        if i != len(inventory) - 1:
                            continue
                        else:
                            print(redbold("You don't have that item."))
            else:
                for i, item in enumerate(inventory):
                    if 'all' in command:
                        item.drop_all()
                    elif item.name.lower() in command:
                        item.drop()
                        break
                    else:
                        if i != len(inventory) - 1:
                            continue
                        else:
                            print(redbold("You don't have that item."))
    elif 'throw' in command:
        if not inventory:
            print(ntii)
        else:
            if command.strip() == 'throw':
                throw_command = input("What do you want to throw?\n>").lower()
                for i, item in enumerate(inventory):
                    if throw_command == item.name.lower():
                        if isinstance(item, Ball):
                            item.throw()
                        else:
                            item.drop()
                    elif 'nothing' in throw_command or 'nevermind' in throw_command or 'nvm' in throw_command:
                        print("ok")
                        break
                    else:
                        if i != len(inventory) - 1:
                            continue
                        else:
                            print(redbold("You don't have that item."))
            else:
                for i, item in enumerate(inventory):
                    if item.name.lower() in command:
                        if isinstance(item, Ball):
                            item.throw()
                        else:
                            item.drop()
                    else:
                        if i != len(inventory) - 1:
                            continue
                        else:
                            print(redbold("You don't have that item."))
    elif 'talk' in command:
        if current_node.character is None or not current_node.character.isAlive:
            print(redbold("There is no one here."))
        elif command == 'talk':
            talk_command = input("Who do you want to talk to?\n>").lower().strip()
            if talk_command == current_node.character.name:
                if current_node.character.isAlive:
                    current_node.character.talk()
                else:
                    print(redbold("That person is dead."))
            elif 'noone' in talk_command or 'nevermind' in talk_command or 'nvm' in talk_command:
                print("ok")
            else:
                print(redbold("That person isn't here."))
        elif current_node.character.name.lower() in command:
            if current_node.character.isAlive:
                current_node.character.talk()
            elif not current_node.character.isAlive:
                print(redbold("That person is dead."))
            else:
                print(redbold("That person isn't here."))
        else:
            print(redbold("That person isn't here."))
    elif 'open door' in command:
        if current_node == LOCKED_DOOR:
            if techRoomKey in inventory:
                current_node = TECH_ROOM
                print(bluebold("You open the door.\n"))
                current_node_hasChanged = True
            else:
                print(redbold("You don't have a key."))
        else:
            print(redbold("There is no locked door to open."))
    elif 'drink' in command:
        if not inventory:
            print(ntii)
        else:
            if command == 'drink':
                drink_command = input("What do you want to drink?\n>").lower()
                for i, item in enumerate(inventory):
                    if item.name.lower() in drink_command:
                        if isinstance(item, Drink) or isinstance(item, Bed):
                            item.drink()
                            break
                        else:
                            print("You can't drink that.")
                    elif 'nothing' in drink_command or 'nevermind' in drink_command or 'nvm' in drink_command:
                        print("ok")
                        break
                    else:
                        if i != len(inventory) - 1:
                            pass
                        else:
                            print("You don't have that in your inventory.")
            else:
                for i, item in enumerate(inventory):
                    if item.name.lower() in command:
                        if isinstance(item, Drink) or isinstance(item, Bed):
                            item.drink()
                            break
                        else:
                            if i != len(inventory) - 1:
                                pass
                            else:
                                print("You don't have that in your inventory.")
    elif 'play' in command:
        if 'computer' in command or 'osu' in command:
            current_node.play()
        elif 'myself' in command:
            print('are you ok?')
        else:
            if command == 'play':
                play_command = input("What do you want to play?\n>").lower().strip()
                if play_command == 'computer' or play_command == 'osu':
                    current_node.play()
                elif play_command == 'myself':
                    print('are you ok?')
                elif 'nothing' in take_command or 'nevermind' in take_command or 'nvm' in take_command:
                    print("ok")
            else:
                print(nii)
    elif 'kill' in command:
        if command == 'kill':
            kill_command = input("Who do you want to kill?\n>").lower()
            if kill_command == 'me' or kill_command == 'self':
                time.sleep(2)
                print("ok")
                time.sleep(.5)
                while health != 0:
                    health -= 1
                    print(redbold("Health: ") + str(health))
                    time.sleep(.01)
                    if health == 0:
                        break
            elif kill_command == current_node.character.name.lower():
                if current_node.character.isAlive:
                    current_node.character.kill()
                else:
                    print(redbold("That person is dead."))
            else:
                print(redbold("That person isn't here."))
        elif current_node.character is None:
            print(redbold("There is no one here."))
        elif current_node.character.name.lower() in command:
            if current_node.character.isAlive:
                current_node.character.kill()
            else:
                print(redbold("That person is dead."))
        else:
            print(redbold("That person isn't here."))
    elif 'suicide' in command:
        time.sleep(2)
        print("ok")
        time.sleep(.5)
        while health != 0:
            health -= 1
            print(redbold("Health: ") + str(health))
            time.sleep(.01)
    elif 'stats' in command:
        if weapon is None and bp is None:
            print(redbold("You don't have a weapon or a backpack."))
        else:
            if weapon is not None:
                weapon.stats()
            if bp is not None:
                bp.stats()
    elif 'attack' in command:
        if command.strip() == 'attack':
            atk_command = input("Who do you want to attack?\n>").lower()
            if current_node.character is not None:
                if atk_command == current_node.character.name.lower():
                    if isinstance(current_node.character, Enemy):
                        attack()
                    elif isinstance(current_node.character, Character):
                        current_node.character.kill()
                    else:
                        print(redbold("That person isn't here."))
                else:
                    print(redbold("That person isn't here."))
            elif 'no one' in atk_command.strip() or 'nvm' in atk_command.strip() or 'nevermind' in atk_command.strip():
                print('ok')
            else:
                if 'self' in atk_command or 'myself' in atk_command:
                    print('are you ok?')
                else:
                    print(redbold("That person isn't here."))
        else:
            if current_node.character is None:
                if 'self' in command or 'myself' in command:
                    print('are you ok?')
                else:
                    print(redbold("That person isn't here."))
            else:
                if current_node.character.name.lower() in command:
                    if isinstance(current_node.character, Enemy):
                        attack()
                    elif isinstance(current_node.character, Character):
                        current_node.character.kill()
                else:
                    print(redbold("That person isn't here."))
    else:
        print("Command not Recognized")
        current_node_hasChanged = False
