class Combatant:
    def __init__(self, name, data):
        self.name = name
        self.original_data = data
        
        # Stats
        stats = data.get('stats', {})
        self.hp = int(stats.get('Hit points', 1))
        self.max_hp = self.hp
        
        # Attack
        # Try Melee first, then Pierce
        self.attack = 0
        self.attack_type = 'Melee'
        
        melee_atk = stats.get('Melee attack')
        pierce_atk = stats.get('Pierce attack')
        
        if melee_atk:
             self.attack = int(melee_atk)
             self.attack_type = 'Melee'
        elif pierce_atk:
             self.attack = int(pierce_atk)
             self.attack_type = 'Pierce'
             
        # Armor
        self.melee_armor = int(stats.get('Melee armor', 0))
        self.pierce_armor = int(stats.get('Pierce armor', 0))
        
        # Other
        self.range = float(stats.get('Range', 0))
        
        # ROF (Reload Time) - default to 2.0 if missing (standard-ish)
        rof_str = stats.get('Reload time', '2.0')
        try:
            self.rof = float(rof_str)
        except:
             self.rof = 2.0
             
        self.cooldown = 0.0
        self.alive = True
        
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            
    def calculate_damage(self, target):
        armor = 0
        if self.attack_type == 'Melee':
            armor = target.melee_armor
        else:
            armor = target.pierce_armor
            
        damage = max(1, self.attack - armor)
        return damage
