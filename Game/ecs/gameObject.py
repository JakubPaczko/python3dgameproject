import glm
from ecs.component import *

class GameObject:
    def __init__(self, scene = None):
        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.quat(0, 0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)

        self.parent = None
        self.children = []
        self.components : list["Component"] = []
        self.scene = scene

    def get_local_transform(self):
        """
        Compute the local transformation matrix of an entity.
        Combines position, rotation (as vec3), and scale into a single matrix.
        """
        m_model = glm.mat4()
        
        m_model = glm.translate(m_model, self.position)

        m_model = glm.rotate(m_model, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        
        # m_model = glm.rotate(m_model, glm.radians(self.rotation))
        m_model = glm.scale(m_model, self.scale)
    
        return m_model
    
    def get_world_transform(self):
        # Compute world transformation matrix
        if self.parent:
            return self.parent.get_world_transform() * self.get_local_transform()
        return self.get_local_transform()
    
    def get_global_position(self):
        """
        Get the global position of the entity by extracting the translation from its world transformation matrix.
        """
        world_transform = self.get_world_transform()
        return glm.vec3(world_transform[3].x, world_transform[3].y, world_transform[3].z)

    def get_global_scale(self):
        """
        Get the global scale of the entity by extracting the scale from its world transformation matrix.
        """
        global_transform = self.get_world_transform()
        # Extract scales from the basis vectors (columns of the transform matrix)
        scale_x = glm.length(glm.vec3(global_transform[0]))
        scale_y = glm.length(glm.vec3(global_transform[1]))
        scale_z = glm.length(glm.vec3(global_transform[2]))
        return glm.vec3(scale_x, scale_y, scale_z)

    def get_global_rotation(self):
        # Combine parent's global rotation with local rotation (in quaternion space)

        mat = self.get_world_transform()
        quat = glm.quat_cast(mat)
        return glm.quat(x=glm.degrees(quat.x), y=glm.degrees(quat.y), z=glm.degrees(quat.z))


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