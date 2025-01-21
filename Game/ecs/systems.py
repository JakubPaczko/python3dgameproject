
from ecs.component import *
from ecs.scene import Scene
import pygame as pg
from camera import Camera
import moderngl as mgl
import numpy as np
import sys
from light import Light
from ecs.model import Mesh

class System:
    def __init__(self, scene):
        self.scene : Scene = scene
    
    def update(self):
        pass

class TestSystem(System):
    def __init__(self, scene):
        super().__init__(scene)

    def update(self):
        for x in self.scene.filter_enitities_by_component(TestComponent):
            component : TestComponent = x.get_component(TestComponent)
            print(component.x)
            component.x += 0.1
        
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
                # self.camera.m_view = entity.get_world_transform()
                # self.camera.pitch = -rotation.x
                # self.camera.yaw = -rotation.y
                # self.camera.roll = -rotation.z
                self.camera.test(rotation)
                # print(entity.get_global_rotation())
                # print(glm.vec3(self.camera.pitch, self.camera.yaw, self.camera.roll))
        else:
            self.camera.move()
            self.camera.rotate()

        self.light.position = self.camera.position

        for entity in self.scene.filter_enitities_by_component(ModelComponent):
            component : ModelComponent = entity.get_component(ModelComponent)
            
            texture = self.mesh.texture.textures[component.tex_id]
            texture.use()
            # m_model = self.get_model_matrix(entity.get_global_position(), entity.get_global_rotation(), entity.get_global_scale())
            m_model = entity.get_world_transform()
            vao = self.mesh.vao.vaos[component.vao_name]
            self.update_vao(vao, m_model)
            # vao = self.get_vao(component.vao_name, m_model)
            # self.update_vao(component.vao, m_model)
            
            
            vao.render()

        if self.scene.app.DEBUG:
            for entity in self.scene.filter_enitities_by_component(AABBColliderComponent):
                component : AABBColliderComponent = entity.get_component(AABBColliderComponent)
                
                m_model = self.get_model_matrix(entity.get_global_position(), glm.vec3(0, 0, 0), entity.scale * component.size)
                # m_model = entity.get_world_transform()
                vao = self.mesh.vao.vaos['AABB_col']
                self.update_wireframe_vao(vao, m_model)
                
                
                vao.render(mgl.LINES)
        




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
    def get_model_matrix(position : glm.vec3, rotation : glm.vec3, scale : glm.vec3) -> glm.mat4:
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
        for entity1 in self.scene.filter_enitities_by_component(AABBColliderComponent):
            component1 = entity1.get_component(AABBColliderComponent)
            character_body = entity1.get_component(CharacterBody)
            
            if not character_body:
                continue
            
            character_body.is_on_floor = False

            for entity2 in self.scene.filter_enitities_by_component(AABBColliderComponent):
                if entity1 == entity2: continue
                component2 = entity2.get_component(AABBColliderComponent)
                
                collision_data = self.check_aabb_collision(entity1.position, component1.size, entity2.position, component2.size)
                new_pos = collision_data[0]
                collision_normal = collision_data[1]
                
                entity1.position = new_pos
                character_body.velocity *= ( glm.vec3(1, 1, 1) - collision_normal )
                
                if collision_normal == glm.vec3(0, 1, 0):
                    character_body.is_on_floor = True
                    
                # print(character_body.velocity)
    
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
        overlap_x = max1.x - min2.x if pos1.x < pos2.x else max2.x - min1.x
        overlap_y = max1.y - min2.y if pos1.y < pos2.y else max2.y - min1.y
        overlap_z = max1.z - min2.z if pos1.z < pos2.z else max2.z - min1.z

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
