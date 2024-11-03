
from gameObject import GameObject

class Component:

    def __init__(self, gameObject ):
        self.gameObject : GameObject = gameObject
    
    def render(self):
        pass

    def ready(self):
        pass

    def update(self, delta):
        pass