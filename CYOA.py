import time
import random

# colored text


def bold_text(string):
    return '\033[1m' + string + '\033[0m'


def blue_text(string):
    return '\033[94m' + string + '\033[0m'


def bold_underline(string):
    return '\033[1m' + '\033[4m' + string + '\033[0m'


def red_bold(string):
    return '\033[91m' + '\033[1m' + string + '\033[0m'


def green_bold(string):
    return '\033[92m' + '\033[1m' + string + '\033[0m'


def blue_bold(string):
    return '\033[94m' + '\033[1m' + string + '\033[0m'


def yellow_bold(string):
    return '\033[93m' + '\033[1m' + string + '\033[0m'


def cyan_bold(string):
    return '\033[96m' + '\033[1m' + string + '\033[0m'


def purple_bold(string):
    return '\033[95m' + '\033[1m' + string + '\033[0m'


# Extra stuff
counter = 0  # for ping
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


# classes


class Room(object):
    def __init__(self, name, description, north, south, east, west, up, down, character, items):
        self.name = name
        self.description = description
        self.north = north
        self.south = south
        self.west = west
        self.east = east
        self.up = up
        self.down = down
        self.character = character
        self.items = items

    def print_descriptions(self):
        print(blue_text(self.name))
        print(self.description)
        if not self.items:
            pass
        else:
            print("It seems you can take:")
            for items in self.items:
                if items == drawTablet or items == mechKeyboard:
                    print("\t" + red_bold(items.name))
                else:
                    print("\t" + bold_text(items.name.lower()))

    def move(self, directions):
        global current_node
        current_node = globals()[getattr(self, directions)]

    def jump(self):
        if current_node == BEDROOM or current_node == LIVING_ROOM:
            time.sleep(.5)
            print(bold_text("oh woop there's a ceiling fan there"))
            time.sleep(1)
            print(red_bold("You hit the ceiling fan while it was on. Your head gets chopped off"))
            quit(0)
        else:
            print(red_bold("ow"))
            time.sleep(.5)

    def oof(self):
        print(bold_text("".join(looping_oof)))
        time.sleep(.5)
        looping_oof.append("oof")

    def ping(self):
        if counter <= 2:
            print(bold_underline("pong"))
        elif counter == 3:
            print(green_bold("don't waste your time doing this"))
        elif counter == 4:
            print(yellow_bold("pls you have more important things other than this"))
        elif counter == 5:
            print(cyan_bold("pls"))
        elif counter <= 9:
            print(purple_bold(random.choice(ping_phrases)))
        elif counter == 10:
            print(red_bold("You typed in ping too much that the game got tired of you and decided to quit"))
            quit(0)

    def flush(self):
        if current_node == BATHROOM:
            print(bold_text("..."))
            time.sleep(1)
            print(red_bold("a man rises from the toilet and kills you"))
            quit(0)
        else:
            print(red_bold("There's no toilet here u stupid"))

    def play(self):
        if head == cookieMask or (mechKeyboard in COMPUTER.items and drawTablet in COMPUTER.items):
            print(purple_bold("You're so good at this game that the computer exploded"))
            time.sleep(1)
            print(purple_bold("And it pops back..."))
        else:
            print(red_bold("You play the game and rage in frustration at why you're so bad at it..."))


class Character(object):
    def __init__(self, name, description, dialogue, inv, hp):
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.inventory = inv
        self.health = hp
        self.isAlive = True
        self.hasTalked = False

    def print_descriptions(self):
        print(green_bold(self.name))
        print(self.description)

    def talk(self):
        if self.dialogue is None:
            print(blue_bold("This person doesn't seem to say anything."))
        else:
            print("He says...")
            time.sleep(1)
            print(self.dialogue)
            time.sleep(.5)
            self.hasTalked = True

    def kill(self):
        print(red_bold("oh woops you killed " + self.name.lower()))
        self.isAlive = False


class Item(object):
    def __init__(self, name, desc):
        self.name = name
        self.description = desc

    def print_descriptions(self):
        print(purple_bold(self.name))
        print(self.description)

    def take(self):
        if len(inventory) == invCapacity:
            print(red_bold("Your inventory is full."))
        else:
            inventory.append(self)
            current_node.items.pop(current_node.items.index(self))
            print(cyan_bold("You take the " + self.name.lower() + "."))

    def take_all(self):
        if len(inventory) == invCapacity:
            print(red_bold("Your inventory is full."))
        else:
            while len(current_node.items) != 0:
                for items in current_node.items:
                    items.take()

    def drop(self):
        inventory.pop(inventory.index(self))
        current_node.items.append(self)
        print(cyan_bold("You drop the " + self.name.lower() + '.'))

    def drop_all(self):
        while len(inventory) != 0:
            for items in inventory:
                items.drop()


