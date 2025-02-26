import glm
class Light:
    def __init__(self, position = (3, 3, 3), color=(1, 1, 1)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)

        self.Ia = 0.3 * self.color
        self.Id = 0.5 * self.color
        self.Is = 0.0 * self.color
