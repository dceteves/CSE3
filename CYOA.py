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
pcount = 0  
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
                if items == mechKeyboard or items == tablet:
                    print("\t", redbold(items.name))
                else:
                    print("\t", bold(items.name.lower()))

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
            if head == cookieMask and mechKeyboard in current_node.items and tablet in current_node.items:
                print(yellowbold("You played so hard, you died."))
                quit(0)
            elif head == cookieMask or (mechKeyboard in current_node.items and tablet in current_node.items):
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

    def print_descriptions(self):
        print(greenbold(self.name))
        print(self.description)

    def talk(self):
        if self.dialogue is None:
            print(greenbold("This person doesn't seem to say anything."))
        else:
            print("He says...")
            time.sleep(1)
            print(self.dialogue)
            time.sleep(.5)
            self.hasTalked = True

    def kill(self):
        print(redbold("oh woops you killed " + self.name.lower()))
        self.isAlive = False
        if self.inventory:
            enemy_drop()


class Enemy(Character):
    def __init__(self, name, description, inv, hp, atk, w=None):
        super(Enemy, self).__init__(name, description, None, inv, hp)
        self.atk = atk
        self.weapon = w

    def print_descriptions(self):
        print(redbold(self.name))
        print(self.description)

    def attack(self):
        global health
        health -= self.atk
        print("You got attacked by %s." % self.name)


# item classes


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
        elif self == mechKeyboard or self == tablet:
            inventory.append(self)
            current_node.items.pop(current_node.items.index(self))
            print(cyanbold("You take the " + self.name + "."))
        else:
            inventory.append(self)
            current_node.items.pop(current_node.items.index(self))
            print(cyanbold("You take the " + self.name.lower() + "."))

    def drop(self):
        if self == mechKeyboard or self == tablet:
            inventory.remove(self)
            current_node.items.append(self)
            print(cyanbold("You drop the " + self.name + '.'))
        else:
            inventory.remove(self)
            current_node.items.append(self)
            print(cyanbold("You drop the " + self.name.lower() + '.'))


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
            inventory.remove(self)

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
            inventory.remove(self)
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

    def hit(self): char.health -= self.damage

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
            char.health -= damage * 2
        else:
            char.health -= damage


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
        print(yellowbold("Why is this hammer made of rubber?"))
        time.sleep(.5)


class Consumable(Item):
    def __init__(self, name, desc):
        super(Consumable, self).__init__(name, desc)

    def use(self):
        inventory.remove(self)


class Food(Consumable):
    def __init__(self, name, desc):
        super(Food, self).__init__(name, desc)

    def eat(self):
        global health
        inventory.remove(self)
        print(purplebold("yummy"))
        health = 100


class Drink(Consumable):
    def __init__(self, name, desc):
        super(Drink, self).__init__(name, desc)

    def drink(self):
        inventory.remove(self)
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
        inventory.remove(self)
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
        global head, chest, legs, feet
        if self.body == 'h':
            head = self
        elif self.body == 'c':
            chest = self
        elif self.body == 'l':
            legs = self
        elif self.body == 'f':
            feet = self
        inventory.remove(self)
        print(bluebold("You equipped the %s." % self.name.lower()))

    def unequip(self):
        global head, chest, legs, feet
        if self.body == 'h':
            head = None
        elif self.body == 'c':
            chest = None
        elif self.body == 'l':
            legs = None
        elif self.body == 'f':
            feet = None
        inventory.append(self)
        print(bluebold("You took off the %s." % self.name.lower()))


class Mask(Wearable):
    def __init__(self, name, desc):
        super(Mask, self).__init__(name, desc, head)

    def equip(self):
        global head
        if head is not None:
            print(redbold("You're already wearing something."))
        else:
            head = self
            inventory.remove(self)
            print(bluebold("You wear the " + self.name.lower() + "."))

    def unequip(self):
        global head
        if head is None:
            print(redbold("You aren't wearing anything."))
        else:
            head = None
            print(bluebold("You take off the " + self.name.lower() + "."))
            inventory.append(self)


class Book(Item):
    def __init__(self, name, desc, read_text):
        super(Book, self).__init__(name, desc)
        self.readText = read_text

    def read(self):
        print("You open the book and read:")
        time.sleep(1)
        print(self.readText)
        time.sleep(.5)


