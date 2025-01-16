from ecs.component import *
import pygame as pg
import glm


class Player(ScriptComponent):
    def update(self):
        self.move()
    
    def move(self):
        keys = pg.key.get_pressed()
        velocity = 0.1
        if keys[pg.K_UP]:
            self.owner.position += glm.vec3(1, 0, 0) * velocity
        if keys[pg.K_DOWN]:
            self.owner.position -= glm.vec3(1, 0, 0) * velocity
        if keys[pg.K_LEFT]:
            self.owner.position -= glm.vec3(0, 0, 1) * velocity
        if keys[pg.K_RIGHT]:
            self.owner.position += glm.vec3(0, 0, 1) * velocity
        if keys[pg.K_SPACE]:
            self.owner.position += glm.vec3(0, 1, 0) * velocity * 10
