import sys
import pygame as pg
import moderngl as mgl
from components.model import *
from camera import Camera
from light import Light

class Engine:
    def __init__(self, win_size=(320, 200)):
        #init pygame modules
        pg.init()
        #set window size
        self.WIN_SIZE = win_size

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode((self.WIN_SIZE[0] * 4, self.WIN_SIZE[1] * 4), flags=pg.OPENGL | pg.DOUBLEBUF)

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)


        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        self.time = 0
        self.delta_time = 0
        self.clock = pg.time.Clock()
        self.camera = Camera(self)
        self.light = Light()

        self.mesh = Mesh(self)

        self.scene = CubeModel(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or(event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()
    
    def render(self):
        # self.ctx.clear(color=(0.08, 0.16, 0.18))
        # self.scene.render()
        # pg.display.flip()
                # Render the scene to the low-resolution framebuffer
        pass




    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001
    
    def run(self):
            # Create the low-resolution framebuffer
        low_res_fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture(self.WIN_SIZE, 4)]
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
            self.camera.update()
            self.render()

             # Render the scene to the low-resolution framebuffer
            low_res_fbo.use()
            self.ctx.clear(0.1, 0.1, 0.1)  # Clear to a dark gray

            # Draw a red rectangle in the low-resolution framebuffer
            self.scene.render()
            
            # Render the low-res texture to the full screen
            self.ctx.screen.use()
            self.ctx.clear(0.0, 0.0, 0.0)  # Clear the screen
            low_res_fbo.color_attachments[0].use(location=0)  # Use texture as input
            quad_vao.render(mgl.TRIANGLE_FAN)  # Draw the full-screen quad

            # Update the display
            pg.display.flip()
