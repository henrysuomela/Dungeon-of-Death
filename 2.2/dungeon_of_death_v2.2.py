import random
import json
import os
from dungeon_layouts import dungeons

script_dir = os.path.dirname(os.path.abspath(__file__))
monster_db_file_path = os.path.join(script_dir, "monster_db.json")


dungeon = random.choice(dungeons)

visited = [[False for _ in row] for row in dungeon]
visited[0][0] = True



player = {
    'health': 100,
    'inventory': {},
    'gold': 0,
    'position': (0, 0),
}


with open(monster_db_file_path, 'r') as file:
    monster_db = json.load(file)


def move_player(direction):
    y, x = player['position']

    if direction == 'w':
        if y > 0:
            player['position'] = (y-1, x)
            return True
        else:
            print('No room in that direction, you run into a wall.')
            return False
    elif direction == 's':
        if y < len(dungeon) - 1:
            player['position'] = (y+1, x)
            return True
        else:
            print('No room in that direction, you run into a wall.')
            return False
    elif direction == 'a':
        if x > 0:
            player['position'] = (y, x-1)
            return True
        else:
            print('No room in that direction, you run into a wall.')
            return False
    elif direction == 'd':
        if x < len(dungeon[0]) - 1:
            player['position'] = (y, x+1)
            return True
        else:
            print('No room in that direction, you run into a wall.')
            return False




def enter_room():
    y, x = player['position']
    room = dungeon[y][x]
    visited[y][x] = True

    if room == 'Dungeon Entrance':
        print('You are at the dungeon entrance and have to delve into the dungeon.')

    elif room == 'Strange Room':
        print('You move into the Strange Room.\n')
        print('It is empty with nothing of note inside, you can have a little breather here.')

    elif room == 'Red Room':
        print('You move into the Red Room.\n')
        print('A horrible demon lunges at you!')
        fight_monster(monster_db['demon'])
        add_to_inventory('Demon horn')

    elif room == 'Compelling Room':
        print('You move into the Compelling Room.\n')
        compelling_choices()

    elif room == 'Ominous Room':
        print('You move into the Ominous Room.\n')
        ominous_encounter()

    elif room == 'Howling Room':
        print('You move into the Howling Room.\n')
        print('A wolf attacks you as its friends howl in unison!')
        fight_monster(monster_db['wolf'])
        add_to_inventory("Wolf's tooth")

    elif room == 'Boney Room':
        print('You move into the Boney Room.\n')
        print('A skeleton with dried flesh hanging off its bones prepares to take a swing at you!')
        fight_monster(monster_db['skeleton'])
        add_to_inventory("Skeleton's skull")

    elif room == 'Room of Webs':
        print('You move into the Room of Webs.\n')
        print("Your spidey senses start tingling just before a massive spider jumps at you!")
        fight_monster(monster_db['massive_spider'])
        add_to_inventory('Spider fang')

    elif room == 'Suspicious Room':
        print('You move into the Suspicious Room.\n')
        trap_encounter()

    elif room == 'Crawling Room':
        print('You move into the Crawling Room.\n')
        print("The walls pulse and skitter — you're not alone in here.")
        fight_monster(monster_db['scarab_swarm'])
        add_to_inventory('Scarab carapace')

    elif room == 'Echoing Room':
        print('You move into the Echoing Room.\n')
        print('A low hum invades your thoughts before the leech shows itself.')
        fight_monster(monster_db['mind_leech'])
        add_to_inventory('Psychic slime')

    elif room == 'Smoldering Room':
        print('You move into the Smoldering Room.\n')
        print('Ash hangs in the air. Something burning is waiting.')
        fight_monster(monster_db['wickerman'])
        add_to_inventory('Charred talisman')

    elif room == 'Watchful Room':
        print('You move into the Watchful Room.\n')
        print("You sense you're being watched — and then the arrows fly.")
        fight_monster(monster_db['revenant_archer'])
        add_to_inventory('Ghostly quiver')

    elif room == 'Sulfurous Room':
        print('You move into the Sulfurous Room.\n')
        print('A wave of heat hits you — the dragonling snarls from the shadows.')
        fight_monster(monster_db['baby_dragon'])
        add_to_inventory('Baby dragon scale')

    elif room == 'Splintered Room':
        print('You move into the Splintered Room.\n')
        print('Broken logs and rotting wood litter the ground. Then you hear the axe.')
        fight_monster(monster_db['corrupted_lumberjack'])
        add_to_inventory('Cursed axe head')

    elif room == 'Whispering Room':
        print('You move into the Whispering Room.\n')
        print('Low chanting echoes around you as the cultist steps forward.')
        fight_monster(monster_db['cult_acolyte'])
        add_to_inventory('Unholy beads')

    elif room == 'Stale Room':
        print('You move into the Stale Room.\n')
        print('The air is dead. Then the corpse moves.')
        fight_monster(monster_db['crawling_corpse'])
        add_to_inventory('Rotten hand')

    elif room == 'Dungeon Exit':
        print('\033[1;35mYou have reached the Dungeon exit.\033[0m\n')
        exit_encounter()



