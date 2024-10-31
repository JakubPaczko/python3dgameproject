import numpy as np
import glm
import pygame as pg

class Plane:
    def __init__(self, app,):
        self.scale = glm.vec3(10, 10, 10)
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture(path='Game/textures/test.png')
        self.on_init()

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        return texture
    
    def update(self):
        m_model = glm.rotate(self.m_model, self.app.time, glm.vec3(0, 1, 0))
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(m_model)

    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model

    def on_init(self):
        self.shader_program['light.Ia'].write(self.app.light.Ia)
        self.shader_program['light.position'].write(self.app.light.position)
        self.shader_program['light.Id'].write(self.app.light.Id)

        self.shader_program['u_texture_0'] = 0
        self.texture.use()
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)



    def render(self):
        self.vao.render()
        self.update()

    def destroy(self):
        self.vbo.release()
        self.shader_program().release()
        self.vao.release()

    def get_vertex_data(self):
        vertices = [(-2, 0, -2), (2, 0, -2,),  (2, 0, 2),  (-2, 0, 2)]

        # for vert in vertices:
        #     vert[0] =  vert[0] * self.scale.x
        #     vert[1] *= vert[1] * self.scale.y
        #     vert[2] *= vert[2] * self.scale.z


        indices = [(1, 0, 3), (2, 1, 3)]
        
        vertex_data = self.get_data(vertices, indices)

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(1, 0, 3), (2, 1, 3)]

        
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data

    @staticmethod
    def get_data(verticies, indices):
        data = [verticies[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')
    
    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f','in_texcoord_0' , 'in_position')])
        return vao

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def get_shader_program(self, shader_name):
        with open(f'Game/shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'Game/shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        return program

class Cube:
    def __init__(self, app,):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture(path='Game/textures/test2.png')
        self.on_init()

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        return texture
    
    def update(self):
        m_model = glm.rotate(self.m_model, self.app.time, glm.vec3(0, 1, 0))
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(m_model)
        self.shader_program['camPos'].write(self.app.camera.position)


    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model

    def on_init(self):
        #light
        self.shader_program['light.position'].write(self.app.light.position)
        self.shader_program['light.Ia'].write(self.app.light.Ia)
        self.shader_program['light.Id'].write(self.app.light.Id)
        self.shader_program['light.Is'].write(self.app.light.Is)

        self.shader_program['u_texture_0'] = 0
        self.texture.use()
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)



    def render(self):
        self.texture.use()
        self.update()
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shader_program().release()
        self.vao.release()

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), (1, -1, 1,),  (1, 1, 1),  (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2), (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6), (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7), (0, 6, 1), (0, 5, 6)]
        
        vertex_data = self.get_data(vertices, indices)

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        normals = [( 0, 0, 1) * 6,
                   ( 1, 0, 0) * 6,
                   ( 0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   ( 0, 1, 0) * 6,
                   (0, -1, 0) * 6]
        
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data

    @staticmethod
    def get_data(verticies, indices):
        data = [verticies[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')
    
    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f 3f','in_texcoord_0', 'in_normal' , 'in_position')])
        return vao

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def get_shader_program(self, shader_name):
        with open(f'Game/shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'Game/shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        return program

class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}
        self.programs['default'] = self.get_program('default')
    
    def get_program(self, shader_name):
        with open(f'Game/shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'Game/shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        return program
    
    def destroy(self):
        [program.release() for program in self.programs.values()]

class VBO:
    def __init__(self, ctx):
        self.vbos = {}
        self.vbos['cube'] = CubeVbo(ctx)

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]

class BaseVBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format : str = None
        self.attrib : str = None

    def get_vertex_date(self):
        pass

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        self.vbo.release()

class CubeVbo(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attrib = ['in_textcoord_0', 'in_normal', 'in_position']

    
    def get_data(vertices, indices):
            data = [vertices[ind] for triangle in indices for ind in triangle]
            return np.array(data, dtype='f4')
    
    def get_vertex_data(self):
        vertices = [(-1, -1, 1), (1, -1, 1,),  (1, 1, 1),  (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2), (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6), (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7), (0, 6, 1), (0, 5, 6)]
        
        vertex_data = self.get_data(vertices, indices)

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        normals = [( 0, 0, 1) * 6,
                   ( 1, 0, 0) * 6,
                   ( 0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   ( 0, 1, 0) * 6,
                   (0, -1, 0) * 6]
        
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data
    
class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        #cube vao
        self.vaos['cube'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['cube'] )
        
        def get_vao(self, program, vbo):
            vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
            return vao
        
        def destroy(self):
            self.vbo.destroy()
            self.program.destroy()