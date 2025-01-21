import glm
import pygame as pg

FOV = 80
NEAR = 0.5
FAR = 200
SPEED = 0.01
SENSIVITY = 0.2



class Camera:
    def __init__(self, app):
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(2, 3, 3)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = 0
        self.pitch = 0
        self.app = app
        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()


    def test(self, quaternion):
        
        q = glm.normalize(quaternion)
    
        # Extract the front, left, and up vectors using the rotation matrix
        self.forward = glm.vec3(2 * (q.x * q.z + q.w * q.y),
                        2 * (q.y * q.z - q.w * q.x),
                        1 - 2 * (q.x * q.x + q.y * q.y))
        
        self.up = glm.vec3(2 * (q.x * q.y - q.w * q.z),
                    1 - 2 * (q.x * q.x + q.z * q.z),
                    2 * (q.y * q.z + q.w * q.x))
        
        self.right = -glm.vec3(1 - 2 * (q.y * q.y + q.z * q.z),
                        2 * (q.x * q.y + q.w * q.z),
                        2 * (q.x * q.z - q.w * q.y))
        self.m_view = self.get_view_matrix()
    
    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSIVITY
        self.pitch -= rel_y * SENSIVITY
        self.pitch = max(-90, min(90, self.pitch))

    def update_cam_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()

        if keys[pg.K_LSHIFT]:
            velocity *= 10

        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_e]:
            self.position += self.up * velocity
        if keys[pg.K_q]:
            self.position -= self.up * velocity

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
    
    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)