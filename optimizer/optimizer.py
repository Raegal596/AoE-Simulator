import json
import os
import random
from .genome import Genome
from .fitness import Fitness

class Optimizer:
    def __init__(self, unit_data, population_size=50):
        self.unit_data = unit_data
        self.population_size = population_size
        self.population = [Genome.random(length=10) for _ in range(population_size)]
        self.fitness_evaluator = Fitness(unit_data)
        self.generation = 0

    def run(self, generations, target_check_fn):
        for g in range(generations):
            self.generation = g
            # Evaluate
            scores = []
            for genome in self.population:
                score = self.fitness_evaluator.evaluate(genome, target_check_fn)
                scores.append((score, genome))
            
            # Sort by score descending
            scores.sort(key=lambda x: x[0], reverse=True)
            
            best_score = scores[0][0]
            print(f"Generation {g}: Best Score {best_score:.1f}")
            if g % 10 == 0:
                 print(f"  Best Actions: {scores[0][1].actions}")

            # Elitism: keep top 10%
            elite_count = int(self.population_size * 0.1)
            new_pop = [x[1] for x in scores[:elite_count]]
            
            # Fill rest
            while len(new_pop) < self.population_size:
                parent1 = self._select(scores)
                parent2 = self._select(scores)
                
                child = parent1.crossover(parent2)
                child.mutate()
                new_pop.append(child)
            
            self.population = new_pop
        
        return self.population[0]

    def _select(self, scores):
        # Tournament selection
        candidates = random.sample(scores, 3)
        return max(candidates, key=lambda x: x[0])[1]

if __name__ == "__main__":
    # Test Run
    def load_data():
        path = os.path.join("data", "units.json")
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)

    unit_data = load_data()
    opt = Optimizer(unit_data, population_size=20)
    
    # Target: 5 Villagers (Start with 3, so need 2 more)
    # The start setup in Fitness spawns 3. 
    # Town Center starts with some, but Simulator spawns separate.
    # In run_test/Fitness default, we have 3 villagers. 
    # Let's say target is 5 villagers total.
    def target(sim):
        villagers = [u for u in sim.state.entities if "Villager" in u.name]
        return len(villagers) >= 5
        
    best = opt.run(20, target)
    print("Final Best:", best.actions)
