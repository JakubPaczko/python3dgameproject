from ecs.component import ScriptComponent, CharacterBody, AnimationComponent, CameraComponent, ModelComponent, AABBColliderComponent, AABBTriggerArea, ParticleComponent, UiTextComponent
from ecs.gameObject import GameObject
from Scripts.enemy import Enemy
from Scripts.player import Player
import random
import pygame as pg
import glm
from Scripts.soundManager import SoundManager


class GameManager(ScriptComponent):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.player: Player = None
        self.enemies = [Enemy]
        self.enemy_limit = 10
        self.round = 0
        
        self.rounds = {
            1 : {
                'boss' : 0,
                'enemy' : 10
            },
            2 : {
                'boss' : 1,
                'enemy' : 9
            },
            3 : {
                'boss' : 2,
                'enemy' : 8
            },
            4 : {
                'boss' : 3,
                'enemy' : 8
            },
            5 : {
                'boss' : 4,
                'enemy' : 8
            },
            6 : {
                'boss' : 5,
                'enemy' : 10
            },
            7 : {
                'boss' : 6,
                'enemy' : 12
            },
            8 : {
                'boss' : 6,
                'enemy' : 14
            },
        }

    def start(self):
        self._init_arena()
        self._spawn_player()
        self._on_new_round()

        game_obj = GameObject()
        game_obj.scale = glm.vec3(0.1, 0.1, 0.1)
        game_obj.add_component(UiTextComponent())
        self.scene.add_entity(game_obj)

    def update(self):
        for enemy in self.enemies:
            if enemy.queue_delete:
                self.enemies.remove(enemy)
            
        if len(self.enemies) <= 0:
            self._on_new_round()

    def _on_new_round(self):
        if self.round > 1:
            SoundManager.instance().play_sound('new_round')
        self.enemies.clear()
        self.round += 1
        round_id = 0

        if self.round > max(self.rounds.keys()):
            round_id = max(self.rounds.keys())
        else:
            round_id = self.round
        
        enemy_count = self.rounds[round_id]['enemy']
        boss_count = self.rounds[round_id]['boss']
        
        for i in range(enemy_count):
            self._spawn_enemy()
        for i in range(boss_count):
            self._spawn_boss()

    def _spawn_player(self):
        game_object = GameObject()
        game_object.position = glm.vec3(0, -1, 0)
        testcomponent = ModelComponent()
        collisioncompo = AABBColliderComponent()
        collisioncompo.size = glm.vec3(100, 1, 100)
        game_object.scale = glm.vec3(99, 1, 99)
        # game_object.scale = collisioncompo.size
        game_object.add_component(collisioncompo)
        game_object.add_component(testcomponent)
        self.scene.add_entity(game_object)

        player = GameObject()
        player.add_component(AABBColliderComponent())
        player.add_component(CharacterBody())
        player_component = Player()
        player.add_component(player_component)
        player.position = glm.vec3(1, 5, 0)

        camera = GameObject()
        camera.add_component(CameraComponent())
        camera.position = glm.vec3(0, 1.8, 0)
        player.add_child(camera)

        sword = GameObject()
        sword_model = ModelComponent(vao_name='sword')
        sword_model.tex_id = 4
        sword.add_component(sword_model)
        sword_animation: AnimationComponent = AnimationComponent()

        sword_animation.add_keyframe('idle', glm.vec3(-1, -1, 1.5), glm.quat(0, 0, 90, 0), glm.vec3(0.3, 0.3, 0.3), 1)
        sword_animation.add_keyframe('idle', glm.vec3(-1, -1, 1.5), glm.quat(0, -20, 90, 0), glm.vec3(0.3, 0.3, 0.3), 20)
        sword_animation.add_keyframe('idle', glm.vec3(0, -0.5, 0.5), glm.quat(0, 90, 180, 45), glm.vec3(0.3, 0.3, 0.3), 30)
        sword_animation.add_keyframe('idle', glm.vec3(-1, -1, 1.5), glm.quat(0, 0, 90, 0), glm.vec3(0.3, 0.3, 0.3), 60)
        # sword_animation.add_keyframe('idle', glm.vec3(-1, -1, 1.5), glm.quat(0, 0, 90, 0), glm.vec3(0.3, 0.3, 0.3), 120)
        player_component.sword_animator = sword_animation
        # sword_animation.add_keyframe('idle', glm.vec3(-1, 0, 1.5), glm.quat(0, 90, 90, 0), glm.vec3(0.3, 0.3, 0.3), 60)
        # sword_animation.add_keyframe('idle', glm.vec3(-1, -1, 1.5), glm.quat(0, 0, 90, 0), glm.vec3(0.3, 0.3, 0.3), 120)
        
        sword_animation.current_animation = 'idle'
        sword_animation.animations['idle']['loop'] = False

        # sword_animation.animations['idle'] = { 1 : {} }
        sword.add_component(sword_animation)

        sword.position = glm.vec3(-1, -1, 1.5)
        sword.rotation.y = 90
        sword.scale = glm.vec3(0.3, 0.3, 0.3)
        camera.add_child(sword)

        attack_collider_component = AABBTriggerArea()
        attack_collider_component.size = glm.vec3(2, 1.5, 2)
        attack_collider = GameObject()
        attack_collider.position = glm.vec3(0, 0, 3)
        attack_collider.add_component(attack_collider_component)
        camera.add_child(attack_collider)
        player_component.hurtbox = attack_collider_component

        self.scene.add_entity(attack_collider)
        self.scene.add_entity(camera)
        self.scene.add_entity(sword)
        self.scene.add_entity(player)
        self.player = player

    def _spawn_enemy(self, enemy_level=1):
        base_damage = 9
        damage_per_level = 1
        base_hp = 15
        hp_per_level = 5

        enemy  = GameObject()
        enemy.scale = glm.vec3(1, 1, 1)
        enemy.position = glm.vec3(random.randrange(- 10, 10), random.randrange(0, 10), random.randrange(- 10, 10))
        enemy_component: Enemy = Enemy()
        enemy_component.damage = base_damage + damage_per_level * enemy_level
        enemy_component.hp =  base_hp + hp_per_level * enemy_level
        
        enemy_character_body = CharacterBody()
        enemy.add_component(enemy_component)
        enemy.add_component(enemy_character_body)
        particle_component = ParticleComponent()
        enemy_component.particle_component = particle_component
        enemy.add_component(particle_component)
        enemy_collider = AABBColliderComponent()
        enemy_collider.size = glm.vec3(2, 2, 2)
        enemy.add_component(enemy_collider)
        enemy.add_component(AABBTriggerArea())
        enemy.add_component(ModelComponent('skull', 1))
        enemy_component.player = self.player
        enemy_component.character_body = enemy_character_body
        self.scene.add_entity(enemy)
        self.enemies.append(enemy)

    def _spawn_boss(self, enemy_level=1):
        base_damage = 18
        damage_per_level = 2
        base_hp = 30
        hp_per_level = 10

        enemy  = GameObject()
        enemy.scale = glm.vec3(1, 1, 1)
        enemy.position = glm.vec3(random.randrange(- 10, 10), random.randrange(0, 10), random.randrange(- 10, 10))
        enemy_component: Enemy = Enemy()
        enemy_component.damage = base_damage + damage_per_level * enemy_level
        enemy_component.hp =  base_hp + hp_per_level * enemy_level
        
        enemy_character_body = CharacterBody()
        enemy.addComponent(enemy_component)
        enemy.addComponent(enemy_character_body)
        particle_component = ParticleComponent()
        enemy_component.particle_component = particle_component
        enemy.addComponent(particle_component)
        enemy_collider = AABBColliderComponent()
        enemy_collider.size = glm.vec3(2, 2, 2)
        enemy.addComponent(enemy_collider)
        enemy.addComponent(AABBTriggerArea())
        enemy.addComponent(ModelComponent('skull_boss', 1))
        enemy_component.player = self.player
        enemy_component.character_body = enemy_character_body
        self.scene.add_entity(enemy)
        self.enemies.append(enemy)

    def _init_arena(self):
        game_object = GameObject()
        game_object.position = glm.vec3(0, -1, 0)
        arena_floor = ModelComponent()
        arena_floor_collider = AABBColliderComponent()
        arena_floor_collider.size = glm.vec3(100, 1, 100)
        game_object.scale = glm.vec3(99, 1, 99)
        game_object.add_component(arena_floor)
        game_object.add_component(arena_floor_collider)
        self.scene.add_entity(game_object)

        for x in range(0, 5):
            game_object2 = GameObject()
            game_object2.position = glm.vec3((20 * x) - 40, -1, 50)
            game_object2.rotation = glm.quat(0, 0, 90, 0)

            wall_model = ModelComponent(vao_name='wall', tex_id=2)
            wall_collider = AABBColliderComponent()
            wall_collider.size = glm.vec3(20, 20, 2)

            game_object2.add_component(wall_model)
            game_object2.add_component(wall_collider)
            self.scene.add_entity(game_object2)
        
        for x in range(0, 5):
            game_object2 = GameObject()
            game_object2.position = glm.vec3((20 * x) - 40, -1, -50)
            game_object2.rotation = glm.quat(0, 0, 90, 0)

            wall_model = ModelComponent(vao_name='wall', tex_id=2)
            wall_collider = AABBColliderComponent()
            wall_collider.size = glm.vec3(20, 20, 2)

            game_object2.add_component(wall_model)
            game_object2.add_component(wall_collider)
            self.scene.add_entity(game_object2)
        
        for x in range(0, 5):
            game_object2 = GameObject()
            game_object2.position = glm.vec3(50, -1, (20 * x) - 40)
            game_object2.rotation = glm.quat(0, 0, 0, 0)

            wall_model = ModelComponent(vao_name='wall', tex_id=2)
            wall_collider = AABBColliderComponent()
            wall_collider.size = glm.vec3(2, 20, 20)

            game_object2.add_component(wall_model)
            game_object2.add_component(wall_collider)
            self.scene.add_entity(game_object2)
        
        for x in range(0, 5):
            game_object2 = GameObject()
            game_object2.position = glm.vec3(-50, -1, (20 * x) - 40)
            game_object2.rotation = glm.quat(0, 0, 0, 0)

            wall_model = ModelComponent(vao_name='wall', tex_id=2)
            wall_collider = AABBColliderComponent()
            wall_collider.size = glm.vec3(2, 20, 20)

            game_object2.add_component(wall_model)
            game_object2.add_component(wall_collider)
            self.scene.add_entity(game_object2)