# function instantiation


def attack():
    global eacn
    global char
    rn = random.randint(0, 6)  # random number
    atk = 1  # default damage (with no weapon)
    if weapon is not None:
        atk = weapon.damage

    if rn % 2 == 0:
        char.health -= atk
        if char.health <= 0:
            print(cyanbold("You killed the %s." % char.name))
            if char.inventory:
                enemy_drop()
            current_node.character = None
            eacn = False
        else:
            print(cyanbold("You attacked the %s." % char.name))
            print((purplebold("%s Health: ") % char.name) + str(char.health))
            char.attack()
    else:
        print(redbold("You missed."))
        char.attack()


def take_all():
    curitm = current_node.items
    if len(curitm) + len(inventory) > invCapacity:
        print(redbold("You won't have any space those items."))
        time.sleep(.5)
        choice = input("Is there an item you don't want to take?\n>").lower()

        if choice == 'no':
            print("ok")
        else:
            _itm = None
            for item in inventory:
                if item.name.lower() in choice:
                    _itm = item

            while len(curitm) != 1:
                for itm in curitm:
                    if itm == _itm:
                        pass
                    else:
                        itm.take()
    else:
        while len(curitm) != 0:
            for itm in curitm:
                itm.take()


def drop_all():
    while len(inventory) != 0:
        for items in inventory:
            items.drop()


def enemy_drop():
    enemy = char
    while len(enemy.inventory) != 0:
        for _itm in enemy.inventory:
            current_node.items.append(_itm)
            enemy.inventory.remove(_itm)
            print(purplebold("The %s dropped %s." % (enemy.name, _itm.name)))


def suicide():
    global health
    time.sleep(2)
    print("ok")
    time.sleep(.5)
    while health != 0:
        health -= 1
        print(redbold("Health: ") + str(health))
        time.sleep(.01)
        if health == 0:
            break


def oof():
    looping_oof = ["oof"]
    print(bold("".join(looping_oof)))
    time.sleep(.5)
    looping_oof.append("oof")


def ping():
    if pcount <= 2:
        print(boldline("pong"))
    elif pcount == 3:
        print(greenbold("don't waste your time doing this"))
    elif pcount == 4:
        print(yellowbold("pls you have more important things other than this"))
    elif pcount == 5:
        print(cyanbold("pls"))
    elif pcount <= 9:
        print(purplebold(random.choice(ping_phrases)))
    elif pcount == 10:
        print(redbold("You typed in ping too much that the game got tired of you and decided to quit"))
        quit(0)


def line():
    ln = '-'
    for n in range(0, 75):
        ln += "-"
    print(ln)


def lookup():
    print("...")
    time.sleep(1)
    print(redbold("You look up and a piece of rock falls on your head."))
    time.sleep(.5)
    print(redbold("You died."))
    quit(0)


# characters and items
cm_desc = "A paper mask of a smiling man wearing glasses with slits in the eyes. Wonder what you'd use it for."

ckie = Food("Cookie", "A chocolate chip cookie. Seems delicious.")
bed = Bed("Bed", "Your average-looking bed.")
ball = Ball("Ball", "A regular, old tennis ball.")
techRoomKey = Item("Key", "The key has a message engraved that says 'Tech Room Key'...")
backwardsGun = BackwardsGun("Gun", "It's a gun, but its barrel is pointing the opposite way.")
water = Drink("Water Bottle", "A water bottle that has an off-center label that says 'Fiji'.")
cookieMask = Mask("Mask", cm_desc)
shirt = Wearable("Shirt", "Just a plain white shirt.", 'h')
weirdBag = Container("Backpack", "Just a regular backpack.", 4)
sword = Sword("Iron Sword", "A normal iron sword.", 10)
hammer = Hammer("Heavy Hammer", "A heavy, 2 foot long hammer with an iron head. Seems lethal.")
silk = Item("Silk", "Authentic spider silk.")
mechKeyboard = Item("HyperX Alloy FPS Keyboard", "A mechanical keyboard with Cherry MX red switches.")
tablet = Item("Huion Graphics Tablet", "A normal graphics tablet. Seems cheap.")
fang = Item("Snake Fang", "Fangs of a snake.")
book = Book("Book", "A brown book. Wonder what it says.", greenbold("if you're reading this it's too late"))
spaghetti = Food("Spaghetti", "Normal, authentic spaghetti.")

