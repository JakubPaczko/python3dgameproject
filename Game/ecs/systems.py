
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

    
    def update(self):
        # self.ctx.clear(0.1, 0.1, 0.1)
        self.camera.update()
        self.light.position = self.camera.position

        for entity in self.scene.filter_enitities_by_component(ModelComponent):
            component : ModelComponent = entity.get_component(ModelComponent)
            
            texture = self.mesh.texture.textures[component.tex_id]
            texture.use()
            m_model = self.get_model_matrix(entity.get_global_position(), entity.rotation, entity.scale)

            vao = self.mesh.vao.vaos[component.vao_name]
            self.update_vao(vao, m_model)
            # vao = self.get_vao(component.vao_name, m_model)
            # self.update_vao(component.vao, m_model)
            
            
            vao.render()

        for entity in self.scene.filter_enitities_by_component(AABBColliderComponent):
            component : AABBColliderComponent = entity.get_component(AABBColliderComponent)
            
            m_model = self.get_model_matrix(entity.get_global_position(), entity.rotation, entity.scale * component.size)
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
        for entity in self.scene.filter_enitities_by_component(AABBColliderComponent):
            component : AABBColliderComponent = entity.get_component(AABBColliderComponent)