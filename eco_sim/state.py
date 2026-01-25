from .entities import ResourceType

class GameState:
    def __init__(self):
        self.time = 0
        self.resources = {
            ResourceType.FOOD: 200, # Standard start
            ResourceType.WOOD: 200,
            ResourceType.GOLD: 0,
            ResourceType.STONE: 150
        }
        self.population = 0
        self.max_population = 5 # Start with Town Center pop space? Actually usually 4 + 4 (houses)
        self.entities = []
        self.tech_tree = set()
        
    def add_entity(self, entity):
        self.entities.append(entity)
        
    def get_resource(self, res_type):
        return self.resources.get(res_type, 0)
        
    def add_resource(self, res_type, amount):
        if res_type in self.resources:
            self.resources[res_type] += amount

    def can_afford(self, costs):
        # costs is dict like {"Food": 50, "Wood": 20}
        # mapped to ResourceType
        pass # Need mapping helper