c_desc = "This person seems to be sitting behind a desk with a computer, mashing his keyboard" \
         "\nquietly, but you could definitely hear it. On his monitor, he seems to be clicking " \
         "circles..."

Cookie = Character("Cookiezi", c_desc, None, None, None)
jeff = Character("jeff", "he's sitting on a chair playing a game on the left side of the room", "no", [], 50)
spider = Enemy("Spider", "A fairly large spider with a venomous aura coming out of it.", [silk], 10, 3)
snake = Enemy("Snake", "A long slithering snake.", [fang], 20, 5)
guard = Enemy("Guard", "He seems to be protecting the stuff on the table.", [book, spaghetti], 30, 10)


# Rooms
broom_desc = "You are in a bedroom full of anime posters, figures, etc." \
             "\nYou have a computer sitting on a desk to your north, and a door to the east."
compute_desc = "On the desk lies a computer with a crappy membrane keyboard and a mouse." \
               "\nOn the computer lies a weird game called 'osu!'..."
hal_desc = "The hallway has a few paintings with a dull red carpet on the wooden floor." \
            "\nThere are stairs leading down to the south, as well as another room across yours."
eroom_desc = "You enter an empty room, but in the southern-most corner there's a " \
             "\ntable with what seems to be a drawing tablet, as well as a keyboard."
t_desc = "On the table there is a key and empty boxes with labels saying" \
            "\n'HyperX Alloy FPS Mechanical Gaming Keyboard' as well as another\n" \
            "box that says 'Huion Graphics Tablet'..."
bth_desc = "The bathroom is set with two sinks, a bathtub and a toilet."
droom_desc = "The dining room has a table with a fancy green cloth and a basket" \
         "\nfull of fake fruit. The kitchen leads east, and the living room to the west."
k1_desc = "In the kitchen there's a refrigerator and a pantry full of food," \
          "\nas well as a long counter to eat food on. There's more stuff farther south."
k2_desc = "This side of the Kitchen has a flat screen tv mounted to the wall\nwith a smaller table below " \
          "it that holds the cable box, and an old,\nuseless game console. There's what seems to be a " \
          "laundry room to the\nwest as well as a slide door leading outside east."
ldroom_desc = "The Laundry Room has a washing and drying machine, as well as a cabinet."
cab_desc = "Inside the cabinet contains jackets and sweaters. The shelf above it has a" \
           "\nfew boxes put for storage, but there's a paper mask of a man's face here..."  # osu! joke
by1_desc = "The empty backyard had little to no grass, making it look like a desert.\nNot only that, there " \
           "are two dogs that seem to not care about it at all\nand just have fun with the tennis balls around them."
by2_desc = "This side of the backyard has an unused grill and a bench lying\nat the wall of the house. " \
           "And more tennis balls..."
lroom_desc = "The living room has couches set with a large TV.\nThe exit seems to go the south."
door_desc = "You stand at the exit of the house, where lies a bunch of shoes.\nThe door faces west, " \
            "and there's another door to the south."
prch_desc = "You exit the house into the porch, where there are short, dull, plants.\nYou can go more to " \
            "the west to exit the porch and into the driveway."
dwroom_desc = "The drive way has a basketball hoop, but to the west you see a store with a\nsign that says... Walm." \
              "\nYou can go back north into the porch."
walm_desc = "Sorry to keep your hopes up, this store is closed."
troom_desc = "The door you open leads you into room filled with bright looking technology." \
             "\nThe whole room seems to be white-ish. The whole room seems to be some sort of 'man cave'." \
             "\nYou feel so intimidated that you shouldn't touch any of the equipment."


