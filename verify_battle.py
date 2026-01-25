import json
import os
from battle_sim.battle import Battle

def load_data():
    path = os.path.join("data", "units.json")
    with open(path, "r", encoding='utf-8') as f:
        return json.load(f)

def get_unit_data(units_data, name):
    for u in units_data:
        if u['name'] == name:
            return u
    return None

data = load_data()
clubman_data = get_unit_data(data, "Clubman")
axeman_data = get_unit_data(data, "Axeman (Age of Empires)")

print("--- Test 1: 1 Clubman vs 1 Clubman (Equal) ---")
battle = Battle()
battle.add_unit('A', "Clubman", clubman_data)
battle.add_unit('B', "Clubman", clubman_data)
res = battle.run()
print(res)

print("\n--- Test 2: 10 Clubmans vs 10 Clubmans (Mass Equal) ---")
battle = Battle()
for _ in range(10):
    battle.add_unit('A', "Clubman", clubman_data)
    battle.add_unit('B', "Clubman", clubman_data)
res = battle.run()
print(res)

print("\n--- Test 3: 5 Clubmans vs 5 Axemans (Axeman wins) ---")
# Axeman has bonus vs Infantry (though not implemented in basic stats yet, raw stats might be higher)
# Checking stats: Clubman 40 HP, 4 Atk, 0 Armor. Axeman 50 HP, 5 Atk, 0 Armor.
# Axeman should win easily.
battle = Battle()
for _ in range(5):
    battle.add_unit('A', "Clubman", clubman_data)
for _ in range(5):
    battle.add_unit('B', "Axeman", axeman_data)
res = battle.run()
print(res)
