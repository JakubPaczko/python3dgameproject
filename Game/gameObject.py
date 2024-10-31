import glm

class GameObject:


    def __init__(self, name : str, **attribs):
        self.name = name
        
        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        
        self.parent = None
        self.children = []
        self.components = []

        self.queue_destroy = False

    def ready(self) -> None:
        for component in self.components:
            component.ready(self)

    def update(self, delta : float) -> None:
        for component in self.components:
            component.update(self, delta)
    
    def getGlobalPosition(self) -> glm.vec3:
        if self.parent:
            return self.position + self.parent.getGlobalPosition()
        return self.position
    
    def getGlobalRotation(self) -> glm.vec3:
        if self.parent:
            return self.rotation + self.rotation.getGlobalRotation()
        return self.rotation
    
    def addComponent(self, componenet):
        self.components.append(componenet)

    def removeComponent(self, componentName : str):
        pass

    def destroy(self):
        self.queue_destroy = True