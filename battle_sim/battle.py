import random
from .combatant import Combatant

class Battle:
    def __init__(self):
        self.team_a = []
        self.team_b = []
        self.time = 0.0
        
    def add_unit(self, team, unit_name, unit_data):
        c = Combatant(unit_name, unit_data)
        if team == 'A':
            self.team_a.append(c)
        else:
            self.team_b.append(c)
            
    def run(self, dt=0.1, max_time=1000):
        while self.time < max_time and self.team_a and self.team_b:
            self.time += dt
            
            # Process Team A attacks
            self._process_team_attacks(self.team_a, self.team_b, dt)
            
            # Process Team B attacks
            self._process_team_attacks(self.team_b, self.team_a, dt)
            
            # Remove dead
            self.team_a = [u for u in self.team_a if u.alive]
            self.team_b = [u for u in self.team_b if u.alive]
            
        return {
            'winner': 'A' if self.team_a else ('B' if self.team_b else 'Draw'),
            'time': self.time,
            'survivors_a': len(self.team_a),
            'survivors_b': len(self.team_b)
        }
        
    def _process_team_attacks(self, attackers, defenders, dt):
        for unit in attackers:
            if not unit.alive: continue
            
            # Cooldown management
            if unit.cooldown > 0:
                unit.cooldown -= dt
                continue
                
            # Find target (simplest: random alive defender)
            live_defenders = [d for d in defenders if d.alive]
            if not live_defenders:
                break
                
            target = random.choice(live_defenders)
            
            # Attack
            damage = unit.calculate_damage(target)
            target.take_damage(damage)
            
            unit.cooldown = unit.rof
