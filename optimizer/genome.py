import random
from eco_sim.executor import ActionType

class Genome:
    def __init__(self, actions=None):
        self.actions = actions if actions else []

    @classmethod
    def random(cls, length=10):
        # Generate a random sequence.
        # Minimal set of actions for now: Train Villager, Build House.
        # We need valid unit names.
        actions = []
        possible_actions = [
            (ActionType.TRAIN, "Villager (Age of Empires)", "Town Center"),
            # Placeholder for House - we haven't implemented BUILD yet fully in executor but let's add it for structure
            # (ActionType.BUILD, "House", "Villager"), 
             (ActionType.GATHER, None, "Berry Bush")
        ]
        
        for _ in range(length):
            actions.append(random.choice(possible_actions))
        return cls(actions)

    def mutate(self, mutation_rate=0.1):
        if random.random() < mutation_rate:
            # Type of mutation
            mut_type = random.choice(['add', 'remove', 'swap'])
            
            if mut_type == 'add':
                possible_actions = [
                    (ActionType.TRAIN, "Villager (Age of Empires)", "Town Center"),
                    (ActionType.GATHER, None, "Berry Bush")
                ]
                self.actions.insert(random.randint(0, len(self.actions)), random.choice(possible_actions))
            
            elif mut_type == 'remove' and self.actions:
                self.actions.pop(random.randint(0, len(self.actions)-1))
                
            elif mut_type == 'swap' and len(self.actions) > 1:
                i, j = random.sample(range(len(self.actions)), 2)
                self.actions[i], self.actions[j] = self.actions[j], self.actions[i]

    def crossover(self, other):
        # Single point crossover
        if not self.actions or not other.actions:
            return Genome(self.actions[:])
            
        point = random.randint(0, min(len(self.actions), len(other.actions)))
        child_actions = self.actions[:point] + other.actions[point:]
        return Genome(child_actions)
