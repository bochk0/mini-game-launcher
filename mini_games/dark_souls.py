HEIGHT = 24
WIDTH = 80

global DEBUG
DEBUG = 0

def open_blue_red_door(player, room, stdscr):
    with open(, 'r') as items:
        items = json.load(items)
        if items["items"]["blue_key"] in player["inventory"]["items"] and items["items"]["red_key"] in player["inventory"]["items"]:
            player["coordinates"][1] += 1
        else:
            write_lines(stdscr, "The door remains firmly locked -- it has a red and blue side,\neach with separate keyholes.", 0)

def sphinx_riddle(player, room, stdscr):
    with open(, 'r') as items:
        items = json.load(items)
        if items["items"]["red_key"] in player["inventory"]["items"]:
            return
        riddle = """\
"I'm green on the inside and noxious too;
I'm caustic to those who approach me and may prove dangerous to you."
"Collect me"
(Press enter to continue)"""
        write_lines(stdscr, riddle, 0.035)
        get_input(stdscr)
        write_lines(stdscr, "A gold snake idol, a bottle with a frog suspended in fluid,\n and a spiked ball lay before you\nChoose one of these objects to present to the sphinx.", 0)
        presented_object = get_input(stdscr)
        if 'snake' in presented_object:
            write_lines(stdscr, "The sphinx' eyes unfocus -- it returns to being completely inanimate.\nThe cage containing the red key opens, allowing you to collect it", 0)
            player["inventory"]["items"].append(items["items"]["red_key"])
        else:
            write_lines(stdscr, "The sphinx' eyes light up with a sharp shade of crimson\n", 0)
            player["coordinates"][0] -= 1

def get_random_paintings(player, room, stdscr):
    with open(, 'r') as items:
        items = json.load(items)
        if items["items"]["painting_0"] in player["inventory"]["items"]:
            return
        paintings_amount = [0, 1, 2, 3, 4, 5]
        for i in range(6):
            rng = random.choice(paintings_amount)
            painting = items["items"][f"painting_{rng}"]
            player["inventory"]["items"].append(painting)
            for line in [f"You collected {items['items'][f'painting_{rng}']['name']}", painting["description"]]:
                write_lines(stdscr, line, 0.025)
                get_input(stdscr)
            del paintings_amount[paintings_amount.index(rng)]

def painting_puzzle(player, room, stdscr):
    items = open(, 'r')
    items = json.load(items)
    paintings_placed = []
    paintings = ["Abyss Depiction", "Cell Diagram", "Plant Painting", "Fish Sketch", "Depiction of Man", "Painting of The End"]
    i = 0
    while i < 6:
        write_lines(stdscr, 'Which painting will you place next?\nEnter "help" to see your options', 0)
        user_input = get_input(stdscr).lower()
        if "help" in user_input:
            for l in range(6):
                rng = random.randint(0, len(paintings) - 1)
                painting = paintings[rng]
                write_lines(stdscr, painting, -1)
                del paintings[rng - 1]
                get_input(stdscr)
            i -= 1
        else:                
            for painting in paintings:
                if user_input == painting.lower():
                    i += 1
                    paintings_placed.append(painting)
                    break
    if paintings_placed == paintings:
        write_lines(stdscr, "The wooden panel falls off the wall, revealing the blue key;\nYou collect the blue key", 0)
        player_items = player["inventory"]["items"]
        player_items.append(items["items"]["blue_key"])
        for i in range(6):
            del player_items[player_items.index(items["items"][f"painting_{i}"])]
    else:
        write_lines(stdscr, "Nothing happened...\nPerhaps you should rethink your approach to this.", 0)
        enemies = {
            "enemies": [ "wolf" ]
        }
        image = open("./images/enemies/wolf.txt", 'r')
        encounter_won = enemy_encounter(stdscr, player, enemies, image.read())
        if encounter_won:
            push_dagger = items["weapons"]["pushdagger"]
            if push_dagger not in player["inventory"]["weapons"]:
                write_lines(stdscr, "You found a push-dagger embedded in the wolf's back", 0)
                player["inventory"]["weapons"].append(push_dagger)
        else:
            game_over(stdscr)
