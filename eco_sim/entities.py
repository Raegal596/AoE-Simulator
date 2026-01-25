from enum import Enum, auto

class EntityType(Enum):
    UNIT = auto()
    BUILDING = auto()
    RESOURCE = auto()

class Entity:
    _id_counter = 0

    def __init__(self, name, entity_type):
        self.id = Entity._id_counter
        Entity._id_counter += 1
        self.name = name
        self.entity_type = entity_type

class UnitState(Enum):
    IDLE = auto()
    MOVING = auto()
    GATHERING = auto()
    BUILDING = auto()
    ATTACKING = auto()

class Unit(Entity):
    def __init__(self, name, stats=None):
        super().__init__(name, EntityType.UNIT)
        self.state = UnitState.IDLE
        self.stats = stats or {}
        self.target = None
        self.gather_type = None
        self.held_resource = 0
        self.max_carry = 10  # Default, can be upgraded
        self.gather_rate = 0.5 # Default specific to resource usually

class Building(Entity):
    def __init__(self, name, stats=None):
        super().__init__(name, EntityType.BUILDING)
        self.stats = stats or {}
        self.production_queue = [] # List of (UnitName, TimeRemaining)
        self.progress = 0 # Construction progress if being built

class ResourceType(Enum):
    FOOD = auto()
    WOOD = auto()
    GOLD = auto()
    STONE = auto()

class ResourceNode(Entity):
    def __init__(self, name, resource_type, amount):
        super().__init__(name, EntityType.RESOURCE)
        self.resource_type = resource_type
        self.amount = amount

