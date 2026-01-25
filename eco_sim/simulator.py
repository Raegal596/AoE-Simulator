from .state import GameState
from .entities import Unit, Building, UnitState, ResourceType, EntityType

class Simulator:
    def __init__(self):
        self.state = GameState()
        self.unit_data = {} # To hold the scraped data

    def load_unit_data(self, units_list):
        # Convert list of dicts to a dict by name for easy lookup
        for u in units_list:
            self.unit_data[u['name']] = u

    def tick(self, dt=1.0):
        self.state.time += dt
        
        # Update entities
        for entity in self.state.entities:
            if entity.entity_type == EntityType.UNIT:
                self._update_unit(entity, dt)
            elif entity.entity_type == EntityType.BUILDING:
                self._update_building(entity, dt)

    def _update_unit(self, unit, dt):
        if unit.state == UnitState.GATHERING:
            if unit.target and unit.target.entity_type == EntityType.RESOURCE:
                # Gather logic
                # Rate depends on type. Simple heuristic for now.
                # Villager default gather rate is roughly ~0.4-0.5 per sec depending on resource.
                rate = 0.4 
                amount = rate * dt
                
                # Check if node has enough
                if unit.target.amount > 0:
                    taken = min(amount, unit.target.amount)
                    unit.target.amount -= taken
                    unit.held_resource += taken
                    
                    if unit.held_resource >= unit.max_carry:
                        # Drop off resource (instant for now, no walking)
                        self.state.add_resource(unit.target.resource_type, unit.held_resource)
                        unit.held_resource = 0

    def _update_building(self, building, dt):
        if building.production_queue:
            # item is (UnitName, TimeRemaining)
            unit_name, needed_time = building.production_queue[0]
            needed_time -= dt
            
            if needed_time <= 0:
                # Unit complete
                self._spawn_unit(unit_name)
                building.production_queue.pop(0)
            else:
                building.production_queue[0] = (unit_name, needed_time)

    def _spawn_unit(self, unit_name):
        # Look up stats
        stats = self.unit_data.get(unit_name, {}).get('stats', {})
        new_unit = Unit(unit_name, stats=stats)
        self.state.add_entity(new_unit)
        print(f"Time {self.state.time:.1f}: Created {unit_name}")

    def train_unit(self, building_id, unit_name):
        # Find building
        building = next((e for e in self.state.entities if e.id == building_id), None)
        if building and building.entity_type == EntityType.BUILDING:
            # Check costs
            if self._pay_cost(unit_name):
                # Get build time. Scraped data might have "Training time" in a weird format string
                # HEURISTIC: "20 seconds"
                train_time = 20.0 # Default
                # TODO: Parse from scraped data properly
                
                building.production_queue.append((unit_name, train_time))
                print(f"Time {self.state.time:.1f}: Queued {unit_name} at {building.name}")
            else:
                print(f"Time {self.state.time:.1f}: Cannot afford {unit_name}")

    def can_afford_unit(self, unit_name):
        data = self.unit_data.get(unit_name)
        if not data: 
            return False
            
        costs = data.get('costs', {})
        # Map string keys to Enum
        cost_map = {
            "Food": ResourceType.FOOD,
            "Wood": ResourceType.WOOD,
            "Gold": ResourceType.GOLD,
            "Stone": ResourceType.STONE
        }
        
        for res_str, amount in costs.items():
            res_type = cost_map.get(res_str)
            if res_type:
                if self.state.get_resource(res_type) < amount:
                    return False
        return True

    def _pay_cost(self, unit_name):
        if not self.can_afford_unit(unit_name):
            return False
            
        data = self.unit_data.get(unit_name)
        costs = data.get('costs', {})
        cost_map = {
            "Food": ResourceType.FOOD,
            "Wood": ResourceType.WOOD,
            "Gold": ResourceType.GOLD,
            "Stone": ResourceType.STONE
        }
        
        # Deduct
        for res_str, amount in costs.items():
            res_type = cost_map.get(res_str)
            if res_type:
                self.state.add_resource(res_type, -amount)
        
        return True

