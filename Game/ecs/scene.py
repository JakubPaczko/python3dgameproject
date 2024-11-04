from ecs import systems
from ecs.gameObject import GameObject
from typing import List, Dict
import ecs.systems 

class Scene:
    def __init__(self, app):
        self.last_added_id = 0
        self.gameObjects : Dict[int, GameObject] = {}
        self.systems : List[ecs.systems.System] = []
        self.app = app

    def add_system(self, system):
        self.systems.append(system)
    
    def update(self):
        for system in self.systems:
            system.update()
    
    
    def add_entity(self, gameObject : GameObject):
        gameObject.scene = self
        self.gameObjects[self.last_added_id] = gameObject
        self.last_added_id += 1
    
    def filter_enitities_by_component(self, component_type) -> List[GameObject]:
        out : List[GameObject] = []

        for gameObject in self.gameObjects.values():
            if gameObject.has_component(component_type):
                out.append(gameObject)
        
        return out
    
    def filter_enitities_by_components(self, component_types) -> List[GameObject]:
        out : List[GameObject] = []

        for gameObject in self.gameObjects.values():
            if gameObject.has_components(component_types):
                out.append(gameObject)
        
        return out