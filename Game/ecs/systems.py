
from ecs.component import *
from ecs.scene import Scene
import pygame as pg
from camera import Camera
import moderngl as mgl
import numpy as np
import sys
from light import Light
from ecs.model import Mesh
from random import uniform
import glm

class System:
    def __init__(self, scene):
        self.scene : Scene = scene
    
    def update(self):
        pass

class RenderSystem(System):

    def __init__(self, scene):
        super().__init__(scene)
        self.ctx = scene.ctx
        self.mesh = Mesh(scene.app)
        self.camera = Camera(scene.app)
        self.app = scene.app
        self.light = Light()
        self.FREE_CAM = False

    
    def update(self):
        # self.ctx.clear(0.1, 0.1, 0.1)

        if not self.FREE_CAM:
            for entity in self.scene.filter_enitities_by_component(CameraComponent):
                self.camera.position = entity.get_global_position()
                rotation = entity.get_global_rotation()
                self.camera.test(rotation)
        else:
            self.camera.move()
            self.camera.rotate()

        self.light.position = self.camera.position

        for entity in self.scene.filter_enitities_by_component(ModelComponent):
            component : ModelComponent = entity.get_component(ModelComponent)
            
            texture = self.mesh.texture.textures[component.tex_id]
            texture.use()

            m_model = entity.get_world_transform()
            vao = self.mesh.vao.vaos[component.vao_name]
            self.update_vao(vao, m_model)
            vao.render()

        for entity in self.scene.filter_enitities_by_component(ParticleComponent):
            component : ParticleComponent = entity.get_component(ParticleComponent)
            texture = self.mesh.texture.textures[component.tex_id]
            texture.use()
            
            for particle in component.particles:

                m_model = self.get_model_matrix(particle.position, glm.vec3(0, 0, 0), particle.scale)
                vao = self.mesh.vao.vaos['plane']
                self.update_vao(vao, m_model)
                vao.render()

        if self.scene.app.DEBUG:
            for entity in self.scene.filter_enitities_by_component(AABBColliderComponent):
                component : AABBColliderComponent = entity.get_component(AABBColliderComponent)
                
                m_model = self.get_model_matrix(entity.get_global_position(), glm.vec3(0, 0, 0), component.size)
                # m_model = entity.get_world_transform()
                vao = self.mesh.vao.vaos['AABB_col']
                self.update_wireframe_vao(vao, m_model)
                
                
                vao.render(mgl.LINES)

        for entity in self.scene.filter_enitities_by_component(UiTextComponent):
            component: UiTextComponent = entity.get_component(UiTextComponent)
            
            # texture = self.mesh.texture.textures[component.tex_id]
            texture.use()
            m_model = entity.get_world_transform()
            vao = self.mesh.vao.vaos['ui']
            self.update_ui_vao(vao, m_model)
            vao.render()

    def update_ui_vao(self, vao, m_model):
        w, h = pg.display.get_surface().get_size()
        ui_proj = glm.ortho(0, w, h, 0, -1, -1)
        # vao.program['u_texture_0'] = 0
        # vao.program['in_uv_0'].write(glm.vec2(1, 1))
        # vao.program['in_vert'].write(glm.vec2(1, 1))
        vao.program['m_proj'].write(ui_proj)
        vao.program['m_model'].write(m_model)
        
        return vao

    def get_vao(self, vao_name, m_model):
        vao = self.mesh.vao.vaos[vao_name]
        
        vao.program['u_texture_0'] = 0

        vao.program['m_proj'].write(self.camera.m_proj)
        vao.program['m_view'].write(self.camera.m_view)
        vao.program['m_model'].write(m_model)

        vao.program['light.position'].write(self.light.position)
        vao.program['light.Ia'].write(self.light.Ia)
        vao.program['light.Id'].write(self.light.Id)
        vao.program['light.Is'].write(self.light.Is)

        return vao
    
    def update_vao(self, vao, m_model):
        program = vao.program

        program['u_texture_0'] = 0

        program['m_proj'].write(self.camera.m_proj)
        program['m_view'].write(self.camera.m_view)
        program['m_model'].write(m_model)

        program['light.position'].write(self.light.position)
        program['light.Ia'].write(self.light.Ia)
        program['light.Id'].write(self.light.Id)
        program['light.Is'].write(self.light.Is)

    def update_wireframe_vao(self, vao, m_model):
        program = vao.program

        program['m_proj'].write(self.camera.m_proj)
        program['m_view'].write(self.camera.m_view)
        program['m_model'].write(m_model)

    @staticmethod
    def get_model_matrix(position: glm.vec3, rotation: glm.vec3, scale: glm.vec3) -> glm.mat4:
        m_model = glm.mat4()

        m_model = glm.translate(m_model, position)

        m_model = glm.rotate(m_model, glm.radians(rotation.x), glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, glm.radians(rotation.y), glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, glm.radians(rotation.z), glm.vec3(0, 0, 1))

        m_model = glm.scale(m_model, scale)

        return m_model
    