BEDROOM = Room("Bedroom", broom_desc, "COMPUTER", None, "HALLWAY", None, None, None, None, [bed, shirt, sword])
COMPUTER = Room("Computer", compute_desc, None, "BEDROOM", "HALLWAY", None, None, None, None, [weirdBag])
HALLWAY = Room("Hallway", hal_desc, "DININGROOM", "EMPTY_ROOM", "BATHROOM", "BEDROOM", None, "DININGROOM", spider, [])
EMPTY_ROOM = Room("Empty Room", eroom_desc, "HALLWAY", "TABLE", None, None, None, None, jeff, [backwardsGun])
TABLE = Room("Table", t_desc, "EMPTY_ROOM", None, None, None, None, None, guard, [techRoomKey, mechKeyboard, tablet])
BATHROOM = Room("Bathroom", bth_desc, None, None, None, "HALLWAY", None, None, None, [])
DININGROOM = Room("Dining Room", droom_desc, None, "HALLWAY", "KITCHEN1", "LIVING_ROOM", "HALLWAY", None, None, [ckie])
KITCHEN1 = Room("Entrance to Kitchen", k1_desc, "DININGROOM", "KITCHEN2", None, None, None, None, None, [])
KITCHEN2 = Room("End of Kitchen", k2_desc, "KITCHEN1", None, "BACKYARD1", "LAUNDRY_ROOM", None, None, None, [hammer])
LAUNDRY_ROOM = Room("Laundry Room", ldroom_desc, "CABINET", None, "KITCHEN2", None, None, None, None, [water])
CABINET = Room("Inside of Cabinet", cab_desc, None, "LAUNDRY_ROOM", "KITCHEN2", None, None, None, None, [cookieMask])
BACKYARD1 = Room("Backyard", by1_desc, "BACKYARD2", None, None, "KITCHEN2", None, None, None, [ball])
BACKYARD2 = Room("Farther side of the Backyard", by2_desc, None, "BACKYARD1", None, None, None, None, None, [ball])
LIVING_ROOM = Room("Living Room", lroom_desc, None, "DOOR", "DININGROOM", None, None, None, None, [])
DOOR = Room("Door", door_desc, "LIVING_ROOM", "LOCKED_DOOR", None, 'PORCH', None, None, None, [])
LOCKED_DOOR = Room("Locked Door", "This room's door is locked.", "DOOR", None, None, None, None, None, None, [])
PORCH = Room("Porch", prch_desc, None, None, "DOOR", "DRIVEWAY", None, None, None, [])
DRIVEWAY = Room("Driveway", dwroom_desc, "PORCH", None, None, "STORE", None, None, snake, [])
STORE = Room("Walm", walm_desc, None, None, "DRIVEWAY", None, None, None, None, [])

TECH_ROOM = Room("Tech Room", troom_desc, "DOOR", None, None, None, None, None, Cookie, [])

dir1 = ['north', 'south', 'east', 'west', 'up', 'down']
dir2 = ['n', 's', 'e', 'w', 'u', 'd']

current_node = BEDROOM
curchange = True
eacn = False  # enemy at current node

input("Press enter to play:")

