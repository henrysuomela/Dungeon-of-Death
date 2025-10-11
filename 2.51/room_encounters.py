import random
import os
import json
from player_state import player

script_dir = os.path.dirname(os.path.abspath(__file__))
monster_db_file_path = os.path.join(script_dir, "monster_db.json")

with open(monster_db_file_path, 'r') as file:
    monster_db = json.load(file)




def fight_monster(monster_template):

    monster = monster_template.copy()
    print(f"You're fighting a \033[1;31m{monster['name']}\033[0m!\n")

    while monster['health'] > 0 and player['health'] > 0:
        action = input('Press Enter to attack.\n')

        if action == "":
            player_damage = random.randint(0, player['max_hit'])
            monster['health'] -= player_damage
            print(f"You swing your weapon and hit the \033[1;31m{monster['name']}\033[0m for \033[1;31m{player_damage}\033[0m damage.")
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

    gold_chance = random.randint(1, 2)
    gold_amount = random.randint(2, 4)

    if monster['health'] <= 0:
        print(f"\033[1;32mYou defeated the {monster['name']}. You're able to leave the room now. The rest of the monsters in the dungeon quiver in fear.\033[0m")
        if gold_chance == 1:
            print(f"You find \033[1;33m{gold_amount} gold coins\033[0m from the {monster['name']}'s dead corpse!")
            player['gold'] += gold_amount

    if player['health'] <= 0:
        print(f"\n\033[1;94mThe {monster['name']} slaughters you!\033[0m")
        death_sequence()




def mythical_shop():
    shop_items = {
        '1': {
            'name': 'Flaming Sword',
            'cost': 30,
            'max_hit_bonus': 20
        },
        '2': {
            'name': 'Icy Blade',
            'cost': 20,
            'max_hit_bonus': 12
        },
        '3': {
            'name': 'Shadow Dagger',
            'cost': 15,
            'max_hit_bonus': 8
        }
    }

    print("\033[1;36mWelcome to the Mythical Shop.\033[0m")
    print("The vendor displays three glimmering weapons:")

    for key, item in shop_items.items():
        print(f"{key}. {item['name']} - {item['cost']} coins (Max Hit \033[1;31m{25 + item['max_hit_bonus']}\033[0m)")

    print(f"\nYou have \033[1;33m{player['gold']} gold coins.\033[0m")
    print(f"Current weapon: \033[1;36m{player['weapon']}\033[0m (Max Hit: \033[1;31m{player['max_hit']}\033[0m)\n")

    while True:
        choice = input("Enter the number of the weapon you wish to purchase (or press Enter to leave): ")

        if choice == '':
            print("You decide not to buy anything and step away from the shop.")
            break
        elif choice not in shop_items:
            print('Choose the item you want to buy or type nothing and press Enter to leave.\n')
        elif shop_items[choice]['name'] == player['weapon']:
            print("You're already wielding that weapon, the vendor suggests you pick something else!\n")
        else:
            item = shop_items[choice]

            if player['gold'] < item['cost']:
                print("You don't have enough gold to buy that item.\n")
                continue

            player['gold'] -= item['cost']
            player['weapon'] = item['name']
            player['max_hit'] = 25 + item['max_hit_bonus']

            print(f"\nYou have purchased the \033[1;36m{item['name']}\033[0m!")
            print(f"Your new weapon increases your max hit to \033[1;31m{player['max_hit']}\033[0m.\n")
            print(f"You have \033[1;33m{player['gold']} gold coins\033[0m left.")
            break




def compelling_choices():
    while True:
        print(f"Current health: \033[1;94m{player['health']}\033[0m")
        potion_choice = input('You find a health potion! Do you wish to drink it? (y/n) ').lower()
        if potion_choice == 'y':
            if player['health'] <= 75:
                player['health'] += 25
            else:
                player['health'] = 100
            print('\nYou drink the potion, spiking your health up by \033[1;94m25\033[0m hitpoints.')
            print(f"Current health: \033[1;94m{player['health']}\033[0m")
            break
        elif potion_choice == 'n':
            print('For reasons unknown, you forego the health potion you found.')
            break
        else:
            print('Invalid choice.\n')

    while True:
        print("\nA soothing magical voice asks you if you'd like \033[1;33m8 gold coins\033[0m in exchange for \033[1;94m30\033[0m hitpoints. It would like to absorb some life energy from you.")
        gold_choice = input("Do you wish to comply with the voice's request? (y/n) ").lower()
        if gold_choice == 'y':
            player['health'] -= 30
            if player['health'] <= 0:
                print("Current health: \033[1;94m0\033[0m")
                death_sequence()
            player['gold'] += 8
            print('\nYou take \033[1;94m30\033[0m damage and \033[1;33m8 gold coins\033[0m are added to your pouch.')
            print(f"Current health: \033[1;94m{player['health']}\033[0m")
            break
        elif gold_choice == 'n':
            print("The voice disgruntledly bids you farewell.")
            break
        else:
            print('You must make a choice between yes and no, adventurer!\n')




def ominous_encounter():
    print("An ominous voice in the walls tells you to choose a number between \033[1;35m1 and 5\033[0m. If you choose wrong you'll take \033[1;94m30\033[0m magical damage.\n")

    while True:
        try:
            choice = int(input('Choose a number between 1 and 5 (1 and 5 included): '))
            if 1 <= choice <= 5:
                break
            else:
                print('You hear the voice telling you to choose between the designated numbers.\n')
        except ValueError:
            print('The voice booms: that is not a number, foolish dummy! Pick a number between 1 and 5.\n')

    chance = random.randint(1, 5)
    if chance != choice:
        print("\033[1;32mYou don't take damage this time. The voice tells you to thank your lucky stars.\033[0m")
        print('On your way out you find \033[1;33m5 gold coins\033[0m.')
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
    print("There's a \033[1;31m50%\033[0m chance you won't take damage tip-toeing through the traps. You can't leave the room before bypassing them.\n")

    while True:
        action = input('Press Enter to venture forward through the traps. ')
        if action == "":
            print('You carefully start making your way through the room.\n')
            break
        else:
            print('Type nothing and press Enter to venture forward.\n')

    chance = random.randint(1, 2)

    if chance == 1:
        print("\033[1;32mYou skilfully avoid all the traps in the room taking no damage!\033[0m")
        print('You even find \033[1;33m3 gold coins\033[0m next to some of the traps you avoided!')
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



def exit_encounter():
    print(f"You survived the dungeon all the way to the exit, collecting \033[1;33m{player['gold']} gold coins\033[0m.")
    print('The items you collected on your journey through the dungeon:\n')
    for item, count in player['inventory'].items():
        if count > 1:
            print(f"\033[1;92m{item}\033[0m x{count}")
        else:
            print(f"\033[1;92m{item}\033[0m")
            
    print('\n\033[1;35mCongratulations! Until next time, adventurer.\033[0m\n')

    user_input = input('Press Enter to exit. ')

    if user_input == "":
        print('Exiting game. Goodbye!')
        exit()
    else:
        print("Can't go back to the dungeon this way. You'll have to launch the game again and start at the beginning.")
        exit()






def death_sequence():
    user_input = input('\nYou died. . . .\nPress Enter to exit: ')

    if user_input == "":
        print('Exiting game. Goodbye!')
        exit()
    else:
        print("You can't continue... the dungeon has claimed you.")
        exit()