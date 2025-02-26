import sys
import pygame as pg
import moderngl as mgl
import ecs.systems 
from ecs.component import * 
import numpy as np
from Scripts.GameManager import GameManager
from ecs.gameObject import GameObject
from ecs.scene import Scene
import random
from imgui.integrations.pygame import PygameRenderer
import imgui

class Engine:
    def __init__(self, win_size=(1920, 1080), resolution=(int(1920/4), int(1080/4))):
        pg.init()

        self.WIN_SIZE = win_size
        self.RESOLUTION = resolution
        self.DEBUG = False

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode((self.WIN_SIZE[0], self.WIN_SIZE[1]), flags=pg.OPENGL | pg.DOUBLEBUF)
        
        

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST)  #| mgl.CULL_FACE)
        self.ctx.enable(mgl.BLEND)
        self.ctx.blend_func = mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA
        self.ctx.wireframe = False
        
        self.time = 0
        self.delta_time = 0
        self.clock = pg.time.Clock()

        self.scene = Scene(self)
        self.scene.add_system(ecs.systems.PhysicsSystem(self.scene))
        self.scene.add_system(ecs.systems.CollisionSystem(self.scene))
        self.scene.add_system(ecs.systems.ScriptSystem(self.scene))
        self.scene.add_system(ecs.systems.AnimationSystem(self.scene))
        self.scene.add_system(ecs.systems.ParticleSystem(self.scene))

        system = ecs.systems.RenderSystem(scene=self.scene)
        self.scene.add_system(system)

        game_manager_entity = GameObject()
        game_manager = GameManager(self.scene)
        game_manager_entity.add_component(game_manager)
        self.scene.add_entity(game_manager_entity)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or(event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
    
    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001
    
    def run(self):
        # Create the low-resolution framebuffer
        low_res_fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture(self.RESOLUTION, 4)]
        )
        # Set nearest filtering for sharp scaling
        low_res_fbo.color_attachments[0].filter = (mgl.NEAREST, mgl.NEAREST)

        # Quad vertices for rendering the low-res texture to the full screen
        quad_vertices = np.array([
            # x,    y,     u, v
            -1.0, -1.0,  0.0, 0.0,
            1.0, -1.0,  1.0, 0.0,
            1.0,  1.0,  1.0, 1.0,
            -1.0,  1.0,  0.0, 1.0,
        ], dtype='f4')

        # Create a vertex buffer for the quad
        quad_vbo = self.ctx.buffer(quad_vertices)

        # Shader program for rendering the quad with texture
        quad_program = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_position;
            in vec2 in_texcoord;
            out vec2 v_texcoord;
            void main() {
                v_texcoord = in_texcoord;
                gl_Position = vec4(in_position, 0.0, 1.0);
            }
            """,
            fragment_shader="""
            #version 330
            uniform sampler2D Texture;
            in vec2 v_texcoord;
            out vec4 fragColor;
            void main() {
                fragColor = texture(Texture, v_texcoord);
            }
            """
        )

        # Create the vertex array objects (VAOs) for both quad and rectangle
        quad_vao = self.ctx.vertex_array(
            quad_program,
            [(quad_vbo, '2f 2f', 'in_position', 'in_texcoord')],
        )

        while True:
            self.delta_time = self.clock.tick(120)
            self.get_time()
            self.check_events()

            self.ctx.screen.use()
            self.ctx.clear(0.0, 0.0, 0.0, depth=1.0)  # Clear to a dark gray
            
            self.scene.update()
            pg.display.flip()
