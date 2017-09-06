from universe import universe
from universe.component import Renderer, Animator, Transform
from universe.manager import client
import math

class RenderProcessor(universe.Processor):
    def __init__(self):
        super(RenderProcessor, self).__init__()

    @client.only
    def start(self, *args, **kwargs):
        def create_model_callback(model, user_data, current_task):
            if model:
                client.get_scene().add_object(model)
                user_data['rend'].model = model
                tran = user_data['tran']
                import math3d
                model.position = math3d.vector(
                    tran.position.x,
                    tran.position.y,
                    tran.position.z
                )
                model.scale = math3d.vector(
                    tran.scale.x,
                    tran.scale.y,
                    tran.scale.z
                )
                model.rotation_matrix = math3d.euler_to_matrix(
                    math3d.vector(
                        tran.rotation.x * math.pi / 180,
                        tran.rotation.y * math.pi / 180,
                        tran.rotation.z * math.pi / 180
                    )
                )
                client.set_loaded_models(client.get_loaded_models() + 1)

        for entity, (tran, rend) in self.world.get_components(Transform, Renderer):
            if rend.model:
                continue

            if type(rend.gim) == str:
                client.set_total_models(client.get_total_models() + 1)
                client.nexo_world.create_model_async(rend.gim, create_model_callback, {
                    'rend': rend,
                    'tran': tran
                })
            elif type(rend.gim) == list:
                model = client.nexo_world.primitives(client.get_scene())
                model.create_line(rend.gim)
                rend.model = model

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