def find_item_holding(item):
    return "[nothing]" if not item else item["name"]


def init_kitchen_puzzle(player):
    items = open(, 'r')
    items = json.load(items)['items']
    try:
        if player['kitchen_puzzle']:
            pass
    except:
        player['kitchen_puzzle'] = {
            "chef_holding": [
                items["jewel_claymore"],
                items["stone_spoon"]
            ],
            "armour_holding": [
                items["pot_lid"],
                None
            ],
            "pot_cover": items["jewel_shield"],
            "meat_embed": None
        }

def kitchen_puzzle_1(player, puzzle, stdscr):
    items = open(, 'r')
    items = json.load(items)["items"]
    init_kitchen_puzzle(player)
    write_lines(stdscr, f"You see a statue.\nIn its left hand is a {find_item_holding(player['kitchen_puzzle'][puzzle][0])}.\nIn its right hand is a {find_item_holding(player['kitchen_puzzle'][puzzle][1])}", 0)
    get_input(stdscr)
    write_lines(stdscr, "Which of these will you take?\nType R for the right hand item\nL for the left hand\nand N for nothing", -1)
    retreived_item = get_input(stdscr).lower()
    if retreived_item.startswith('l') and player['kitchen_puzzle'][puzzle][0]:
        player["inventory"]["items"].append(player['kitchen_puzzle'][puzzle][0])
        write_lines(stdscr, f"Retrieved {player['kitchen_puzzle'][puzzle][0]['name']}", -1)
        player['kitchen_puzzle'][puzzle][0] = None
    elif retreived_item.startswith('r') and player['kitchen_puzzle'][puzzle][1]:
        player["inventory"]["items"].append(player['kitchen_puzzle'][puzzle][1])
        write_lines(stdscr, f"Retrieved {player['kitchen_puzzle'][puzzle][1]['name']}", -1)
        player['kitchen_puzzle'][puzzle][1] = None
    time.sleep(0.5)
    write_lines(stdscr, "Which hand will you place an item in?\nType R for the right hand item\nL for the left hand\nand N for nothing", -1)
    giving_hand = get_input(stdscr).lower()
    dest = 0 if giving_hand.startswith('l') else 1 if giving_hand.startswith('r') else None
    if dest == None or player["kitchen_puzzle"][puzzle][dest]:
        return
    write_lines(stdscr, "Write the exact name of the item you wish to place.", -1)
    giving_item = get_input(stdscr).lower()
    i = 0
    for item in player["inventory"]["items"]:
        if item["name"].lower() == giving_item:
            if item["effect"] == "place":
                player['kitchen_puzzle'][puzzle][dest] = item
                write_lines(stdscr, f"Placed {item['name']}", 0)
                del player["inventory"]["items"][i]
            else:
                write_lines(stdscr, f"Could not place {item['name']}\nItem is not meant to be placed", 0)
            break
        i += 1

def kitchen_puzzle_2(player, puzzle, stdscr):
    items = open(, 'r')
    items = json.load(items)["items"]
    init_kitchen_puzzle(player)
    if player['kitchen_puzzle'][puzzle]:
        write_lines(stdscr, f"Will you remove the {find_item_holding(player['kitchen_puzzle'][puzzle])}?\ny/N", 0)
        answer = get_input(stdscr).lower()
        if answer.startswith('y'):
            write_lines(stdscr, f"Removed {player['kitchen_puzzle'][puzzle]['name']}", 0)
            player["inventory"]["items"].append(player['kitchen_puzzle'][puzzle])
            player['kitchen_puzzle'][puzzle] = None
            get_input(stdscr)
    if player['kitchen_puzzle'][puzzle]:
            return
    write_lines(stdscr, "Will you place any item?\ny/N", 0)
    placing = get_input(stdscr).lower()
    if placing.startswith('y'):
        write_lines(stdscr, "Write the exact name of the item you wish to place.", -1)
        giving_item = get_input(stdscr).lower()
        i = 0
        for item in player["inventory"]["items"]:
            if item["name"].lower() == giving_item:
                if item["effect"] == "place":
                    player['kitchen_puzzle'][puzzle] = item
                    write_lines(stdscr, f"Placed {item['name']}", 0)
                    del player["inventory"]["items"][i]
                else:
                    write_lines(stdscr, f"Could not place {item['name']}\nItem is not meant to be placed", 0)
                break
            i += 1