while True:
    line()
    
    char = current_node.character

    if health == 0:
        print(redbold("you died"))
        break
    print(redbold("Health: "), str(health))

    if curchange:
        current_node.print_descriptions()
        curchange = False
        if char is not None and char.isAlive:
            if isinstance(char, Enemy):
                print(redbold("You've walked into %s." % char.name.lower()))
                eacn = True
            else:
                char.print_descriptions()

    cmd = input('>').lower()

    if cmd == 'quit':
        quit(0)
    elif cmd == 'help':
        print("-> To move, use the cardinal directions.")
        print("-> If you don't know where you are, type 'l' or 'look'.")
        print("-> For more detail for enemies, type 'enemy' or 'character'.")
    elif 'do it to em' in cmd:
        print("\n", yellowbold(
            "⠀⠀⠀⠀⣠⣦⣤⣀ ⠀⠀⠀⠀⢡⣤⣿⣿ \n"
            "⠀⠀⠀⠀⠠⠜⢾⡟ ⠀⠀⠀⠀⠀⠹⠿⠃⠄ \n"
            "⠀⠀⠈⠀⠉⠉⠑⠀⠀⠠⢈⣆ \n"
            "⠀⠀⣄⠀⠀⠀⠀⠀⢶⣷⠃⢵ \n"
            "⠐⠰⣷⠀⠀⠀⠀⢀⢟⣽⣆⠀⢃ \n"
            "⠰⣾⣶⣤⡼⢳⣦⣤⣴⣾⣿⣿⠞ \n"
            "⠀⠈⠉⠉⠛⠛⠉⠉⠉⠙⠁ \n"
            "⠀⠀⡐⠘⣿⣿⣯⠿⠛⣿⡄ \n"
            "⠀⠀⠁⢀⣄⣄⣠⡥⠔⣻⡇ \n"
            "⠀⠀⠀⠘⣛⣿⣟⣖⢭⣿⡇ \n"
            "⠀⠀⢀⣿⣿⣿⣿⣷⣿⣽⡇ \n"
            "⠀⠀⢸⣿⣿⣿⡇⣿⣿⣿⣇ \n"
            "⠀⠀⠀⢹⣿⣿⡀⠸⣿⣿⡏ \n"
            "⠀⠀⠀⢸⣿⣿⠇⠀⣿⣿⣿ \n"
            "⠀⠀⠀⠈⣿⣿⠀⠀⢸⣿⡿ \n"
            "⠀⠀⠀⠀⣿⣿⠀⠀⢀⣿⡇ \n"
            "⠀⣠⣴⣿⡿⠟⠀⠀⢸⣿⣷ \n"
            "⠀⠉⠉⠁⠀⠀⠀⠀⢸⣿⣿⠁ \n"
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈\n"
        ))
    elif cmd.strip() == 'look up':
        lookup()
    elif 'check' in cmd or 'look at' in cmd:
        if not inventory and weapon is None:
            print(ntii)
        else:
            if cmd.strip() == 'check' or cmd.strip() == 'look at':
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
                    if item.name.lower() in cmd:
                        itm = item

                if itm is None:
                    print(nii)
                else:
                    itm.print_descriptions()
    elif 'inv' in cmd or 'inventory' in cmd:
        if not inventory:
            print(ntii)
        else:
            print("Your inventory:")
            for item in inventory:
                if item == mechKeyboard or item == tablet:
                    print("\t" + purplebold(item.name))
                else:
                    print("\t" + bold(item.name.lower()))
            if bp is None:
                print(purplebold("Capacity: ") + str(invCapacity))
            else:
                print(purplebold("Capacity: "), str(invCapacity), "(", greenbold("+" + str(bp.capacity)), ")")
            print("You have %s spaces left." % (invCapacity - len(inventory)))
    elif 'armor' in cmd:
        if head is None and chest is None and legs is None and feet is None:
            print(redbold("You're wearing nothing."))
        else:
            print("You are wearing:")
            if head is not None:
                print("\tHead: " + bold(head.name.lower()))
            if chest is not None:
                print("\tChest: " + bold(chest.name.lower()))
            if legs is not None:
                print("\tLegs: " + bold(legs.name.lower()))
            if feet is not None:
                print("\tFeet: " + bold(feet.name.lower()))

            if weapon is not None:
                print("\tWeapon: " + bold(weapon.name.lower()))
            if bp is not None:
                print("\tBackpack: " + bold(bp.name.lower()) + " +" + bp.capacity)
    elif 'look' in cmd or cmd == 'l':
        current_node.print_descriptions()
        if char is None or not char.isAlive:
            continue
        else:
            char.print_descriptions()
    elif 'jump' in cmd:
        current_node.jump()
    elif 'yeet' in cmd:
        print(bold('yeet'))
    elif cmd == "oof":
        current_node.oof()
    elif cmd == 'flush':
        current_node.flush()
    elif 'suicide' in cmd:
        suicide()
    elif cmd == 'beep':
        print('boop')
    elif cmd == "ping":
        current_node.ping()
        pcount += 1
    elif cmd in dir2:
        if eacn:
            print(redbold("There's an enemy in the room. You can't leave unless you kill it."))
        else:
            pos = dir2.index(cmd)
            cmd = dir1[pos]
            try:
                current_node.move(cmd)
                curchange = True
            except KeyError:
                print(redbold("You can't go that way."))
                curchange = False
    elif cmd in dir1:
        if eacn:
            print(redbold("There's an enemy in the room. You can't leave unless you kill it."))
        else:
            try:
                current_node.move(cmd.lower())
                curchange = True
            except KeyError:
                print(red("You can't go that way."))
                curchange = False
    elif 'wear' in cmd:
        if not inventory:
            print(ntii)
        else:
            if cmd.strip() == 'wear':
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
                    if item.name.lower() in cmd:
                        itm = item

                if itm is None:
                    print(nii)
                else:
                    if issubclass(type(itm), Wearable) or isinstance(itm, Bed):
                        itm.equip()
                    else:
                        print(redbold("You can't wear that."))
    elif 'take off' in cmd or 'unequip' in cmd:
        if head is None \
                and chest is None and legs is None \
                and feet is None and weapon is None \
                and bp is None:
            print(redbold("You aren't wearing anything."))
        else:
            if cmd.strip() == 'take off' or cmd.strip() == 'unequip':
                unequip_cmd = input("What do you want to take off?\n>").lower()
                try:
                    if head is not None:
                        if head.name.lower() in unequip_cmd:
                            head.unequip()
                    elif chest is not None:
                        if chest.name.lower() in unequip_cmd:
                            chest.unequip()
                    elif legs is not None:
                        if legs.name.lower() in unequip_cmd:
                            legs.unequip()
                    elif feet is not None:
                        if feet.name.lower() in unequip_cmd:
                            feet.unequip()
                    elif weapon is not None:
                        if weapon.name.lower() in unequip_cmd:
                            weapon.unequip()
                    elif bp is not None:
                        if bp.name.lower() in unequip_cmd:
                            bp.unequip()
                    elif unequip_cmd == 'nvm' or unequip_cmd == 'nothing':
                        print('ok')
                except AttributeError:
                    print(redbold("You aren't wearing that."))
            else:
                try:
                    if head is not None:
                        if head.name.lower() in cmd:
                            head.unequip()
                    elif chest is not None:
                        if chest.name.lower() in cmd:
                            chest.unequip()
                    elif legs is not None:
                        if legs.name.lower() in cmd:
                            legs.unequip()
                    elif feet is not None:
                        if feet.name.lower() in cmd:
                            feet.unequip()
                    elif weapon is not None:
                        if weapon.name.lower() in cmd:
                            weapon.unequip()
                    elif bp is not None:
                        if bp.name.lower() in cmd:
                            bp.unequip()
                except AttributeError:
                    print(redbold("You aren't wearing that."))
    elif 'equip' in cmd:
        if not inventory:
            print(ntii)
        else:
            if cmd.strip() == 'equip':
                equip_cmd = input("What do you want to equip?\n>").lower()
                itm = None
                for item in inventory:
                    if item.name.lower() in equip_cmd:
                        itm = item

                if itm is None:
                    print(nii)
                else:
                    if isinstance(itm, Container) \
                            or issubclass(type(itm), Weapon) \
                            or issubclass(type(itm), Wearable) \
                            or isinstance(itm, Bed):
                        itm.equip()
                    else:
                        print(redbold("You can't equip that."))
            else:
                itm = None
                for item in inventory:
                    if item.name.lower() in cmd:
                        itm = item

                if itm is None:
                    print(nii)
                else:
                    if isinstance(itm, Container) \
                            or issubclass(type(itm), Weapon) \
                            or issubclass(type(itm), Wearable) \
                            or isinstance(itm, Bed):
                        itm.equip()
                    else:
                        print(redbold("You can't equip that."))
    elif 'take' in cmd or 'pickup' in cmd.strip():
        if not current_node.items:
            print(redbold("There is nothing here to take."))
        else:
            if cmd.strip() == 'take' or cmd.strip() == 'pickup':
                take_cmd = input("What do you want to take?\n>").lower().strip()
                itm = None
                for item in current_node.items:
                    if item.name.lower() in take_cmd:
                        itm = item

                if 'all' in take_cmd:
                    # if len(current_node.items) <= invCapacity:
                    take_all()
                    # else:
                    #     print(redbold("You don't have any more space."))
                elif 'nothing' in take_cmd or 'nevermind' in take_cmd or 'nvm' in take_cmd:
                    print("ok")
                elif itm is None:
                    print(nii)
                else:
                    itm.take()
            else:
                itm = None
                for item in current_node.items:
                    if item.name.lower() in cmd:
                        itm = item

                if 'all' in cmd:
                    # if len(current_node.items) <= invCapacity:
                    take_all()
                    # else:
                    #     print(redbold("You don't have any more space."))
                elif itm is None:
                    print(nii)
                else:
                    itm.take()
    elif 'drop' in cmd:
        if not inventory:
            print(ntii)
        else:
            if cmd.strip() == 'drop':
                drop_cmd = input("What do you want to drop?\n>").lower()
                itm = None
                for item in inventory:
                    if item.name.lower() in drop_cmd:
                        itm = item
                
                if 'all' in cmd:
                    drop_all()
                elif 'nothing' in drop_cmd or 'nevermind' in drop_cmd or 'nvm' in drop_cmd:
                    print("ok")
                elif itm is None:
                    print(nii)
                else:
                    itm.drop()
            else:
                itm = None
                for item in inventory:
                    if item.name.lower() in cmd:
                        itm = item
                
                if 'all' in cmd:
                    drop_all()
                elif itm is None:
                    print(nii)
                else:
                    itm.drop()
    elif 'throw' in cmd:
        if not inventory:
            print(ntii)
        else:
            if cmd.strip() == 'throw':
                throw_cmd = input("What do you want to throw?\n>").lower()
                itm = None
                for item in inventory:
                    if item.name.lower() in throw_cmd:
                        itm = item
                        
                if 'all' in throw_cmd:
                    drop_all()
                elif 'nothing' in throw_cmd or 'nevermind' in throw_cmd or 'nvm' in throw_cmd:
                    print("ok")
                elif itm is None:
                    print(nii)
                else:
                    if isinstance(itm, Ball):
                        itm.throw()
                    else:
                        itm.drop()
            else:
                itm = None
                for item in inventory:
                    if item.name.lower() in cmd:
                        itm = item
                        
                if 'all' in cmd:
                    drop_all()
                else:
                    if isinstance(itm, Ball):
                        itm.throw()
                    else:
                        itm.drop()         
    elif 'talk' in cmd:
        if char is None or not char.isAlive:
            print(redbold("There is no one here."))
        else:
            if cmd == 'talk':
                talk_cmd = input("Who do you want to talk to?\n>").lower().strip()
                if talk_cmd == char.name.lower():
                    if char.isAlive:
                        char.talk()
                    else:
                        print(redbold("That person is dead."))
                elif 'no one' in talk_cmd or 'nevermind' in talk_cmd or 'nvm' in talk_cmd:
                    print("ok")
                else:
                    print(redbold("That person isn't here."))
            else:
                if char.name.lower() in cmd:
                    if char.isAlive:
                        char.talk()
                    else:
                        print(redbold("That person is dead."))
                else:
                    print(redbold("That person isn't here."))
    elif 'open door' in cmd:
        if current_node == LOCKED_DOOR:
            if techRoomKey in inventory:
                current_node = TECH_ROOM
                print(bluebold("You open the door.\n"))
                curchange = True
            else:
                print(redbold("You don't have a key."))
        else:
            print(redbold("There is no locked door to open."))
    elif 'drink' in cmd:
        if not inventory:
            print(ntii)
        else:
            if cmd == 'drink':
                drink_cmd = input("What do you want to drink?\n>").lower().strip()
                itm = None
                for item in inventory:
                    if item.name.lower() in drink_cmd:
                        itm = item

                if 'nothing' in drink_cmd or 'nevermind' in drink_cmd or 'nvm' in drink_cmd:
                    print("ok")
                elif itm is None:
                    print(nii)
                else:
                    if isinstance(itm, Drink) or isinstance(itm, Bed):
                        itm.drink()
                    else:
                        print(redbold("You can't drink that."))
            else:
                itm = None
                for item in inventory:
                    if item.name.lower() in cmd:
                        itm = item

                if itm is None:
                    print(nii)
                else:
                    if isinstance(itm, Drink) or isinstance(itm, Bed):
                        itm.drink()
                    else:
                        print(redbold("You can't drink that."))
    elif 'play' in cmd:
        if 'computer' in cmd or 'osu' in cmd:
            current_node.play()
        elif 'myself' in cmd:
            print('are you ok?')
        else:
            if cmd == 'play':
                play_cmd = input("What do you want to play?\n>").lower().strip()
                if play_cmd == 'computer' or play_cmd == 'osu':
                    current_node.play()
                elif play_cmd == 'myself':
                    print('are you ok?')
                elif 'nothing' in take_cmd or 'nevermind' in take_cmd or 'nvm' in take_cmd:
                    print("ok")
            else:
                print(nii)
    elif 'kill' in cmd:
        if cmd == 'kill':
            kill_cmd = input("Who do you want to kill?\n>").lower()
            if kill_cmd == 'me' or kill_cmd == 'self':
                suicide()
            elif kill_cmd == char.name.lower():
                if isinstance(char, Enemy):
                    print(redbold("This character is an enemy. You must use the attack cmd to kill it."))
                else:
                    if char.isAlive:
                        char.kill()
                    else:
                        print(redbold("That person is dead."))
            else:
                print(redbold("That person isn't here."))
        elif char is None:
            print(redbold("There is no one here."))
        elif char.name.lower() in cmd:
            if isinstance(char, Enemy):
                print(redbold("This character is an enemy. You must use the attack cmd to kill it."))
            else:
                if char.isAlive:
                    char.kill()
                else:
                    print(redbold("That person is dead."))
        else:
            print(redbold("That person isn't here."))
    elif 'stats' in cmd:
        if weapon is None and bp is None:
            print(redbold("You don't have a weapon or a backpack."))
        else:
            if weapon is not None:
                weapon.stats()
            if bp is not None:
                bp.stats()
    elif 'attack' in cmd:
        if cmd.strip() == 'attack':
            atk_cmd = input("Who do you want to attack?\n>").lower()
            if char is not None:
                if atk_cmd == char.name.lower():
                    if isinstance(char, Enemy):
                        attack()
                    elif isinstance(char, Character):
                        char.kill()
                    else:
                        print(redbold("That person isn't here."))
                else:
                    print(redbold("That person isn't here."))
            elif 'no one' in atk_cmd.strip() or 'nvm' in atk_cmd.strip() or 'nevermind' in atk_cmd.strip():
                print('ok')
            else:
                if 'self' in atk_cmd or 'myself' in atk_cmd:
                    print('are you ok?')
                else:
                    print(redbold("That person isn't here."))
        else:
            if char is None:
                if 'self' in cmd or 'myself' in cmd:
                    print('are you ok?')
                else:
                    print(redbold("That person isn't here."))
            else:
                if char.name.lower() in cmd:
                    if isinstance(char, Enemy):
                        attack()
                    elif isinstance(char, Character):
                        char.kill()
                else:
                    print(redbold("That person isn't here."))
    elif 'break door' in cmd:
        if not inventory:
            print(ntii)
        else:
            if current_node == LOCKED_DOOR:
                if isinstance(weapon, Hammer):
                    hammer.break_door()
                else:
                    print(redbold("You need a hammer in order to break this door."))
            else:
                print(redbold("There are no doors here to break open."))
    elif 'eat' in cmd:
        if cmd.strip() == 'eat':
            eat_cmd = input("What do you want to eat?\n>").lower()
            itm = None
            for item in inventory:
                if item.name.lower() in eat_cmd:
                    itm = item

            if eat_cmd.strip() == 'nvm' or eat_cmd.strip() == 'nevermind' or eat_cmd.strip() == 'nothing':
                print('ok')
            elif itm is None:
                print(nii)
            elif isinstance(itm, Food):
                itm.eat()
            else:
                print(redbold("You can't eat that."))
        else:
            itm = None
            for item in inventory:
                if item.name.lower() in cmd:
                    itm = item

            if itm is None:
                print(nii)
            elif isinstance(itm, Food):
                itm.eat()
            else:
                print(redbold("You can't eat that."))
    elif 'enemy' in cmd or 'character' in cmd:
        if char is not None:
            char.print_descriptions()
        else:
            print(redbold("There is no one here."))
    elif 'read' in cmd:
        if not inventory:
            print(ntii)
        else:
            if cmd == 'read':
                read_cmd = input("What do you want to read?\n>").lower()
                itm = None
                for item in inventory:
                    if item.name.lower() in read_cmd:
                        itm = item

                if read_cmd.strip() == 'nvm' or read_cmd.strip() == 'nevermind' or read_cmd.strip() == 'nothing':
                    print('ok')
                elif itm is None:
                    print(nii)
                elif isinstance(itm, Book):
                    itm.read()
                else:
                    print(redbold("You can't read that."))
            else:
                itm = None
                for item in inventory:
                    if item.name.lower() in cmd:
                        itm = item

                if itm is None:
                    print(nii)
                elif isinstance(itm, Book):
                    itm.read()
                else:
                    print(redbold("You can't read that."))