class Bed(Item):
    def __init__(self, name, desc):
        super(Bed, self).__init__(name, desc)
        self.body = head

    def drink(self):
        time.sleep(1)
        print("ok")
        time.sleep(.5)
        print(blue_bold("You drink the bed."))
        inventory.pop(inventory.index(bed))

    def equip(self):
        global head
        if head is not None:
            print(red_bold("You're already wearing something."))
        else:
            time.sleep(1)
            print("ok")
            time.sleep(.5)
            head = bed
            print(blue_bold("You wear the bed."))
            inventory.pop(inventory.index(self))

    def unequip(self):
        global head
        if head is None:
            print(red_bold("You aren't wearing anything."))
        else:
            head = None
            inventory.append(bed)
            print(blue_bold("You take off the bed."))


class Weapon(Item):
    def __init__(self, name, desc, damage):
        super(Weapon, self).__init__(name, desc)
        self.damage = damage

    def hit(self): current_node.character.health -= self.damage

    def check_stats(self): print(blue_bold("Damage: ") + str(self.damage))


class Sword(Weapon):
    def __init__(self, name, desc, damage):
        super(Sword, self).__init__(name, desc, damage)

    def hit(self):
        random_number = random.randint(0, 10)
        if random_number % 2 == 0:  # crit
            current_node.character.health -= damage * 2
        else:
            current_Node.character.health -= damage


class BackwardsGun(Weapon):
    def __init__(self, name, desc):
        super(BackwardsGun, self).__init__(name, desc, 100)

    def shoot(self):
        print(red_bold("you shot yourself and died"))
        quit(0)


class Hammer(Weapon):
    def __init__(self, name):
        super(Hammer, self).__init__(name, desc, 1)

    def break_door(self):
        print(bold_text("..."))
        time.sleep(1)
        print(blue_bold("Why is this hammer made of rubber?"))


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
        print(purple_bold("yummy"))


class Drink(Consumable):
    def __init__(self, name, desc):
        super(Drink, self).__init__(name, desc)

    def drink(self):
        inventory.pop(inventory.index(self))
        print(blue_bold("You drink the water, but its bottle disappears..."))


class Container(Item):
    def __init__(self, name, desc, capacity):
        super(Container, self).__init__(name, desc)
        self.capacity = capacity
        self.inventory = []
        self.isOpen = False
        self.isEmpty = False

    def lookin(self):
        if not self.inventory:
            print(red_bold("This " + self.name.lower() + " doesn't have anything in it."))
        else:
            print("In " + self.name.lower() + ":")
            for items in self.inventory:
                print(bold_text("\t" + items.name.lower()))

    def put_item_in(self, item_name):
        if len(self.inventory) == self.capacity:
            print(red_bold("This inventory is full."))
        else:
            self.inventory.append(item_name)
            inventory.pop(inventory.index(item_name))
            print(cyan_bold("You put the " + item_name.name.lower() + " in the " + self.name.lower() + "."))

    def take_out(self, item_name):
        self.inventory.pop(self.inventory.index(item_name))
        inventory.append(item_name)
        print(cyan_bold("You take out the " + item_name.name.lower() + " from the " + self.name.lower() + "."))

    def open(self):
        if not self.isOpen:
            self.isOpen = True
            print(blue_bold("You open the " + self.name.lower() + "."))
        else:
            print(red_bold("That is already open."))

    def close(self):
        if self.isOpen:
            self.isOpen = False
            print(blue_bold("You close the " + self.name.lower() + "."))
        else:
            print(red_bold("That is already closed"))

    def random_drop(self):  # only for weirdBag
        if self.isOpen:
            for items in self.inventory:
                current_node.items.append(items)
                self.inventory.pop(self.inventory.index(items))
                break
        else:
            pass


class Box(Container):
    def __init__(self, name, desc):
        super(Box, self).__init__(name, desc, 4)

    def put_item_in(self, item_name):
        if self.inventory.len() == capacity:
            print(red_bold("This inventory is full."))
        else:
            self.inventory.append(item_name)
            print(cyan_bold("You put the %s in the box") % item_name.lower())

    def wear(self):
        global head
        head = self


