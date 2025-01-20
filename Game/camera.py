import glm
import pygame as pg

FOV = 50
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

    def update(self):
        # self.move()
        # self.rotate()
        # self.update_cam_vectors()
        self.m_view = self.get_view_matrix()

    def test(self, quaternion):
        rotation_matrix = glm.mat3_cast(quaternion)
        
        # Extract the basis vectors
        right = glm.vec3(rotation_matrix[0][0], rotation_matrix[1][0], rotation_matrix[2][0])  # X-axis
        up = glm.vec3(rotation_matrix[0][1], rotation_matrix[1][1], rotation_matrix[2][1])     # Y-axis
        forward = glm.vec3(rotation_matrix[0][2], rotation_matrix[1][2], rotation_matrix[2][2]) # Z-axis
        self.right = right
        self.up = up
        self.forward = forward
        # print(quaternion)
        # print(forward)
        # print(up)
        # print(right)

        # return forward, right, up
    
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