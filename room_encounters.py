import random
import os
import json
from player_state import player

script_dir = os.path.dirname(os.path.abspath(__file__))
monster_db_file_path = os.path.join(script_dir, "monster_db.json")

with open(monster_db_file_path, "r") as file:
    monster_db = json.load(file)




def fight_monster(monster_template):

    monster = monster_template.copy()
    print(f"You're fighting a \033[1;31m{monster['name'].lower()}\033[0m!\n")

    while monster['health'] > 0 and player['health'] > 0:
        action = input("Press Enter to attack.\n")

        if action == "":
            player_damage = random.randint(0, player['max_hit'])
            monster['health'] -= player_damage
            print(f"You attack and hit the \033[1;31m{monster['name'].lower()}\033[0m for \033[1;31m{player_damage}\033[0m damage.")
            if monster['health'] > 0:
                print(f"\033[1;31m{monster['name']}'s\033[0m remaining health: \033[1;31m{monster['health']}\033[0m\n")
            else:
                print(f"\033[1;31m{monster['name']}'s\033[0m remaining health: \033[1;31m0\033[0m\n")
            
            if monster['health'] > 0:
                armor_destroyed_check = False

                monster_damage = random.randint(0, monster['max_hit'])
                if player['armor_hp'] > 0:
                    if monster_damage >= player['armor_hp']:
                        pure_damage = monster_damage - player['armor_hp']
                        player['armor_hp'] = 0
                        armor_destroyed_check = True
                        player['health'] -= pure_damage
                    else:
                        player['armor_hp'] -= monster_damage
                else:
                    player['health'] -= monster_damage
                print(f"\033[1;94mThe {monster['name'].lower()}\033[0m hits you for \033[1;94m{monster_damage}\033[0m damage.")
                if player['health'] > 0:
                    print(f"Your remaining health: \033[1;94m{player['health']}\033[0m")
                    if player['armor_hp'] > 0:
                        print(f"\033[1;36m{player['armor']}'s\033[0m remaining protection: \033[1;96m{player['armor_hp']}\033[0m\n")
                    elif armor_destroyed_check:
                        print(f"Your \033[1;36m{player['armor'].lower()}\033[0m loses its integrity!\n")
                    else:
                        print()
                else:
                    print("Your remaining health: \033[1;94m0\033[0m")
                    print(f"\n\033[1;94mThe {monster['name'].lower()} slaughters you!\033[0m")
                    death_sequence()
        else:
            print("Invalid action. Type nothing and press enter to attack.\n")


    if monster['health'] <= 0:
        print(f"\033[1;32mYou defeated the {monster['name'].lower()}. You're able to leave the room now. The rest of the monsters in the dungeon quiver in fear.\033[0m")
        gold_chance = random.randint(1, 2)
        gold_amount = random.randint(2, 4)
        if gold_chance == 1:
            print(f"You find \033[1;33m{gold_amount} gold coins\033[0m from the {monster['name'].lower()}'s remains!")
            player['gold'] += gold_amount


def compelling_choices():
    while True:
        print(f"Current health: \033[1;94m{player['health']}\033[0m")
        potion_choice = input("You find a health potion! Do you wish to drink it? (y/n) ").lower()
        if potion_choice == "y":
            health_before_heal = player['health']
            if player['health'] <= 75:
                player['health'] += 25
            else:
                player['health'] = 100
            heal_amount = player['health'] - health_before_heal
            print(f"\nYou drink the potion, spiking your health up by \033[1;94m{heal_amount}\033[0m hitpoints.")
            print(f"Current health: \033[1;94m{player['health']}\033[0m")
            break
        elif potion_choice == "n":
            print("For reasons unknown, you forego the health potion you found.")
            break
        else:
            print("Invalid choice.\n")

    while True:
        print("\nA soothing magical voice asks you if you'd like \033[1;33m8 gold coins\033[0m in exchange for \033[1;94m30\033[0m hitpoints. It would like to absorb some life energy from you.")
        gold_choice = input("Do you wish to comply with the voice's request? (y/n) ").lower()
        if gold_choice == "y":
            player['health'] -= 30
            if player['health'] <= 0:
                print("Current health: \033[1;94m0\033[0m")
                death_sequence()
            player['gold'] += 8
            print("\nYou take \033[1;94m30\033[0m damage and \033[1;33m8 gold coins\033[0m are added to your pouch.")
            print(f"Current health: \033[1;94m{player['health']}\033[0m")
            break
        elif gold_choice == "n":
            print("The voice disgruntledly bids you farewell.")
            break
        else:
            print("You must make a choice between yes and no, adventurer!\n")




