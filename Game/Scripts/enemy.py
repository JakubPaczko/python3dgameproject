from ecs.component import *
import pygame as pg
import numpy as np
import glm
import random
from Scripts.soundManager import SoundManager 


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
        self.particle_component = None

    def take_damage(self):
        SoundManager.instance().play_sound_rand_pitch('hit')

    def start(self):
        self.character_body.gravity = 0

    def update(self):
        if self.hp <= 0:
            self.owner.queue_delete = True

        if self.character_body and self.player:
            dir_vec = self.player.position.xz - self.owner.position.xz

            dist = glm.length(dir_vec)

            if dist > 10:
                dir_vec = glm.vec3(dir_vec.x, 0, dir_vec.y) + glm.vec3(0, 1, 0) * (dist / 5)
            else:
                dir_vec = self.player.position - self.owner.position

            glm.normalize(dir_vec)
            self.look_dir = glm.lerp(self.look_dir, dir_vec, 0.05)
            self.character_body.velocity += self.look_dir * self.speed * 0.001 
            self.character_body.velocity *= self.drag

            self.calculate_lookat_quaternion(
                self.owner.position,
                self.owner.position + self.character_body.velocity
            )

    def change_pitch_numpy(self, sound, pitch_factor):
        """ Adjust the pitch using NumPy by changing the playback speed """
        sound_array = pg.sndarray.array(sound)
        new_length = int(len(sound_array) / pitch_factor)
        indices = np.round(np.linspace(0, len(sound_array) - 1, new_length)).astype(int)
        new_sound_array = sound_array[indices]
        return pg.sndarray.make_sound(new_sound_array)

    def calculate_lookat_quaternion(self, position1, position2):
        # Calculate direction vector from position1 to position2
        direction = position2 - position1  # Compute direction vector
        yaw_radians = glm.atan(direction.x, direction.z)  # Compute yaw angle (radians)
        yaw_degrees = glm.degrees(yaw_radians)
        
        self.owner.rotation.y = yaw_degrees
        # return glm.quat(x=glm.degrees(quat.x), 
                        # y=glm.degrees(quat.y), 
                        # z=glm.degrees(quat.z), 
                        # w=glm.degrees(quat.w))