def finished_kitchen_puzzle(player, stdscr):
    items = open(, 'r')
    items = json.load(items)["items"]
    answers = player['kitchen_puzzle']
    if (items["stone_fork"] in answers["chef_holding"] and items["stone_spoon"] in answers["chef_holding"]) and (items["jewel_shield"] in answers["armour_holding"] and items["jewel_claymore"] in answers["armour_holding"]) and answers["pot_cover"] == items["pot_lid"] and answers["meat_embed"] == items["butcher_cleaver"] and items["helmet_key"] not in player["inventory"]["items"]:
        player["inventory"]["items"].append(items["helmet_key"])
        write_lines(stdscr, "A compartment in the direct middle of\nthe food court has opened, revealing the helmet key\nYou pick it up and return.", 0)
        get_input(stdscr)

def chef_statue(player, room, stdscr):
    kitchen_puzzle_1(player, "chef_holding", stdscr)
    finished_kitchen_puzzle(player, stdscr)

def knight_armour(player, room, stdscr):
    kitchen_puzzle_1(player, "armour_holding", stdscr)
    finished_kitchen_puzzle(player, stdscr)

def kitchen_pot(player, room, stdscr):
    kitchen_puzzle_2(player, "pot_cover", stdscr)
    finished_kitchen_puzzle(player, stdscr)

def slab_of_meat(player, room, stdscr):
    kitchen_puzzle_2(player, "meat_embed", stdscr)
    finished_kitchen_puzzle(player, stdscr)

def warden_gate(player, room, stdscr):
    with open(, 'r') as items:
        items = json.load(items)
        if items["items"]["rope_key"] in player["inventory"]["items"] and items["items"]["helmet_key"] in player["inventory"]["items"]:
            player["coordinates"][1] += 1
        else:
            write_lines(stdscr, "The door remains firmly locked.\nOne of its keyholes has a rope insignia on it.\nThe other has a helmet insignia.", 0)

def guillotine_riddle(player, room, stdscr):
    
    write_lines(stdscr, 'A guillotine stands before you.\nA sign on it states "Bring forth the head of justice".\nAround you are several skeletons -- shackled and bound.', 0)
    get_input(stdscr)
    write_lines(stdscr, 'The first one has an iron helmet\nand a sign hung around his neck that has the following inscribed\n"Sir Sampson of Camelot - Charged with Desertion"', 0)
    get_input(stdscr)
    write_lines(stdscr, 'The skeleton beside is adorned with regal robes and a golden crown.\nHung around his neck is a sign that says\n"King Xavier III - Charged with Tyranny"', 0)
    get_input(stdscr)
    write_lines(stdscr, 'Another skeleton has a rogues cloak on.\nThe sign hung around his neck says\n"Roa - Charged with Vigilantism"', 0)
    get_input(stdscr)
    write_lines(stdscr, "Write out the name of the 'prisoner' to present to the guillotine.", 0)
    name = get_input(stdscr).lower()
    if name == 'roa':
        player["coordinates"][1] += 1
        write_lines(stdscr, "A bright flash of light is emitted by the guillotine\nYou find yourself in another room...", 0)
    elif name == player["name"]:
        return
        
    else:
        write_lines(stdscr, "You place the skeleton on the guillotine.\nJust when you begin to pull down on the lever, in a split-second\nyou find yourself in the skeletons place.", 0)
        get_input(stdscr)
        game_over(stdscr)
