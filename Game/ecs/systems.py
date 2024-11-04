
from ecs.component import *
from ecs.scene import Scene

class System:
    def __init__(self, scene):
        self.scene : Scene = scene
    
    def update():
        pass

class RenderSystem(System):
    def __init__(self, scene):
        super().__init__(scene)

class TestSystem(System):
    def __init__(self, scene):
        super().__init__(scene)

    def update(self):
        for x in self.scene.filter_enitities_by_component(TestComponent):
            component : TestComponent = x.get_component(TestComponent)
            print(component.x)
            component.x += 0.1