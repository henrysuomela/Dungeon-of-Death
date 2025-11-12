import random

SHOP_ROOMS = ["Mythical Shop", "Tanky Shop"]

HEALING_ROOMS = ["Compelling Room", "Fountain Room"]

FILLER_ROOMS = ["Strange Room", "Echoey Room"]

ENCOUNTER_ROOMS_NON_CB = ["Suspicious Room", "Ominous Room"]

COMBAT_ROOMS = [
    "Room of Webs", "Boney Room", "Smoldering Room", "Red Room",
    "Sulfurous Room", "Splintered Room", "Howling Room", "Crawling Room",
    "Whispering Room", "Parasitic Room", "Watchful Room", "Stale Room"
]


def generate_dungeon(dungeon_levels=25, rooms_per_level=5):
    dungeon = []
    all_rooms = SHOP_ROOMS + HEALING_ROOMS + FILLER_ROOMS + ENCOUNTER_ROOMS_NON_CB + COMBAT_ROOMS

    SPECIAL_ROOM_ODDS = [
        (0.5, HEALING_ROOMS),
        (0.7, FILLER_ROOMS),
        (0.8, ENCOUNTER_ROOMS_NON_CB)
    ]

    # Määritellään kauppa levelit (määrää voi muuttaa)
    shop_level_pool = list(range(0, dungeon_levels - 1, 3)) # Pool on joka kolmas leveli, kauppalevelit väh. 2 levelin päässä toisistaan
    shop_levels = random.sample(shop_level_pool, 6)
    shops_that_appear = {}

    prev_level_rooms = set()

    for level in range(dungeon_levels):
        level_rooms = []
        rooms_used_this_level = set()
        special_room_count = 0

        # Luodaan available rooms ja poistetaan siitä previous level rooms
        available_rooms = all_rooms.copy()
        for room in prev_level_rooms:
            if room in available_rooms:
                available_rooms.remove(room)

        # Ekaan leveliin entrance, vikaan exit
        if level == 0:
            level_rooms.append("Dungeon Entrance")
        elif level == dungeon_levels - 1:
            level_rooms.append("Dungeon Exit")

        # Kauppaleveleihin kauppa
        if level in shop_levels:
            # Pienin count esiintyvien kauppojen dictionaryssä
            if len(shops_that_appear) == len(SHOP_ROOMS):
                min_count = min(shops_that_appear.values())
            else:
                min_count = 0

            # Lista kaupoista jotka esiintyy min_count verran
            candidates = []
            for shop in SHOP_ROOMS:
                count = shops_that_appear.get(shop, 0)
                if count == min_count:
                    candidates.append(shop)
            
            # Valitaan listasta kauppa, lisätään leveliin ja päivitetään count
            shop = random.choice(candidates)
            level_rooms.append(shop)
            if shop in shops_that_appear:
                shops_that_appear[shop] += 1
            else:
                shops_that_appear[shop] = 1
            


        # Arvotaan special roomit leveliin
        for chance, pool in SPECIAL_ROOM_ODDS:
            if random.random() < chance and special_room_count < 3:
                available_in_pool = list(set(pool) & set(available_rooms))
                if available_in_pool:
                    special_room = random.choice(available_in_pool)
                    if special_room not in rooms_used_this_level:
                        level_rooms.append(special_room)
                        rooms_used_this_level.add(special_room)
                        special_room_count += 1

        # Loput huoneet leveliin
        while len(level_rooms) < rooms_per_level:
            remaining_slots = rooms_per_level - len(level_rooms)
            combat_pool = list(set(COMBAT_ROOMS) & set(available_rooms))
            if len(combat_pool) < remaining_slots:
                combat_pool = COMBAT_ROOMS.copy()

            cb_room = random.choice(combat_pool)
            if cb_room not in rooms_used_this_level:
                level_rooms.append(cb_room)
                rooms_used_this_level.add(cb_room)

        prev_level_rooms = set(level_rooms)

        # Shufflaa huoneet
        random.shuffle(level_rooms)

        dungeon.append(level_rooms)

    return dungeon