class Ball(Item):
    def __init__(self, name, desc):
        super(Ball, self).__init__(name, desc)

    def throw(self):
        inventory.pop(inventory.index(ball))
        print("You throw the ball and in a blink "
              "of an eye, one of the dogs zoom in "
              "a blink of an eye and catch the ball.")
        time.sleep(4)
        print(yellow_bold("The dog then hovers and starts floating to orbit."))
        time.sleep(3)
        print(yellow_bold("The dog comes back with a bucket with even more balls."))
        time.sleep(1)
        current_node.items.append(ball)


class Wearable(Item):
    def __init__(self, name, desc, body):
        super(Wearable, self).__init__(name, desc)
        self.body = body

    def equip(self):
        if self.body is not None:
            print(red_bold("You're already wearing something."))
        else:
            self.body = self
            inventory.pop(inventory.index(self))
            print(blue_bold("You wear the " + self.name))

    def unequip(self):
        if self.body is None:
            print(red_bold("You aren't wearing anything."))
        else:
            self.body = None
            print(blue_bold("You take off the " + self.name))
            inventory.append(self)


class Mask(Wearable):
    def __init__(self, name, desc):
        super(Mask, self).__init__(name, desc, head)

    def equip(self):
        global head
        if head is not None:
            print(red_bold("You're already wearing something."))
        else:
            head = self
            inventory.pop(inventory.index(self))
            print(blue_bold("You wear the " + self.name.lower() + "."))

    def unequip(self):
        global head
        if head is None:
            print(red_bold("You aren't wearing anything."))
        else:
            head = None
            print(blue_bold("You take off the " + self.name.lower() + "."))
            inventory.append(self)


class Shirt(Wearable):
    def __init__(self, name, desc):
        super(Shirt, self).__init__(name, desc, chest)

    def equip(self):
        global chest
        if chest is not None:
            print(red_bold("You're already wearing something."))
        else:
            chest = self
            inventory.pop(inventory.index(self))
            print(blue_bold("You wear the " + self.name.lower() + "."))

    def unequip(self):
        global chest
        if chest is None:
            print(red_bold("You aren't wearing anything."))
        else:
            print(blue_bold("You take off the " + self.name.lower() + "."))
            chest = None
            inventory.append(self)


class Book(Item):
    def __init__(self, name, desc, read_text):
        super(Book, self).__init__(name, desc)
        self.readText = read_text

    def read(self):
        print(self.read_text)


# Characters and Items

Cookie = Character("Cookiezi", "This person seems to be sitting behind a desk with a computer mashing his keyboard\n"
                               "slightly, but you could definitely hear it. On his monitor, he seems to be clicking "
                               "circles...", None, None, None)
jeff = Character("jeff", "he's sitting on a chair playing a game on the left side of the room", "stop", ['pen'], 50)

cookie = Food("Cookie", "A chocolate chip cookie. Seems delicious.")
bed = Bed("Bed", "Your average-looking bed.")
ball = Ball("Ball", "A regular, old tennis ball.")
techRoomKey = Item("Key", "The key has a message engraved that says 'Tech Room Key'...")
backwardsGun = BackwardsGun("Gun", "It's a gun, but its barrel is pointing the opposite way.")
water = Drink("Water Bottle", "A water bottle that has an off-center label that says 'Fiji'.")
cookieMask = Mask("Mask", "A mask of a smiling man wearing glasses with slits in the eyes. "
                          "Wonder what you'd use it for.")
shirt = Shirt("Shirt", "Just a plain white shirt.")
weirdBag = Container("Backpack", "Just a regular backpack.", 4)
mechKeyboard = Item("HyperX Alloy FPS Mech Keyboard", "A mechanical keyboard with red CherryMX switches.")
drawTablet = Item("Huion Graphics Tablet", "A drawing tablet for drawing on computer software.")

# Rooms

BEDROOM = Room("Bedroom",
               "You are in a bedroom full of anime posters, figures, etc."
               "\nYou have a computer sitting on a desk to your north, and a door to the east.",
               "COMPUTER", None, "HALLWAY", None, None, None, None, [bed, shirt])
