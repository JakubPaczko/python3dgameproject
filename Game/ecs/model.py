import numpy as np
import glm
import pygame as pg
import pywavefront
import moderngl as mgl
from ecs.component import Component

class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}
        self.programs['default'] = self.get_program('default')
        self.programs['wireframe'] = self.get_program('wireframe')

    
    def get_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        return program
    
    def destroy(self):
        [program.release() for program in self.programs.values()]

class VBO:
    def __init__(self, ctx):
        self.vbos = {}
        self.vbos['cube'] = CubeVbo(ctx)
        # self.vbos['skull'] = SkullVBO(ctx)
        self.vbos['cube_wireframe'] = CubeWireframeVBO(ctx)
        self.vbos['skull'] = LoadVBO(ctx, 'objects/skull/skull.obj')
        self.vbos['skeleton'] = LoadVBO(ctx, 'objects/skeleton/skeleton.obj')
        self.vbos['wall'] = LoadVBO(ctx, 'objects/wall/wall.obj')
        self.vbos['sword'] = LoadVBO(ctx, 'objects/weapons/long_sword.obj')




    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]

class BaseVBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format : str = None
        self.attrib : list = None

    def get_vertex_data(self):
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
        self.attrib = ['in_texcoord_0', 'in_normal', 'in_position']

    @staticmethod
    def get_data(vertices, indices):
            data = [vertices[ind] for triangle in indices for ind in triangle]
            return np.array(data, dtype='f4')
    
    def get_vertex_data(self):
        vertices = [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5,),  (0.5, 0.5, 0.5),  (-0.5, 0.5, 0.5),
                    (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5)]

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

class CubeWireframeVBO(CubeVbo):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f'
        self.attrib = ['in_position']
    
    def get_vertex_data(self):
        vertices = [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5,),  (0.5, 0.5, 0.5),  (-0.5, 0.5, 0.5),
                    (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5)]

        indices = [(0, 5), (1, 6), (2, 7), (3, 4),
                   (2, 3), (2, 1), (3, 0), (0, 1),
                   (4, 5), (4, 7), (7, 6), (6, 5)]
        # indices = [(0, 2, 3), (0, 1, 2), (1, 7, 2), (1, 6, 7),
        #            (6, 5, 4), (4, 7, 6), (3, 4, 5), (3, 5, 0),
        #            (3, 7, 4), (3, 2, 7), (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)
        
        return vertex_data

class SkullVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attrib = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/skull/skull.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data

class LoadVBO(BaseVBO):
    def __init__(self, ctx, path):
        self.path = path
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attrib = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront(self.path, cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
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

        self.vaos['AABB_col'] = self.get_vao(
            program = self.program.programs['wireframe'],
            vbo = self.vbo.vbos['cube_wireframe'] )

        self.vaos['skull'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['skull'] )
        
        self.vaos['skeleton'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['skeleton'] )
        
        self.vaos['wall'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['wall'] )
        
        self.vaos['sword'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['sword'] )
        
    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attrib)])
        return vao
    
    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()

class Texture:
    def __init__(self, ctx, path='textures/test2.png'):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path)
        self.textures[1] = self.get_texture('objects/skull/polygon_texture.png')
        self.textures[2] = self.get_texture('objects/wall/wall_texture.png')
        self.textures[3] = self.get_texture('objects/skeleton/skeleton_texture.png')
        self.textures[4] = self.get_texture('objects/weapons/long_sword_texture.png')



        # self.textures['skybox'] = self.get_texture_cube()

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', ' botton', 'front', 'left']
        textures = [pg.image.load(dir_path + f'{face}.{ext}').convert() for face in faces] 

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)
        
        return texture_cube

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        return texture
    
    def destroy(self):
        self.texture.release()

class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app.ctx)

    def destroy(self):
        self.vao.destroy()
        self.texture.destroy()

class BaseModel():
    def __init__(self, app):
        self.m_model = self.get_model_matrix()
        self.app = app
        self.camera = self.app.camera
    
    def set_vao(self, vao_name):
        self.vao = self.app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        
        self.program['u_texture_0'] = 0

        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)

    def set_texture(self, tex_id):
        self.tex_id = tex_id
        
        self.texture = self.app.mesh.texture.texture
        self.texture.use()

    def get_model_matrix(self):
        m_model = glm.mat4()
        # if self.gameObject:
        #     m_model = glm.translate(m_model, self.gameObject.getGlobalPosition())

        #     m_model = glm.rotate(m_model, glm.radians(self.gameObject.rotation.x), glm.vec3(1, 0, 0))
        #     m_model = glm.rotate(m_model, glm.radians(self.gameObject.rotation.y), glm.vec3(0, 1, 0))
        #     m_model = glm.rotate(m_model, glm.radians(self.gameObject.rotation.z), glm.vec3(0, 0, 1))

        #     m_model = glm.scale(m_model, self.gameObject.scale)

        return m_model;

    def render(self):
        self.m_model = self.get_model_matrix()
        self.update()
        self.vao.render()

class CubeModel(BaseModel):

    def update(self):
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
    
    def on_init(self):
        self.texture = self.app.mesh.texture.texture
        self.texture.use()

        self.program['u_texture_0'] = 0

        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
