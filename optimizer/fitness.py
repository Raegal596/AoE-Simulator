from eco_sim.simulator import Simulator
from eco_sim.executor import Executor
from eco_sim.entities import Building, ResourceNode, ResourceType, UnitState

class Fitness:
    def __init__(self, unit_data):
        self.unit_data = unit_data

    def evaluate(self, genome, target_check_fn):
        # Setup Simulation
        sim = Simulator()
        sim.load_unit_data(self.unit_data)
        
        # Setup Standard Start (should probably be configurable)
        tc = Building("Town Center")
        sim.state.add_entity(tc)
        
        berries = ResourceNode("Berry Bush", ResourceType.FOOD, 2000)
        sim.state.add_entity(berries)
        
        sim.state.resources[ResourceType.FOOD] = 200
        sim.state.resources[ResourceType.WOOD] = 200
        sim.state.population = 0
        sim.state.max_population = 5 
        
        # Initial Villagers (usually 3)
        for _ in range(3):
            sim._spawn_unit("Villager (Age of Empires)")
            
        executor = Executor(sim)
        executor.load_order(genome.actions)
        
        max_time = 600 # 10 minutes limit
        completed = False
        
        for _ in range(max_time):
            executor.update()
            sim.tick(1.0)
            
            if target_check_fn(sim):
                completed = True
                break
        
        score = 0
        if completed:
            # High score for finishing fast
            score = 10000 - sim.state.time
        else:
            # Partial score based on progress?
            # Ideally we want close to target.
            # For now, just resources gathered + pop count as tie breaker
            score = sim.state.get_resource(ResourceType.FOOD) + (len(sim.state.entities) * 100)
            
        return score
