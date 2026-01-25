import json
import os
from eco_sim.simulator import Simulator
from eco_sim.entities import Building, ResourceType, ResourceNode, UnitState

def load_data():
    path = os.path.join("data", "units.json")
    with open(path, "r", encoding='utf-8') as f:
        return json.load(f)

def run_test():
    sim = Simulator()
    units_data = load_data()
    sim.load_unit_data(units_data)
    
    # Setup initial state
    # 1 Town Center, 3 Villagers
    tc = Building("Town Center")
    sim.state.add_entity(tc)
    
    # Find Berry Bush
    berries = ResourceNode("Berry Bush", ResourceType.FOOD, 150)
    sim.state.add_entity(berries)
    
    # Spawn a villager
    sim._spawn_unit("Villager (Age of Empires)")
    
    # Assign villager to gather
    villager = sim.state.entities[-1] # The one we just spawned
    villager.state = UnitState.GATHERING
    villager.target = berries
    
    print("Starting Simulation...")
    print(f"Initial Food: {sim.state.get_resource(ResourceType.FOOD)}")
    
    # Run for 60 seconds
    for _ in range(60):
        sim.tick(1.0)
        
    print(f"Food after 60s gathering: {sim.state.get_resource(ResourceType.FOOD)}")
    
    # Try to queue a villager
    print("Queueing Villager...")
    sim.train_unit(tc.id, "Villager (Age of Empires)")
    
    # Run for another 30s
    for _ in range(30):
        sim.tick(1.0)
        
    # Check if we have 2 units now (1 initial + 1 trained)
    # Actually we just spawned 1 manually.
    units = [e for e in sim.state.entities if e.entity_type.name == 'UNIT']
    print(f"Total Units: {len(units)}")
    for u in units:
        print(f" - {u.name}")

if __name__ == "__main__":
    run_test()
