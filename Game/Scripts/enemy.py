from ecs.component import *
import pygame as pg
import glm


class Enemy(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.speed = 0.1
        self.damage = 1
        self.hp = 20
        self.player = None
        self.character_body = None
        self.drag = 0.99
        self.look_dir = glm.vec3(0, 1, 0)
    
    def start(self):
        self.character_body.gravity = 0

    def update(self):
        if self.hp <= 0:
            self.owner.queue_delete = True

        if self.character_body and self.player:
            dir_vec = self.player.position.xz - self.owner.position.xz

            dist = glm.length( dir_vec )

            if dist > 10:
                dir_vec = glm.vec3(dir_vec.x, 0, dir_vec.y) + glm.vec3(0, 1, 0) * (dist / 5)
            else:
                dir_vec = self.player.position - self.owner.position

            glm.normalize(dir_vec)
            self.look_dir = glm.lerp(self.look_dir, dir_vec, 0.05)
            self.character_body.velocity += self.look_dir * self.speed * 0.001 
            self.character_body.velocity *= self.drag
            self.owner.rotation = self.calculate_lookat_quaternion(self.owner.position, self.player.position)        
    
    def calculate_lookat_quaternion(self, position1, position2):
        # Calculate direction vector from position1 to position2
        direction = glm.normalize(position2 - position1)
        
        # Default "up" vector
        up = glm.vec3(0, 1, 0)
        
        # Avoid degeneracy by checking if direction is parallel to up
        if glm.length(glm.cross(direction, up)) < 1e-6:
            up = glm.vec3(1, 0, 0)  # Use a different up vector
        
        # Create the look-at matrix
        look_at_matrix = glm.lookAt(position1, position2, up)
        
        # Extract rotation (upper-left 3x3 part of the matrix)
        rotation_matrix = glm.mat3(look_at_matrix)
        
        # Convert the rotation matrix to a quaternion
        look_at_quaternion = glm.quat_cast(rotation_matrix)
        
        return look_at_quaternion