"""
world_map = {
    'WESTHOUSE': {
        'NAME': 'West of House',
        'DESCRIPTION': 'You are west of a white house.',
        'PATHS': {
            'NORTH': 'NORTHHOUSE',
            'SOUTH': 'SOUTHHOUSE'
        }
    },
    'SOUTHHOUSE': {
        'NAME': 'South of House',
        'DESCRIPTION': 'You are south of a white house.',
        'PATHS': {
            'WEST': 'WESTHOUSE'
        }
    },
}
"""

uso_worldMap = {
    "BEDROOM": {
        "NAME": "Bedroom",
        "DESCRIPTION": "You are in a bedroom full of anime posters, figures, etc."
                       "\nYou have a computer sitting on a desk to your north, and a door to the east.",
        "PATHS": {
            "NORTH": "COMPUTER",
            "WEST": "HALLWAY"
        },
    },
    "COMPUTER": {
        "NAME": "Computer",
        "DESCRIPTION": "On the desk lies a computer with a crappy membrane keyboard and a mouse. "
                       "On the computer lies a weird game called 'osu!'...",
        "PATHS": {
            "EAST": "HALLWAY",
            "SOUTH": "BEDROOM"
        }
    },
    "HALLWAY": {
        "NAME": "Hallway",
        "DESCRIPTION": "The hallway has a few paintings with a dull red carpet on the wooden floor."
                       "\nThere are stairs leading down to the south, as well as another room across yours.",
        "PATHS": {
            "WEST": "BEDROOM",
            "EAST": "BATHROOM",
            "DOWN": "DINING ROOM",
            "SOUTH": "EMPTY ROOM"
        }
    },
    "BATHROOM": {
        "NAME": "Bathroom",
        "DESCRIPTION": "The bathroom is set with two sinks, a bathtub and a toilet. "
                       "There are also toiletries sitting on top of the sink counter.",
        "PATHS": {
            "WEST": "HALLWAY"
        }
    },
    "DINING ROOM": {
        "NAME": "Dining Room",
        "DESCRIPTION": "The dining room has a table with a fancy green cloth and a basket full of fake fruit."
                       "\nThe kitchen leads south east, and the living room to the west.",
        "PATHS": {
            "EAST": "KITCHEN1",
            "WEST": "LIVING ROOM"
        }
    },
    "KITCHEN1": {
        "NAME": "Entrance to Kitchen",
        "DESCRIPTION": "In the kitchen there's a refrigerator and a pantry full of "
                       "food, as well as a long counter to eat food on.\nThere's more stuff farther south.",
        "PATHS": {
            "SOUTH": "KITCHEN2",
            "NORTH": "DINING ROOM"
        }
    },
    "KITCHEN2": {
        "NAME": "Farther Side of Kitchen",
        "DESCRIPTION": "This side of the Kitchen has a flat screen tv mounted to the wall with a smaller table below "
                       "it that holds the cable box, and an old, useless game console.\nThere's what seems to be a "
                       "laundry room to the west as well as a slide door leading outside east.",
        "PATHS": {
            "WEST": "LAUNDRY ROOM",
            "EAST": "BACKYARD1",
            "SOUTH": "LOUNGE ROOM",
            "NORTH": "KITCHEN1"
        }
    },
    "BACKYARD2": {
        "NAME": "Farther side of the Backyard",
        "DESCRIPTION": "This side of the backyard has an unused grill and a bench lying at the wall of the house. And "
                       "more tennis balls...",
        "PATHS": {
            "SOUTH": "BACKYARD1"
        }
    },
    "LAUNDRY ROOM": {
        "NAME": "Laundry Room",
        "DESCRIPTION": "The Laundry Room has a washing and drying machine, as well as a cabinet."
                       "\nThere's a door again to the west.",
        "PATHS": {
            "EAST": "KITCHEN2",
            "NORTH": "CABINET"
        }
    },
    "CABINET": {
        "NAME": "Inside of Cabinet",
        "DESCRIPTION": "Inside the cabinet contains jackets and sweaters. The shelf above it has a few boxes put for "
                       "storage, but there's a paper mask of a man's face with glasses smiling and squinting his "
                       "eyes...",
        "PATHS": {
            "SOUTH": "LAUNDRY ROOM",
            "EAST": "KITCHEN2"
        }
    },
    "BACKYARD1": {
        "NAME": "Backyard",
        "DESCRIPTION": "The empty backyard had little to no grass, making it look like a desert. Not only that, there "
                       "are two dogs that seem to not care about it at all and just have fun with the tennis balls "
                       "around them.",
        "PATHS": {
            "WEST": "KITCHEN2",
            "NORTH": "BACKYARD2"
        }
    },
    "LIVING ROOM": {
        "NAME": "Living Room",
        "DESCRIPTION": "The living room has couches set with a large TV.\nThe exit seems to go the east, as well as a "
                       "door to the south.",
        "PATHS": {
            "EAST": "DINING ROOM",
            "WEST": "DOOR",
            "SOUTH": "LOCKED DOOR"
        }
    },
    "DOOR": {
        "NAME": "Door",
        "DESCRIPTION": "You stand at the exit of the house, where lies a bunch of shoes.\nThe door faces south.",
        "PATHS": {
            "NORTH": "LIVING ROOM",
            "SOUTH": "PORCH"
        }
    },
    "PORCH": {
        "NAME": "Porch",
        "DESCRIPTION": "You exit the house  into the porch, where there are short, dull, plants.\nYou can go south to "
                       "exit the porch and into the driveway.",
        "PATHS": {
            "SOUTH": "DRIVEWAY",
            "NORTH": "DOOR"
        }
    },
    "DRIVEWAY": {
        "NAME": "Driveway",
        "DESCRIPTION": "The drive way has a basketball hoop, but to the south you see a store with a sign that says... "
                       "Walm.",
        "PATHS": {
            "WEST": "PORCH",
            "SOUTH": "STORE"
        }
    },
    "STORE": {
        "NAME": "Walm",
        "DESCRIPTION": "Sorry to keep your hopes up, this store is closed.",
        "PATHS": {
            "NORTH": "DRIVEWAY"
        }
    }
}
current_node = uso_worldMap['BEDROOM']
directions = ['NORTH', 'SOUTH', 'EAST', 'WEST']

while True:
    print(current_node['NAME'])
    print(current_node['DESCRIPTION'])
    command = input('>_')
    if command == 'quit':
        quit(0)
    if command in directions:
        try:
            name_of_node = current_node['PATHS'][command]
            current_node = uso_worldMap[name_of_node]
        except KeyError:
            print("You cannot go this way.")

    else:
        print("Command not Recognized")
