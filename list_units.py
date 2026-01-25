import json
with open('data/units.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for u in data:
        print(u['name'])