def compelling_choices():
    while True:
        print(f"Current health: \033[1;94m{player['health']}\033[0m")
        potion_choice = input('You find a health potion! Do you wish to drink it? (y/n) ').lower()
        if potion_choice == 'y':
            if player['health'] <= 40:
                player['health'] += 60
            else:
                player['health'] = 100
            print('\nYou drink the potion, spiking your health up by \033[1;94m60\033[0m hitpoints.')
            print(f"Current health: \033[1;94m{player['health']}\033[0m")
            break
        elif potion_choice == 'n':
            print('For reasons unknown, you forego the health potion you found.')
            break
        else:
            print('Invalid choice.\n')

    while True:
        print("\nA soothing magical voice asks you if you'd like \033[1;33m15 gold pieces\033[0m in exchange for \033[1;94m15\033[0m hitpoints. It would like to absorb some life energy from you.")
        gold_choice = input("Do you wish to comply with the voice's request? (y/n) ").lower()
        if gold_choice == 'y':
            player['health'] -= 15
            if player['health'] <= 0:
                print("Current health: \033[1;94m0\033[0m")
                death_sequence()
            player['gold'] += 15
            print('\nYou take \033[1;94m15\033[0m damage and \033[1;33m15 gold pieces\033[0m are added to your pouch.')
            print(f"Current health: \033[1;94m{player['health']}\033[0m")
            break
        elif gold_choice == 'n':
            print("The voice disgruntledly bids you farewell.")
            break
        else:
            print('You must make a choice between yes and no, adventurer!')



def ominous_encounter():
    print('\033[1;36mYou feel an ominous tingling in your bones as you enter the ominous room.\033[0m')
    print("An ominous voice in the walls tells you to choose a number between \033[1;35m1 and 5\033[0m. If you choose wrong you'll take \033[1;94m30\033[0m magical damage.\n")

    while True:
        try:
            choice = int(input('Choose a number between 1 and 5 (1 and 5 included): '))
            if 1 <= choice <= 5:
                break
            else:
                print('You hear the voice telling you to choose between the designated numbers.')
        except ValueError:
            print('The voice booms: that is not a number, foolish dummy! Pick a number between 1 and 5.')

    chance = random.randint(1, 5)
    if chance != choice:
        print("\033[1;32mYou don't take damage this time. The voice tells you to thank your lucky stars.\033[0m")
        print('On your way out you find \033[1;33m5 gold pieces\033[0m.')
        player['gold'] += 5
    else:
        print('The voice laughs maniacally as you take \033[1;94m30\033[0m damage.')
        player['health'] -= 30
        if player['health'] >= 0:
            print(f"Current health: \033[1;94m{player['health']}\033[0m")
        else:
            print("Current health: \033[1;94m0\033[0m")
        if player['health'] <= 0:
            death_sequence()



def trap_encounter():
    print('\033[1;35mYou enter a room with traps on the floor and on the walls.\033[0m')
    print("There's a \033[1;31m50%\033[0m chance you won't take damage tip-toeing through the traps. You can't leave the room before bypassing them.\n")

    while True:
        action = input('Press Enter to venture forward through the traps. ')
        if action == "":
            print('You carefully start making your way through the room.\n')
            break
        else:
            print('Type nothing and press Enter to venture forward.')

    chance = random.randint(1, 2)

    if chance == 1:
        print("\033[1;32mYou skilfully avoid all the traps in the room taking no damage!\033[0m")
        print('You even find \033[1;33m3 gold pieces\033[0m next to some of the traps you avoided!')
        player['gold'] += 3
    if chance == 2:
        print("A trap catches you, dealing \033[1;94m20\033[0m damage!")
        player['health'] -= 20
        if player['health'] >= 0:
            print(f"\nYour remaining health: \033[1;94m{player['health']}\033[0m")
        else:
            print("\nYour remaining health: \033[1;94m0\033[0m")
        if player['health'] <= 0:
            death_sequence()



