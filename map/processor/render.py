from map import universe
from map.component import Renderer, Animator
from map.manager import client

class RenderProcessor(universe.Processor):
    def __init__(self):
        super(RenderProcessor, self).__init__()

    @client.only
    def start(self, *args, **kwargs):
        for entity, rend in self.world.get_component(Renderer):
            if rend.primitive is not None:
                model = client.nexo_world.primitives(client.scene)
                model.create_line(rend.primitive)
                rend.model = model
            elif rend.gim is not None:
                rend.model = client.nexo_world.model(rend.gim, client.scene)

    @client.only
    def update(self, dt, *args, **kwargs):
        pass

class AnimatorProcessor(universe.Processor):
    def __init__(self):
        super(AnimatorProcessor, self).__init__()

    @client.only
    def start(self, *args, **kwargs):
        for entity, animator in self.world.get_component(Animator):
            for param in animator.parameters:
                conditions = animator.transitions[animator.state]

                pass

    @client.only
    def update(self, dt, *args, **kwargs):
        pass