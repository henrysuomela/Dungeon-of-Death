import random
import json
import os
from player_state import player

script_dir = os.path.dirname(os.path.abspath(__file__))
shop_items_file_path = os.path.join(script_dir, "shop_items.json")

with open(shop_items_file_path, "r") as file:
    all_shop_items = json.load(file)

def tanky_shop():
    shop_items = all_shop_items['tanky_shop']

    print("\033[1;36mWelcome to the Tanky Shop.\033[0m")
    print("The merchant has three products in stock:")

    for key, item in shop_items.items():
        print(f"{key}. {item['name']} - {item['cost']} monster parts (Protection: \033[1;31m{item['hp']}\033[0m)")

    player_funds = sum(player['inventory'].values())

    print(f"\nYou have \033[1;32m{player_funds} monster parts\033[0m in your bag.")
    print(f"Current armor: \033[1;36m{player['armor']}\033[0m (remaining protection: \033[1;31m{player['armor_hp']}\033[0m)\n")

    while True:
        choice = input("Enter the number of the item you wish to purchase (or press Enter to leave): ")

        if choice == "":
            print("You decide not to buy anything and step away from the shop.")
            break
        elif choice not in shop_items:
            print("Choose the item you want to buy or type nothing and press Enter to leave.\n")
        else:
            item = shop_items[choice]

            if player_funds < item['cost']:
                print("You don't have enough monster parts to buy that item.\n")
                continue

            bill = 0
            while bill < item['cost']:
                monster_part = random.choice(list(player['inventory'].keys()))
                if player['inventory'][monster_part] > 1:
                    player['inventory'][monster_part] -=1
                else:
                    del player['inventory'][monster_part]
                bill += 1

            print(f"\033[1;33mThe merchant picks the {item['cost']} monster parts that call to him from your bag.\033[0m\n")

            player['armor_hp'] = item['hp']
            if player['armor'] == item['name']:
                print(f"You replace your \033[1;36m{player['armor']}\033[0m with a fresh one.")
            else:
                player['armor'] = item['name']
                print(f"You have purchased the \033[1;36m{item['name']}\033[0m!")
            
            print(f"You have \033[1;32m{player_funds - item['cost']} monster parts\033[0m left.")
            break


def mythical_shop():
    shop_items = all_shop_items['mythical_shop']

    print("\033[1;36mWelcome to the Mythical Shop.\033[0m")
    print("The vendor displays three glimmering weapons:")

    for key, item in shop_items.items():
        print(f"{key}. {item['name']} - {item['cost']} coins (Max Hit \033[1;31m{item['max_hit']}\033[0m)")

    print(f"\nYou have \033[1;33m{player['gold']} gold coins.\033[0m")
    print(f"Current weapon: \033[1;36m{player['weapon']}\033[0m (Max Hit: \033[1;31m{player['max_hit']}\033[0m)\n")

    while True:
        choice = input("Enter the number of the weapon you wish to purchase (or press Enter to leave): ")

        if choice == "":
            print("You decide not to buy anything and step away from the shop.")
            break
        elif choice not in shop_items:
            print("Choose the item you want to buy or type nothing and press Enter to leave.\n")
        elif shop_items[choice]['name'] == player['weapon']:
            print("You're already wielding that weapon, the vendor suggests you pick something else!\n")
        else:
            item = shop_items[choice]

            if player['gold'] < item['cost']:
                print("You don't have enough gold to buy that item.\n")
                continue

            player['gold'] -= item['cost']
            player['weapon'] = item['name']
            player['max_hit'] = item['max_hit']

            print(f"\nYou have purchased the \033[1;36m{item['name']}\033[0m!")
            print(f"Your new weapon increases your max hit to \033[1;31m{player['max_hit']}\033[0m.\n")
            print(f"You have \033[1;33m{player['gold']} gold coins\033[0m left.")
            break