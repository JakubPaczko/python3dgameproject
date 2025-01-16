from ecs.component import *
import pygame as pg
import glm


class Player(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.SENSITIVITY = 0.1
        self.JUMP_FORCE = 0.05
        self.camera = None
        self.character_body : CharacterBody = None

    def update(self):
        self.rotate()
        self.jump()
        self.move()

    def move(self):
        keys = pg.key.get_pressed()
        velocity = 0.1

        if not self.character_body: return
        # rotation = glm.vec3(self.camera.rotation.x, self.owner.rotation.x, 0)
        # print(self.owner.rotation)
        vectors = self.calculate_vectors(-self.owner.rotation.y)
        input_vector = glm.vec3(0, 0, 0)
        if keys[pg.K_w]:
            input_vector += vectors[0]
        if keys[pg.K_s]:
            input_vector -= vectors[0]
        if keys[pg.K_a]:
            input_vector -= vectors[1]
        if keys[pg.K_d]:
            input_vector += vectors[1]

        input_vector = input_vector * velocity
        self.character_body.velocity = glm.vec3(input_vector.x, self.character_body.velocity.y, input_vector.z)
        

    def rotate(self):
        if not self.camera:
            for child in self.owner.children:
                if child.has_component(CameraComponent):
                    self.camera = child
        
        rel_x, rel_y = pg.mouse.get_rel()
        self.owner.rotation.y -= rel_x * self.SENSITIVITY
        self.camera.rotation.x += rel_y * self.SENSITIVITY
        self.camera.rotation.x = max(-90, min(90, self.camera.rotation.x))
    
    def jump(self):
        if not self.character_body:
            self.character_body = self.owner.get_component(CharacterBody)
        else:
            keys = pg.key.get_pressed()
            # print(self.character_body.is_on_floor)

            if keys[pg.K_SPACE]:
                if self.character_body.is_on_floor:
                    self.character_body.velocity.y += self.JUMP_FORCE
                    print(self.character_body.velocity.y)
                    self.owner.position.y += glm.vec3(0, 1, 0) * 0.1
    @staticmethod
    def calculate_vectors(y_angle):
        y_angle = glm.radians(y_angle) 

        forward_vector = glm.vec3(glm.cos(y_angle), 0, glm.sin(y_angle))

        right = glm.normalize(glm.cross(forward_vector, glm.vec3(0, 1, 0)))

        return forward_vector, right
