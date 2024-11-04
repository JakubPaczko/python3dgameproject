
from ecs.gameObject import GameObject
import glm

class Component:
    def __init__(self, gameObject):
        self.owner = gameObject

class CameraComponent(Component):
    def __init__(self, gameObject, fov=90, far=100, near=0.5):
        super().__init__(gameObject)
        self.fov = fov
        self.far = far
        self.near = near

class TestComponent(Component):
    def __init__(self, gameObject):
        super().__init__(gameObject)
        self.x = 0

class ScriptComponent(Component):
    def __init__(self, gameObject):
        super().__init__(gameObject)
    

class ColliderComponent(Component):
    def __init__(self, gameObject):
        super().__init__(gameObject)

class ModelComponent(Component):
    def __init__(self, gameObject, vao_name, tex_id):
        super().__init__(gameObject)
        self.vao_name = vao_name
        self.tex_id = tex_id