def fight_monster(monster_template):

    monster = monster_template.copy()
    print(f"You're fighting a \033[1;31m{monster['name']}\033[0m!\n")

    while monster['health'] > 0 and player['health'] > 0:
        action = input('Press Enter to attack.\n')

        if action == "":
            player_damage = random.randint(0, 25)
            monster['health'] -= player_damage
            print(f"You swing your sword and hit the \033[1;31m{monster['name']}\033[0m for \033[1;31m{player_damage}\033[0m damage.")
            if monster['health'] > 0:
                print(f"\033[1;31m{monster['name']}'s\033[0m remaining health: \033[1;31m{monster['health']}\033[0m\n")
            else:
                print(f"\033[1;31m{monster['name']}'s\033[0m remaining health: \033[1;31m0\033[0m\n")
            
            if monster['health'] > 0:
                monster_damage = random.randint(0, monster['max_hit'])
                player['health'] -= monster_damage
                print(f"\033[1;94mThe {monster['name']}\033[0m hits you for \033[1;94m{monster_damage}\033[0m damage.")
                if player['health'] > 0:
                    print(f"Your remaining health: \033[1;94m{player['health']}\033[0m\n")
                else:
                    print('Your remaining health: \033[1;94m0\033[0m')
        else:
            print('Invalid action. Type nothing and press enter to attack.\n')

    if monster['health'] <= 0:
        print(f"\033[1;32mYou defeated the {monster['name']}. You're able to leave the room now. The rest of the monsters in the dungeon quiver in fear.\033[0m")

    if player['health'] <= 0:
        print(f"\n\033[1;94mThe {monster['name']} slaughters you!\033[0m")
        death_sequence()



def add_to_inventory(item):
    if item in player['inventory']:
        player['inventory'][item] += 1
    else:
        player['inventory'][item] = 1


def check_health():
    print(f"Your current health: \033[1;94m{player['health']}\033[0m")

def check_gold():
    print(f"You have \033[1;33m{player['gold']} gold pieces\033[0m.")

def check_inventory():
    print('Your inventory:')
    for item, count in player['inventory'].items():
        if count > 1:
            print(f"\033[1;36m{item}\033[0m x{count}")
        else:
            print(f"\033[1;36m{item}\033[0m")


def show_map():
    for y, row in enumerate(dungeon):
        row_display = []
        for x, room in enumerate(row):
            if (y, x) == tuple(player['position']):
                cell = f"▶ {dungeon[y][x]}"
            elif visited[y][x]:
                cell = room
            else:
                cell = '???'
            row_display.append(f'{cell:<18}')
        print(f'{y + 1:2} | ' + ' | '.join(row_display))
    
    y, x = player['position']



def death_sequence():
    user_input = input('You died. . . .\nPress Enter or type "exit" to quit: ').lower()

    if user_input == "" or user_input == "exit":
        print('Exiting game. Goodbye!')
        exit()
    else:
        print("You can't continue... the dungeon has claimed you.")
        exit()


def exit_encounter():
    print(f"You survived the dungeon all the way to the exit, collecting \033[1;33m{player['gold']} gold pieces\033[0m.")
    print('The items you collected on your journey through the dungeon:\n')
    for item, count in player['inventory'].items():
        if count > 1:
            print(f"\033[1;36m{item}\033[0m x{count}")
        else:
            print(f"\033[1;36m{item}\033[0m")
            
    print('\n\033[1;32mCongratulations! Until next time, adventurer.\033[0m\n')

    user_input = input('Press Enter or type "exit" to exit the game. ')

    if user_input == "" or user_input == "exit":
        print('Exiting game. Goodbye!')
        exit()
    else:
        print("Can't go back to the dungeon this way. You'll have to launch the game again and start at the beginning.")
        exit()




def game_loop():
    print('\033[1;35mWelcome to the Dungeon of Death, adventurer!\033[0m')
    print('You are at the dungeon entrance and have to delve into the dungeon.\n')
    show_map()
    while True:
        command = input('\nEnter command | up(w) / down(s) / right(d) / left(a), health(h) / gold(g) / inventory(i) / map(m), quit |: ').lower()

        if command in ['w', 's', 'a', 'd']:
            moved = move_player(command)
            if moved:
                enter_room()
            print()
            show_map()
        elif command == 'm':
            print()
            show_map()
        elif command == 'h':
            check_health()
        elif command == 'g':
            check_gold()
        elif command == 'i':
            check_inventory()
        elif command == 'quit':
            print('Goodbye, adventurer.')
            break
        else:
            print('Invalid command')



game_loop()