class CollisionSystem(System):
    def __init__(self, scene):
        super().__init__(scene)
    
    def update(self):
        self.handle_collision()
        self.handle_trigger_collision()
                    
    def handle_collision(self):
        for entity1 in self.scene.filter_enitities_by_specific_component(AABBColliderComponent):
            component1 = entity1.get_component(AABBColliderComponent)
            character_body = entity1.get_component(CharacterBody)
            
            if not character_body:
                continue
            
            character_body.is_on_floor = False

            for entity2 in self.scene.filter_enitities_by_specific_component(AABBColliderComponent):
                if entity1 == entity2: continue
                character_body2 = entity2.get_component(CharacterBody)

                if character_body2 and self.is_overlaping(entity1.get_global_position(), component1.size, entity2.get_global_position(), component2.size):
                    dir_vec = entity1.position - entity2.position
                    character_body.velocity += glm.normalize(dir_vec) * 0.001
                    character_body2.velocity += glm.normalize(-dir_vec) * 0.001
                    continue

                component2 = entity2.get_component(AABBColliderComponent)
                
                collision_data = self.check_aabb_collision(entity1.get_global_position(), component1.size, entity2.get_global_position(), component2.size)
                new_pos = collision_data[0]
                collision_normal = collision_data[1]
                
                entity1.position = new_pos
                character_body.velocity *= ( glm.vec3(1, 1, 1) - collision_normal )
                
                if collision_normal == glm.vec3(0, 1, 0):
                    character_body.is_on_floor = True
    
    def handle_trigger_collision(self):
        for entity1 in self.scene.filter_enitities_by_specific_component(AABBTriggerArea):
            component1 : AABBTriggerArea = entity1.get_component(AABBTriggerArea)
            component1.overlaping_colliders = []

            for entity2 in self.scene.filter_enitities_by_specific_component(AABBTriggerArea):
                component2 : AABBTriggerArea = entity2.get_component(AABBTriggerArea)
                
                if component1 == component2: continue

                is_overlaping = self.is_overlaping(entity1.get_global_position(), component1.size, entity2.get_global_position(), component2.size)

                if is_overlaping:
                    component1.overlaping_colliders.append(component2)

    @staticmethod
    def is_overlaping(
        pos1: glm.vec3, size1: glm.vec3,
        pos2: glm.vec3, size2: glm.vec3
    ) -> bool:
    
        # Calculate the min and max points of each box
        min1 = pos1 - size1 / 2
        max1 = pos1 + size1 / 2
        min2 = pos2 - size2 / 2
        max2 = pos2 + size2 / 2

        # Calculate overlap distances along each axis
        overlap_x = max1.x - min2.x if pos1.x < pos2.x else max2.x - min1.x
        overlap_y = max1.y - min2.y if pos1.y < pos2.y else max2.y - min1.y
        overlap_z = max1.z - min2.z if pos1.z < pos2.z else max2.z - min1.z

        # If there is no overlap on any axis, return the original position
        if overlap_x <= 0 or overlap_y <= 0 or overlap_z <= 0:
            return False

        return True
    
    @staticmethod
    def check_aabb_collision(
        pos1: glm.vec3, size1: glm.vec3,
        pos2: glm.vec3, size2: glm.vec3
    ) -> glm.vec3:
    
        # Calculate the min and max points of each box
        min1 = pos1 - size1 / 2
        max1 = pos1 + size1 / 2
        min2 = pos2 - size2 / 2
        max2 = pos2 + size2 / 2

        # Calculate overlap distances along each axis
        overlap_x = max1.x - min2.x if pos1.x <= pos2.x else max2.x - min1.x
        overlap_y = max1.y - min2.y if pos1.y <= pos2.y else max2.y - min1.y
        overlap_z = max1.z - min2.z if pos1.z <= pos2.z else max2.z - min1.z

        # If there is no overlap on any axis, return the original position
        if overlap_x <= 0 or overlap_y <= 0 or overlap_z <= 0:
            return pos1, glm.vec3(0, 0, 0)

        # Determine the smallest overlap axis and direction
        if overlap_x <= overlap_y and overlap_x <= overlap_z:
            # X-axis collision resolution
            displacement = glm.vec3(-overlap_x if pos1.x < pos2.x else overlap_x, 0, 0)
            collision_normal = glm.vec3(1, 0, 0)
        elif overlap_y <= overlap_x and overlap_y <= overlap_z:
            # Y-axis collision resolution
            displacement = glm.vec3(0, -overlap_y if pos1.y < pos2.y else overlap_y, 0)
            collision_normal = glm.vec3(0, 1, 0)
        else:
            # Z-axis collision resolution
            displacement = glm.vec3(0, 0, -overlap_z if pos1.z < pos2.z else overlap_z)
            collision_normal = glm.vec3(0, 0, 1)

        # Adjust position of the first AABB to resolve collision
        new_pos = pos1 + displacement
        return new_pos, collision_normal
    