def find_entrance(dungeon):
    for x, room in enumerate(dungeon[0]):
        if room == "Dungeon Entrance":
            return 0, x
        

def get_adjacent_room_coords(direction, y, x):
    if direction == "w":
        return (y - 1, x)
    elif direction == "s":
        return (y + 1, x)
    elif direction == "a":
        return (y, x - 1)
    elif direction == "d":
        return (y, x + 1)
        

def create_helper_grids(dungeon):
    opposite_directions = {"w": "s", "s": "w", "a": "d", "d": "a"}
    entrance_y, entrance_x = find_entrance(dungeon)

    visited = [[False for _ in row] for row in dungeon]
    visited[entrance_y][entrance_x] = True

    cleared = [[False for _ in row] for row in dungeon]
    cleared[entrance_y][entrance_x] = True

    missing_a_door = [[False for _ in row] for row in dungeon]
    which_doors_missing = [[[] for _ in row] for row in dungeon]

    # Täytetään missing_a_door ja which_doors_missing
    for y, row in enumerate(dungeon):

        x_positions = random.sample(range(len(row)), 1)

        for x in x_positions:
            blocked_direction = random.choice(['w', 'a', 's', 'd'])
            if not missing_a_door[y][x]:
                missing_a_door[y][x] = True
            if blocked_direction not in which_doors_missing[y][x]:
                which_doors_missing[y][x].append(blocked_direction)

            adj_y, adj_x = get_adjacent_room_coords(blocked_direction, y, x)
            if 0 <= adj_y < len(dungeon) and 0 <= adj_x < len(dungeon[0]):
                if opposite_directions[blocked_direction] not in which_doors_missing[adj_y][adj_x]:
                    missing_a_door[adj_y][adj_x] = True
                    which_doors_missing[adj_y][adj_x].append(opposite_directions[blocked_direction])

    # Varmistetaan ettei minkään huoneen kaikki suunnat oo blokattu
    corners = [(0, 0), (0, len(dungeon[0]) - 1), (len(dungeon) - 1, 0), (len(dungeon) - 1, len(dungeon[0]) - 1)]
    for y, row in enumerate(dungeon):
        for x in range(len(row)):
            position = (y, x)
            doors_missing = which_doors_missing[y][x]
            valid_doors = []
            for door in doors_missing:
                adj_y, adj_x = get_adjacent_room_coords(door, y, x)
                if 0 <= adj_y < len(dungeon) and 0 <= adj_x < len(dungeon[0]):
                    valid_doors.append(door)

            if position in corners:
                max_missing = 1
            elif y == 0 or y == len(dungeon) - 1 or x == 0 or x == len(dungeon[0]) - 1:
                max_missing = 2
            else:
                max_missing = 3

            if len(valid_doors) > max_missing:
                unlocked_direction = random.choice(valid_doors)
                which_doors_missing[y][x].remove(unlocked_direction)

                adj_y, adj_x = get_adjacent_room_coords(unlocked_direction, y, x)
                which_doors_missing[adj_y][adj_x].remove(opposite_directions[unlocked_direction])
                if not which_doors_missing[adj_y][adj_x]:
                    missing_a_door[adj_y][adj_x] = False


    return visited, cleared, missing_a_door, which_doors_missing
        

# Dungeonin printtausta generoinnin testaukselle
"""

dungeon = generate_dungeon(25, 5)
visited, cleared, missing_a_door, which_doors_missing = create_helper_grids(dungeon)

for y, row in enumerate(which_doors_missing):
        row_display = []
        for x, room in enumerate(row):
            if not room:
                room = " "
            else:
                room = ", ".join(room)
            row_display.append(f"{room:<18}")
        print(' | ' + ' | '.join(row_display) + ' | ')

print("\n\n")

for y, row in enumerate(dungeon):
        row_display = []
        for x, room in enumerate(row):
            if room in SHOP_ROOMS:
                formatted_cell = f"{room:<18}"
                cell = f"\033[95m{formatted_cell}\033[0m"
            else:
                cell = room
            row_display.append(f"{cell:<18}")
        print(' | ' + ' | '.join(row_display) + ' | ')

"""