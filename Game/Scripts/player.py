from ecs.component import ScriptComponent, CharacterBody, AnimationComponent, CameraComponent
from Scripts.enemy import Enemy
import pygame as pg
import glm
from Scripts.soundManager import SoundManager


class Player(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.SENSITIVITY = 0.1
        self.JUMP_FORCE = 0.05
        self.SPEED = 0.1
        self.ATTACK_DAMAGE = 10
        self.camera = None
        self.character_body: CharacterBody = None
        self.sword_animator: AnimationComponent = None
        self.hurtbox = None
        self.can_attack = True
        self.attack_timer = 0
        self.attack_cooldown = 60
        self.drag = 0.85

    def update(self):
        self.rotate()
        self.jump()
        self.move()
        self.attack()
        # if self.hurtbox:
        #     print(self.hurtbox.overlaping_colliders)

    def move(self):
        keys = pg.key.get_pressed()

        if not self.character_body:
            return
        # rotation = glm.vec3(self.camera.rotation.x, self.owner.rotation.x, 0)
        # print(self.owner.rotation)
        forward, right = self.calculate_vectors(self.owner.rotation.y)
        input_vector = glm.vec3(0, 0, 0)
        # self.owner.rotation.z = 0
        if self.character_body.is_on_floor:
            if keys[pg.K_w]:
                input_vector += forward
            if keys[pg.K_s]:
                input_vector -= forward
            if keys[pg.K_a]:
                input_vector -= right
                self.owner.rotation.z = glm.lerp(self.owner.rotation.z, -5, 0.1)
            if keys[pg.K_d]:
                input_vector += right
                self.owner.rotation.z = glm.lerp(self.owner.rotation.z, 5, 0.1)

        if not keys[pg.K_d] and not keys[pg.K_a]:
            self.owner.rotation.z = glm.lerp(self.owner.rotation.z, 0, 0.1)

        glm.normalize(input_vector)
        input_vector *= self.SPEED * 0.2
        self.character_body.velocity += glm.vec3(
                                                    input_vector.x,
                                                    0,
                                                    input_vector.z
                                                )

        if self.character_body.is_on_floor:
            self.character_body.velocity *= self.drag

    def attack(self):
        if not self.sword_animator:
            return

        if self.attack_timer == 30:
            for collider in self.hurtbox.overlaping_colliders:
                enemy = collider.owner.get_component(Enemy)
                if enemy:
                    enemy.hp -= self.ATTACK_DAMAGE
                    enemy.particle_component.emiting = True
                    enemy.take_damage()
                    print(enemy.hp)


        if not self.can_attack:
            self.attack_timer += 1
            if self.attack_timer > self.attack_cooldown:
                self.can_attack = True
                self.attack_timer = 0
            return

        keys = pg.mouse.get_pressed()

        if keys[0]:
            SoundManager.instance().play_sound_rand_pitch('sword')
            self.can_attack = False
            self.sword_animator.paused = False
            self.sword_animator.current_animation = 'idle'

    def rotate(self):
        # self.owner.rotation.y += 0.1
        if not self.camera:
            for child in self.owner.children:
                if child.has_component(CameraComponent):
                    self.camera = child

        rel_x, rel_y = pg.mouse.get_rel()
        self.owner.rotation.y -= rel_x * self.SENSITIVITY
        self.camera.rotation.x += rel_y * self.SENSITIVITY
        self.camera.rotation.x = max(-90, min(90, self.camera.rotation.x))
        # print(self.camera.get_global_rotation())

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

        forward_vector = glm.vec3(glm.sin(y_angle), 0, glm.cos(y_angle))

        right = glm.normalize(glm.cross(forward_vector, glm.vec3(0, 1, 0)))

        return forward_vector, right