class PhysicsSystem(System):
    def update(self):
        for entity1 in self.scene.filter_enitities_by_component(CharacterBody):
            component : CharacterBody = entity1.get_component(CharacterBody)
            entity1.position += component.velocity
            if not component.is_on_floor:
                component.velocity.y -= component.gravity * self.scene.app.delta_time * 0.0001

class ScriptSystem(System):
    def update(self):
        for entity in self.scene.filter_enitities_by_component(ScriptComponent):
            script = entity.get_component(ScriptComponent)
            script.update()

class AnimationSystem(System):
    def __init__(self, scene):
        super().__init__(scene)

    def update(self):
        for entity in self.scene.filter_enitities_by_component(AnimationComponent):
            animation_component : AnimationComponent = entity.get_component(AnimationComponent)

            anim_name = animation_component.current_animation

            if anim_name == '' or animation_component.paused:
                continue

            animation = animation_component.animations[anim_name]
            keyframe = animation_component.keyframe
            keyframes = animation['keyframes']

            if len(keyframes) - 1 <= keyframe:
                animation_component.animation_time = 0
                animation_component.keyframe = 0

                if not animation['loop']:
                    animation_component.paused = True
                    animation_component.current_animation = ''
                continue


            current_keyframe = keyframes[keyframe]
            next_keyframe = keyframes[keyframe + 1]
            
            animation_component.animation_time += 1
            next_keyframe_frame = next_keyframe.time - current_keyframe.time
            lerp_value = (1 / next_keyframe_frame) * (animation_component.animation_time - current_keyframe.time)
            
            position = glm.lerp(current_keyframe.position, next_keyframe.position, lerp_value)
            rotation = glm.lerp(current_keyframe.rotation, next_keyframe.rotation, lerp_value)
            scale = glm.lerp(current_keyframe.scale, next_keyframe.scale, lerp_value)
            

            if animation_component.animation_time >= next_keyframe.time:
                animation_component.keyframe += 1
                # animation_component.animation_time = 0

            entity.position = position
            entity.rotation = rotation
            entity.scale = scale

class ParticleSystem(System):
    def __init__(self, scene):
        super().__init__(scene)

    def update(self):
        for entity in self.scene.filter_enitities_by_component(ParticleComponent):
            particle_component : ParticleComponent = entity.get_component(ParticleComponent)


            for particle in particle_component.particles[::-1]:
                particle.time += 1
                particle.position += particle.velocity
                particle.velocity *= particle_component.drag
                particle.velocity.y -= particle_component.gravity


                if particle.time >= particle_component.lifespan:
                    particle_component.particles.remove(particle)
                    particle_component.emiting = False

            particles_to_add = particle_component.max_particles - len(particle_component.particles) - 1

            if particle_component.emiting:
                for i in range(particles_to_add):
                    vel_min = particle_component.vel_min
                    ven_max = particle_component.vel_max

                    velocity = glm.vec3(uniform(vel_min.x, ven_max.x),
                                        uniform(vel_min.y, ven_max.y),
                                        uniform(vel_min.z, ven_max.z))
                    
                    particle = ParticleComponent.Particle(entity.get_global_position(), velocity)
                    particle_component.particles.append(particle)