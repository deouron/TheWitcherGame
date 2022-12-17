import sqlite3


def fill_items():
    connect = sqlite3.connect('dbs/data.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute('INSERT INTO items (Cost, CostToSale, ItemType, HP, Mana, Attack, MagicAttack, Armour, '
                   'MagicArmour, ReqLevel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   [10, 5, 'potion', 2, 0, 0, 0, 0, 0, 1])
    connect.commit()  # зелье-здоровье
    cursor.execute('INSERT INTO items (Cost, CostToSale, ItemType, HP, Mana, Attack, MagicAttack, Armour, '
                   'MagicArmour, ReqLevel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   [10, 5, 'potion', 0, 2, 0, 0, 0, 0, 1])
    connect.commit()  # зелье-мана
    cursor.execute('INSERT INTO items (Cost, CostToSale, ItemType, HP, Mana, Attack, MagicAttack, Armour, '
                   'MagicArmour, ReqLevel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   [20, 10, 'armour ', 0, 0, 0, 0, 3, 0, 1])
    connect.commit()  # броня


def give_open_bonus(message):
    connect = sqlite3.connect('dbs/data.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute('INSERT INTO items_links (UserID, ItemID, quantity, IsActive)'
                   'values (?, ?, ?, ?)',
                   [message.chat.id, 1, 1, 1])
    connect.commit()  # бонусное зелье-здоровье
    cursor.execute('INSERT INTO items_links (UserID, ItemID, quantity, IsActive)'
                   'values (?, ?, ?, ?)',
                   [message.chat.id, 2, 1, 1])
    connect.commit()  # бонусное зелье-мана


def fill_locations():
    connect = sqlite3.connect('dbs/data.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute('INSERT INTO locations (LocationName) VALUES (?)', ['Center'])
    connect.commit()
    cursor.execute('INSERT INTO locations (LocationName, XCoord, YCoord) VALUES (?, ?, ?)', ['Novigrad', 0, 2])
    connect.commit()


def fill_location_reachability():
    connect = sqlite3.connect('dbs/data.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute(f'select LocationID, XCoord, YCoord from locations')
    locations = list(cursor.fetchall())
    for i in range(len(locations) - 1):
        for j in range(i + 1, len(locations)):
            distance = ((locations[i][1] - locations[j][1])**2 + (locations[i][2] - locations[j][2])**2)**0.5
            if distance <= 10.01:
                cursor.execute('INSERT INTO locations_links (FirstLocationID, SecondLocationID) VALUES (?, ?)',
                               [locations[i][0], locations[j][0]])
                connect.commit()
                cursor.execute('INSERT INTO locations_links (FirstLocationID, SecondLocationID) VALUES (?, ?)',
                               [locations[j][0], locations[i][0]])
                connect.commit()
            print(distance)