def ominous_encounter():
    print("An ominous voice in the walls tells you to choose a number between \033[1;35m1 and 5\033[0m. If you choose wrong you'll take \033[1;94m30\033[0m magical damage.\n")

    while True:
        try:
            choice = int(input("Choose a number between 1 and 5 (1 and 5 included): "))
            if 1 <= choice <= 5:
                break
            else:
                print("You hear the voice telling you to choose between the designated numbers.\n")
        except ValueError:
            print("The voice booms: that is not a number, foolish dummy! Pick a number between 1 and 5.\n")

    chance = random.randint(1, 5)
    if chance != choice:
        print("\033[1;32mYou don't take damage this time. The voice tells you to thank your lucky stars.\033[0m")
        print("On your way out you find \033[1;33m5 gold coins\033[0m.")
        player['gold'] += 5
    else:
        print("The voice laughs maniacally as you take \033[1;94m30\033[0m damage.")
        player['health'] -= 30
        if player['health'] > 0:
            print(f"Current health: \033[1;94m{player['health']}\033[0m")
        else:
            print("Current health: \033[1;94m0\033[0m")
            death_sequence()




def trap_encounter():
    print("\033[1;94mYou spot a switch to disarm the traps, but it's on the other side of the room. You'll have to tip-toe your way over to it.\033[0m")

    while True:
        action = input("Press Enter to venture forward through the traps. ")
        if action == "":
            print("\nYou carefully start making your way through the room.\n")
            break
        else:
            print("\nType nothing and press Enter to venture forward.")

    chance = random.randint(1, 2)

    if chance == 1:
        print("\033[1;32mYou skilfully avoid all the traps in the room and flick the switch to disarm them!\033[0m")
        print("You even find \033[1;33m3 gold coins\033[0m from under a disarmed trap!")
        player['gold'] += 3
    if chance == 2:
        print("A trap catches you, dealing \033[1;94m20\033[0m damage!")
        player['health'] -= 20
        if player['health'] > 0:
            print(f"Your remaining health: \033[1;94m{player['health']}\033[0m")
        else:
            print("Your remaining health: \033[1;94m0\033[0m")
            death_sequence()
        print("\n\033[1;32mYou manage to disarm the rest of the traps, dazed from the damage.\033[0m")


def healing_fountain():
    while True:
        fountain_choice = input("Do you wish to heal yourself here? (y/n) ").lower()
        if fountain_choice == "y":
            print("\n\033[1;36mYou run your fingers through the fountain's healing water and feel its energy flow through you.\033[0m")
            player['health'] = 100
            print(f"Current health: \033[1;94m{player['health']}\033[0m")
            break
        elif fountain_choice == "n":
            print("You ignore the healing powers of the fountain and move on.")
            break
        else:
            print("Invalid choice.\n")


def exit_encounter():
    print("\033[1;35mYou have reached the Dungeon exit.\033[0m\n")
    print(f"You survived the dungeon all the way to the exit, collecting \033[1;33m{player['gold']} gold coins\033[0m.")
    print("The items you collected on your journey through the dungeon:")
    for item, count in player['inventory'].items():
        if count > 1:
            print(f"\033[1;92m{item}\033[0m x{count}")
        else:
            print(f"\033[1;92m{item}\033[0m")
            
    print("\n\033[1;35mCongratulations! Until next time, adventurer.\033[0m\n")

    user_input = input("Press Enter to exit. ")

    if user_input == "":
        print("Exiting game. Goodbye!")
        exit()
    else:
        print("Can't go back to the dungeon this way. You'll have to launch the game again and start at the beginning.")
        exit()






def death_sequence():
    user_input = input("\nYou died. . . .\nPress Enter to exit: ")

    if user_input == "":
        print("Exiting game. Goodbye!")
        exit()
    else:
        print("You can't continue... the dungeon has claimed you.")
        exit()