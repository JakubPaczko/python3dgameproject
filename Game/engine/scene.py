class Scene:
    def __init__(self, app):
        self.gameObjects = []
        self.app = app

    def update(self):
        for gameObject in self.gameObjects:
            gameObject.update(1.0)
    
    def render(self):
        for gameObject in self.gameObjects:
            gameObject.render()
    