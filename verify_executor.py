import json
import os
from eco_sim.simulator import Simulator
from eco_sim.executor import Executor, ActionType
from eco_sim.entities import Building, ResourceType, ResourceNode

def load_data():
    path = os.path.join("data", "units.json")
    with open(path, "r", encoding='utf-8') as f:
        return json.load(f)

def run_test():
    sim = Simulator()
    units_data = load_data()
    sim.load_unit_data(units_data)
    
    # Setup initial state
    tc = Building("Town Center")
    sim.state.add_entity(tc)
    
    berries = ResourceNode("Berry Bush", ResourceType.FOOD, 1000)
    sim.state.add_entity(berries)
    
    # Initial stuff
    sim.state.resources[ResourceType.FOOD] = 50 # Enough for 1 villager
    
    # Spawn a starting villager to do the gathering
    sim._spawn_unit("Villager (Age of Empires)")
    
    # Define Build Order
    # 1. Train Villager
    # 2. Train Villager (will fail initially due to funds, should wait)
    # 3. Gather Berries (retask existing villager)
    
    order = [
         (ActionType.GATHER, None, "Berry Bush"), # Send initial villager to food
         (ActionType.TRAIN, "Villager (Age of Empires)", "Town Center"),
         (ActionType.TRAIN, "Villager (Age of Empires)", "Town Center")
    ]
    
    executor = Executor(sim)
    executor.load_order(order)
    
    print("Starting Execution...")
    for i in range(200): # 200 ticks
        executor.update()
        sim.tick(1.0)
        
        if (i+1) % 50 == 0:
            print(f"Time {sim.state.time}: Food {sim.state.get_resource(ResourceType.FOOD):.1f}, Pop {len([e for e in sim.state.entities if e.entity_type.name == 'UNIT'])}")

if __name__ == "__main__":
    run_test()