COMPUTER = Room("Computer",
                "On the desk lies a computer with a crappy membrane keyboard and a mouse. "
                "On the computer lies a weird game called 'osu!'...",
                None, "BEDROOM", "HALLWAY", None, None, None, None, [weirdBag, cookieMask])
HALLWAY = Room("Hallway",
               "The hallway has a few paintings with a dull red carpet on the wooden floor."
               "\nThere are stairs leading down to the south, as well as another room across yours.",
               "DINING_ROOM", "EMPTY_ROOM", "BATHROOM", "BEDROOM", None, "DINING_ROOM", None, [])
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
               None, "LAUNDRY_ROOM", "KITCHEN2", None, None, None, None, [])
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

print("\n" + "When using the put or take out command, make sure the syntax is:"
      + green_bold("\nput/take out <item1 name> in/from <item2 name>")
      + "\nEx: put mask in backpack\n\ttake out mask from backpack\nDon't add any extra words!" + "\n")

while True:
    if health == 0:
        print(red_bold("you died"))
        break
    print(red_bold("Health: ") + str(health))
    if current_node_hasChanged:
        current_node.print_descriptions()
        current_node_hasChanged = False
        if current_node.character is not None \
                and current_node.character.isAlive:
            current_node.character.print_descriptions()

        if weirdBag in inventory:
            if not weirdBag.inventory:
                pass
            else:
                weirdBag.random_drop()

    command = input('>').lower()
    if command == 'quit':
        quit(0)
    elif 'jump' in command:
        current_node.jump()
    elif 'inv' in command or 'inventory' in command:
        if not inventory:
            print(red_bold("You don't have anything in your inventory."))
        else:
            print("Your inventory:")
            for item in inventory:
                if issubclass(type(item), Container):
                    if item.isOpen:
                        print("\t" + bold_text(item.name.lower() + " (Opened)"))
                    else:
                        print("\t" + bold_text(item.name.lower() + " (Closed)"))
                else:
                    print("\t" + bold_text(item.name.lower()))
    elif 'armor' in command:
        if head is None and chest is None and legs is None and feet is None:
            print(red_bold("You're wearing nothing."))
        else:
            print("You are wearing:")
            if head is not None:
                print("\t" + "Head: " + head.name)
            if chest is not None:
                print("\t" + "Chest: " + chest.name)
            if legs is not None:
                print("\t" + "Legs: " + legs.name)
            if feet is not None:
                print("\t" + "Feet: " + feet.name)
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
        pos = dir2.index(command)
        command = dir1[pos]
        try:
            current_node.move(command)
            current_node_hasChanged = True
        except KeyError:
            print(red_bold("You can't go that way."))
            current_node_hasChanged = False
    elif command in dir1:
        try:
            current_node.move(command.lower())
            current_node_hasChanged = True
        except KeyError:
            print(red_bold("You can't go that way."))
            current_node_hasChanged = False
    elif 'wear' in command:
        if not inventory:
            print(red_bold("You don't have anything in your inventory."))
        else:
            if command.strip() == 'wear':
                wear_command = input("What do you want to wear?\n>").lower()
                for i, item in enumerate(inventory):
                    if wear_command == item.name.lower():
                        if issubclass(type(item), Wearable) or isinstance(item, Bed):
                            item.equip()
                            break
                        else:
                            print(red_bold("You can't wear that."))
                            break
                    elif 'nothing' in wear_command or 'nevermind' in wear_command or 'nvm' in wear_command:
                        print("ok")
                        break
                    else:
                        if i != len(inventory) - 1:
                            pass
                        else:
                            print(red_bold("You don't have that in your inventory."))
            else:
                for i, item in enumerate(inventory):
                    if item.name.lower() in command:
                        if issubclass(type(item), Wearable) or isinstance(item, Bed):
                            item.equip()
                            break
                        else:
                            print(red_bold("You can't wear that."))
                            break
                    else:
                        if i != len(inventory) - 1:
                            pass
                        else:
                            print(red_bold("You don't have that in your inventory."))
    elif 'put' in command:
        if not inventory:
            print(red_bold("You don't have anything in your inventory."))
        else:
            try:
                splitCommand = command.split()
                item1 = None
                item2 = None
                for i, item in enumerate(inventory):
                    if item.name.lower() == splitCommand[1]:
                        item1 = item
                    if item.name.lower() == splitCommand[3]:
                        item2 = item

                if not issubclass(type(item1), Item) or not issubclass(type(item2), Item):
                    print(red_bold("You don't have those items."))
                elif item1 == item2:
                    print(red_bold("You can't put something in itself."))
                elif item1 is not None and item2 is not None:
                    if isinstance(item2, Container):
                        if item2.isOpen:
                            item2.put_item_in(item1)
                        else:
                            print(red_bold("The container isn't open."))
                    else:
                        print(red_bold("You can't put that in there."))
            except IndexError:
                print(red_bold("You aren't using the correct syntax.")
                      + "\nEx: put mask in backpack\n\ttake out mask from backpack\n\tDon't add any extra words!")
    elif 'take out' in command:
        if not inventory:
            print(red_bold("You don't have anything in your inventory."))
        else:
            try:
                splitCommand = command.split()
                container = None
                for item in inventory:
                    if item.name.lower() == splitCommand[4]:
                        if isinstance(item, Container):
                            container = item
                        else:
                            print(red_bold("You don't have a container."))
                            break
                for i, item in enumerate(container.inventory):
                    if item.name.lower() == splitCommand[2]:
                        container.take_out(item)
                        break
                    else:
                        print(red_bold("That item is not in the container."))
            except IndexError:
                print(red_bold("You aren't using the correct syntax.")
                      + "\nEx: put mask in backpack\n\ttake out mask from backpack\n\tDon't add any extra words!")
    elif 'take off' in command or 'unequip' in command:
        if head is None and chest is None and legs is None and feet is None:
            print(red_bold("You aren't wearing anything."))
        else:
            if command.strip() == 'take off' or command.strip() == 'unequip':
                unequip_command = input("What do you want to take off?\n>").lower()
                if head is not None:
                    head.unequip()
                elif chest is not None:
                    chest.unequip()
                elif legs is not None:
                    legs.unequip()
                elif feet is not None:
                    feet.unequip()
                else:
                    print(red_bold("You aren't wearing that."))
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
                else:
                    print(red_bold("You aren't wearing anything."))
    elif 'take' in command or 'pickup' in command.strip():
        if not current_node.items:
            print(red_bold("There is nothing here to take."))
        else:
            if command.strip() == 'take' or command.strip() == 'pickup':
                take_command = input("What do you want to take?\n>").lower().strip()
                for i, item in enumerate(current_node.items):
                    if 'all' in take_command:
                        item.take_all()
                        break
                    elif take_command == item.name.lower():
                        item.take()
                        break
                    elif 'nothing' in take_command or 'nevermind' in take_command or 'nvm' in take_command:
                        print("ok")
                        break
                    else:
                        if len(current_node.items) == 1:
                            print(red_bold("That item isn't here."))
                        else:
                            if i != len(current_node.items) - 1:
                                print(red_bold("That item isn't here."))
            else:
                for i, item in enumerate(current_node.items):
                    if 'all' in command:
                        item.take_all()
                        break
                    elif item.name.lower() in command:
                        item.take()
                        break
                    else:
                        if len(current_node.items) == 1:
                            print(red_bold("That item isn't here."))
                        else:
                            if i != len(current_node.items) - 1:
                                pass
                            else:
                                print(red_bold("That item isn't here."))
    elif 'drop' in command:
        if not inventory:
            print(red_bold("You don't have anything in your inventory."))
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
                            print(red_bold("You don't have that item."))
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
                            print(red_bold("You don't have that item."))
    elif 'throw' in command:
        if not inventory:
            print(red_bold("You don't have anything in your inventory."))
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
                            print(red_bold("You don't have that item."))
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
                            print(red_bold("You don't have that item."))
    elif 'talk' in command:
        if current_node.character is None or not current_node.character.isAlive:
            print(red_bold("There is no one here."))
        elif command.strip() == 'talk':
            talk_command = input("Who do you want to talk to?\n>").lower().strip()
            if talk_command == current_node.character.name:
                if current_node.character.isAlive:
                    current_node.character.talk()
                else:
                    print(red_bold("That person is dead."))
            elif 'noone' in talk_command or 'nevermind' in talk_command or 'nvm' in talk_command:
                print("ok")
            else:
                print(red_bold("That person isn't here."))
        elif current_node.character.name.lower() in command:
            if current_node.character.isAlive:
                current_node.character.talk()
            elif not current_node.character.isAlive:
                print(red_bold("That person is dead."))
            else:
                print(red_bold("That person isn't here."))
        else:
            print(red_bold("That person isn't here."))
    elif 'open door' in command:
        if current_node == LOCKED_DOOR:
            if techRoomKey in inventory:
                current_node = TECH_ROOM
                print(blue_bold("You open the door.\n"))
                current_node_hasChanged = True
            else:
                print(red_bold("You don't have a key."))
        else:
            print(red_bold("There is no locked door to open."))
    elif 'shoot' in command:
        if backwardsGun in inventory:
            if command.strip() == 'shoot':
                backwardsGun_command = input("Who do you want to shoot?\n>").lower()
                if current_node.character is None:
                    if backwardsGun_command == 'self' or backwardsGun_command == 'me':
                        print("huh..... it didn't kill you")
                    else:
                        print(red_bold("That person isn't here."))
                else:
                    if backwardsGun_command == current_node.character.name.lower():
                        backwardsGun.shoot()
                    elif backwardsGun_command == 'self' or backwardsGun_command == 'me':
                        print("huh..... it didn't kill you")
                    else:
                        print(red_bold("That person isn't here."))
            else:
                if current_node.character is None:
                    if 'me' in command or 'self' in command:
                        time.sleep(1)
                        print("huh..... it didn't kill you")
                        time.sleep(.5)
                    else:
                        print(red_bold("That person isn't here."))
                else:
                    if current_node.character.name.lower() in command:
                        backwardsGun.shoot()
                    elif 'me' in command or 'self' in command:
                        time.sleep(1)
                        print("huh..... it didn't kill you")
                        time.sleep(.5)
                    else:
                        print(red_bold("That person isn't here."))
        else:
            print(red_bold("You don't have anything to shoot with."))
    elif 'check' in command or 'look at' in command:
        if not inventory:
            print(red_bold("You don't have anything in your inventory."))
        else:
            if command.strip() == 'check' or command.strip() == 'look at':
                check_command = input("What do you want to check?\n>").lower()
                for i, item in enumerate(inventory):
                    if check_command == item.name.lower():
                        item.print_descriptions()
                        break
                    elif 'nothing' in check_command or 'nevermind' in check_command or 'nvm' in check_command:
                        print("ok")
                        break
                    else:
                        if i != len(inventory) - 1:
                            pass
                        else:
                            print(red_bold("You don't have that item."))
            else:
                for i, item in enumerate(inventory):
                    if item.name.lower() in command:
                        item.print_descriptions()
                        break
                    else:
                        if i != len(inventory) - 1:
                            pass
                        else:
                            print(red_bold("You don't have that item."))
    elif 'drink' in command:
        if not inventory:
            print(red_bold("You don't have anything in your inventory."))
        else:
            for i, item in enumerate(inventory):
                if command.strip() == 'drink':
                    drink_command = input("What do you want to drink?\n>").lower()
                    if drink_command == item.name.lower():
                        if isinstance(item, Drink) or isinstance(item, Bed):
                            item.drink()
                        else:
                            print(red_bold("You can't drink that."))
                    elif 'nothing' in drink_command or 'nevermind' in drink_command or 'nvm' in drink_command:
                        print("ok")
                    else:
                        if i != len(inventory) - 1:
                            pass
                        else:
                            print(red_bold("You can't drink that."))
                        print(red_bold("That's not in your inventory."))
                elif item.name.lower() in command:
                    if isinstance(item, Drink) or isinstance(item, Bed):
                        item.drink()
                    else:
                        print(red_bold("You can't drink that."))
                else:
                    if i != len(inventory) - 1:
                        pass
                    else:
                        print(red_bold("That's not in your inventory."))



    elif 'play' in command:
        if 'computer' in command:
            if current_node == COMPUTER:
                current_node.play()
            else:
                print(red_bold("There's no computer here."))
        elif command.strip() == 'play':
            play_command = input("What do you want to play?\n>").lower().strip()
            if play_command == 'computer':
                if current_node == COMPUTER:
                    current_node.play()
                else:
                    print(red_bold("There's no computer here."))
            elif 'nothing' in play_command or 'nevermind' in play_command or 'nvm' in play_command:
                print("ok")
            else:
                print(red_bold("You can't play that."))



    elif 'kill' in command:
        if command.strip() == 'kill':
            kill_command = input("Who do you want to kill?\n>").lower()
            if kill_command == 'me' or kill_command == 'self':
                time.sleep(2)
                print("ok")
                time.sleep(.5)
                while health != 0:
                    health -= 1
                    print(red_bold("Health: ") + str(health))
                    time.sleep(.01)
                    if health == 0:
                        break
            elif kill_command == current_node.character.name.lower():
                if current_node.character.isAlive:
                    current_node.character.kill()
                else:
                    print(red_bold("That person is dead."))
            else:
                print(red_bold("That person isn't here."))
        elif current_node.character is None:
            print(red_bold("There is no one here."))
        elif current_node.character.name.lower() in command:
            if current_node.character.isAlive:
                current_node.character.kill()
            else:
                print(red_bold("That person is dead."))
        else:
            print(red_bold("That person isn't here."))
    elif 'suicide' in command:
        time.sleep(2)
        print("ok")
        time.sleep(.5)
        while health != 0:
            health -= 1
            print(red_bold("Health: ") + str(health))
            time.sleep(.01)
            if health == 0:
                break
    elif 'open' in command:
        if not inventory:
            print(red_bold("You don't have anything in your inventory to open."))
        else:
            if command.strip() == 'open':
                open_command = input("What do you want to open?\n>").lower()
                for i, item in enumerate(inventory):
                    if open_command == item.name.lower():
                        if isinstance(item, Container):
                            item.open()
                        else:
                            print(red_bold("You can't open that."))
                            break
                    elif 'nothing' in open_command or 'nevermind' in open_command or 'nvm' in open_command:
                        print("ok")
                    else:
                        if i != len(inventory) - 1:
                            pass
                        else:
                            print(red_bold("That is not in your inventory."))
            else:
                for i, item in enumerate(inventory):
                    if item.name.lower() in command:
                        if isinstance(item, Container):
                            item.open()
                            break
                        else:
                            print(red_bold("You can't open that."))
                    else:
                        if i != len(inventory) - 1:
                            pass
                        else:
                            print(red_bold("That is not in your inventory."))
    elif 'close' in command:
        if not inventory:
            print(red_bold("You don't have anything in your inventory to close."))
        else:
            if command.strip() == 'close':
                close_command = input("What do you want to close?\n>").lower()
                for i, item in enumerate(inventory):
                    if close_command == item.name.lower():
                        if isinstance(item, Container):
                            item.close()
                        else:
                            print(red_bold("You can't close that."))
                            break
                    elif 'nothing' in close_command or 'nevermind' in close_command or 'nvm' in close_command:
                        print("ok")
                        break
                    else:
                        if i != len(inventory) - 1:
                            pass
                        else:
                            print(red_bold("That isn't in your inventory."))
            else:
                for i, item in enumerate(inventory):
                    if item.name.lower() in command:
                        if isinstance(item, Container):
                            item.close()
                        else:
                            print(red_bold("You can't open that."))
                            break
                    else:
                        if i != len(inventory) - 1:
                            pass
                        else:
                            print(red_bold("That is not in your inventory."))
    elif 'look in' in command:
        if not inventory:
            print(red_bold("You don't have anything to look in."))
        else:
            if command.strip() == 'look in':
                look_command = input("What do you want to look in?\n>").lower()
                for i, item in enumerate(inventory):
                    if item.name.lower() in look_command:
                        if isinstance(item, Container):
                            if item.isOpen:
                                item.lookin()
                                break
                            else:
                                print(red_bold("The container isn't open."))
                                break
                        else:
                            print(red_bold("You can't look in that."))
                            break
                    elif 'nothing' in look_command or 'nevermind' in look_command or 'nvm' in look_command:
                        print("ok")
                        break
                    else:
                        if i != len(inventory) - 1:
                            pass
                        else:
                            print(red_bold("That isn't in your inventory."))
                            break
            else:
                for i, item in enumerate(inventory):
                    if item.name.lower() in command:
                        if isinstance(item, Container):
                            if item.isOpen:
                                item.lookin()
                                break
                            else:
                                print(red_bold("The container isn't open."))
                                break
                        else:
                            print(red_bold("You can't look in that."))
                    else:
                        if i != len(inventory) - 1:
                            pass
                        else:
                            print(red_bold("That isn't in your inventory."))
    elif 'look' in command or command == 'l':
        current_node.print_descriptions()
        if current_node.character is None or not current_node.character.isAlive:
            continue
        else:
            current_node.character.print_descriptions()
    else:
        print("Command not Recognized")
        current_node_hasChanged = False
