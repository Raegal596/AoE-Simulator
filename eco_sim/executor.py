from .entities import EntityType, UnitState, ResourceType

class ActionType:
    TRAIN = "TRAIN"
    BUILD = "BUILD"
    GATHER = "GATHER"

class Executor:
    def __init__(self, simulator):
        self.sim = simulator
        self.build_order = [] # List of (ActionType, Target, Param)
        self.current_step = 0

    def load_order(self, order):
        self.build_order = order
        self.current_step = 0

    def update(self):
        if self.current_step >= len(self.build_order):
            return

        action, target, param = self.build_order[self.current_step]

        if action == ActionType.TRAIN:
            # target = Unit Name, param = Building Type (optional logic) or Building ID
            # Simple logic: Find ANY idle building that can train this unit
            # For now, let's assume param is "Town Center" or similar string
            building_type = param
            
            # Find an idle building of this type
            # We need a helper in sim to find idle buildings?
            # Or we iterate here.
            candidates = [
                e for e in self.sim.state.entities 
                if e.entity_type == EntityType.BUILDING 
                and e.name == building_type
                and not e.production_queue
            ]
            
            if candidates:
                building = candidates[0]
                if self.sim.can_afford_unit(target):
                    self.sim.train_unit(building.id, target)
                    print(f"Executing: TRAIN {target}")
                    self.current_step += 1
                else:
                    # Waiting for resources
                    pass
            else:
                 # Waiting for idle building
                 pass

        elif action == ActionType.GATHER:
            # target = "Villager", param = "ResourceName" (e.g. "Berry Bush")
            # Logic: Find an IDLE villager and send to resource
            # Real build orders usually specify "Villager created at pop X goes to Y"
            # Simplified: Whenever we have an idle villager, check if current step is GATHER
            
            # This logic is tricky. Usually "Gather" is a setting for new villagers or re-tasking.
            # Let's assume the step means "Retask 1 idle villager to X"
            
            idle_villagers = [
                u for u in self.sim.state.entities
                if u.entity_type == EntityType.UNIT
                and u.name.startswith("Villager") # heuristic
                and u.state == UnitState.IDLE
            ]
            
            if idle_villagers:
                villager = idle_villagers[0]
                # Find resource node
                res_node = next((r for r in self.sim.state.entities if r.entity_type == EntityType.RESOURCE and r.name == param), None)
                if res_node:
                    villager.state = UnitState.GATHERING
                    villager.target = res_node
                    print(f"Executing: GATHER {param}")
                    self.current_step += 1
