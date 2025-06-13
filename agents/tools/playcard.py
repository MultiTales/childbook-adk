import random

CHARACTERS = [
    "A curious explorer",
    "A wise old wizard",
    "A mischievous robot",
    "A shy artist",
    "A brave firefighter",
    "A lost princess",
    "A talking cat",
    "A young inventor",
    "A mysterious detective",
    "A cheerful baker",
    "A sleepy giant",
    "A determined athlete",
    "A lonely astronaut",
    "An adventurous pirate",
    "A shy ghost",
    "A clever fox",
]

SETTINGS = [
    "A hidden cave",
    "A bustling city at night",
    "A magical forest",
    "A deserted island",
    "A space station",
    "A cozy library",
    "A misty mountain peak",
    "A haunted castle",
    "A sunny beach",
    "A secret laboratory",
    "A crowded market",
    "A quiet village",
    "A deep ocean trench",
    "A futuristic city",
    "A dark underground tunnel",
    "A floating sky island",
]

OBJECTS = [
    "A golden key",
    "A mysterious map",
    "A glowing crystal",
    "A broken watch",
    "A talking mirror",
    "A magical flute",
    "A locked treasure chest",
    "A mysterious letter",
    "A floating lantern",
    "A dusty old book",
    "A pair of enchanted boots",
    "A pot of glowing paint",
    "A flying carpet",
    "A strange device",
    "A silver locket",
    "A magical seed",
]

EVENTS = [
    "A sudden storm",
    "A secret is discovered",
    "A race against time",
    "Someone goes missing",
    "A strange noise in the night",
    "A new friendship begins",
    "A mysterious message arrives",
    "A spell is cast",
    "A treasure is found",
    "A disguise is revealed",
    "A journey begins",
    "A competition is held",
    "A door is unlocked",
    "A strange creature appears",
    "A mystery is solved",
    "A party is interrupted",
]

def draw_playcard():
    """
    Draw one playcard from each category.
    """
    return {
        "character": random.choice(CHARACTERS),
        "setting": random.choice(SETTINGS),
        "object": random.choice(OBJECTS),
        "event": random.choice(EVENTS),
    }
