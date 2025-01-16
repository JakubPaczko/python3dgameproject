import glm
from ecs.component import *

class GameObject:
    def __init__(self, scene = None):
        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)

        self.parent = None
        self.children = []
        self.components : list["Component"] = []
        self.scene = scene

    def get_global_position(self) -> glm.vec3:
        if self.parent:
            return self.position + self.parent.get_global_position()
        return self.position
    
    def get_global_rotation(self) -> glm.vec3:
        if self.parent:
            return self.rotation + self.parent.get_global_rotation()
        return self.rotation

    def get_global_scale(self) -> glm.vec3:
        if self.parent:
            return self.scale + self.parent.get_global_scale()
        return self.scale
    
    def get_component(self, component_type):
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None
    
    def get_component_in_children(self, component_type):
        for child in self.children:
            comonent = child.get_component(component_type)
        return comonent            
        
    def addComponent(self, component) -> None:
        self.components.append(component)
        component.owner = self

    def has_component(self, component_type) -> bool:
        for component in self.components:
            if isinstance(component, component_type):
                return True
        return False
    
    def has_components(self, component_types) -> bool:
        for component in self.components:
            if not type(component) in component_types:
                return False
        return True

    def add_child(self, child_object):
        child_object.parent = self
        self.children.append(child_object)