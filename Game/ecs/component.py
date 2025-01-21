
from ecs.gameObject import GameObject
import glm

class Component:
    def __init__(self):
        self.owner : GameObject = None
        pass

class CameraComponent(Component):
    def __init__(self, fov=90.0, far=100.0, near=0.5):
        super().__init__()
        self.fov = fov
        self.far = far
        self.near = near

class TestComponent(Component):
    def __init__(self):
        super().__init__()
        self.x = 0

class ScriptComponent(Component):
    def __init__(self):
        super().__init__()

    def update(self):
        pass

    def start(self):
        pass

    def on_delete(self):
        pass
    
class AABBColliderComponent(Component):
    def __init__(self, size : glm.vec3 = glm.vec3(1, 1, 1)):
        super().__init__()
        self.size  : glm.vec3 = size
        self.is_trigger = False

class CharacterBody(Component):
    def __init__(self):
        super().__init__()
        self.velocity : glm.vec3 = glm.vec3(0, 0, 0)
        self.gravity : float = 1.0
        self.is_on_floor : bool = False

class ModelComponent(Component):
    def __init__(self, vao_name = 'cube', tex_id=0):
        super().__init__()
        self.vao_name = vao_name
        self.vao = None
        self.tex_id = tex_id

class CameraComponent(Component):
    def __init__(self):
        super().__init__()

class AnimationComponent(Component):
    class KeyFrame:
        def __init__(self, position, rotation, scale, time):
            self.position = position
            self.rotation = rotation
            self.scale = scale
            self.time = time

    def __init__(self):
        super().__init__()
        self.animations = {}
        self.current_animation = ''
        self.animation_time = 0.0
        self.keyframe = 0
        self.animated_object = None
        self.paused = True
    
    def add_keyframe(self, animation_name, position, rotation, scale, time):
        if not animation_name in self.animations.keys():
            self.animations[animation_name] = []
        
        
        keyframe = self.KeyFrame(position, rotation, scale, time)

        self.animations[animation_name].append(keyframe)
        

