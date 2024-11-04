
from ecs.gameObject import GameObject
import glm

class Component:
    def __init__(self, gameObject : GameObject):
        self.owner : GameObject = gameObject

class CameraComponent(Component):
    def __init__(self, gameObject, fov=90.0, far=100.0, near=0.5):
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
    
class AABBColliderComponent(Component):
    def __init__(self, gameObject, size : glm.vec3 = glm.vec3(1, 1, 1)):
        super().__init__(gameObject)
        self.size  : glm.vec3 = size
        self.is_trigger = False

class CharacterBody(Component):
    def __init__(self, gameObject):
        super().__init__(gameObject)
        self.velocity : glm.vec3 = glm.vec3(0, 0, 0)

class ModelComponent(Component):
    def __init__(self, gameObject, vao_name = 'cube', tex_id=0):
        super().__init__(gameObject)
        self.vao_name = vao_name
        self.vao = None
        self.tex_id = tex_id
