from universe import universe
from universe.component import Renderer, Animator, Transform, StateMachine
from universe.manager import Client, ClientOnly
import math

class RenderProcessor(universe.Processor):
    def __init__(self):
        super(RenderProcessor, self).__init__()


    def create_model(self, tran, rend):
        if type(rend.gim) == str:
            model = Client.nexo_world.model(rend.gim, Client.scene)
            model.position = Client.nexo_math3d.vector(
                tran.position.x,
                tran.position.y,
                tran.position.z
            )
            model.rotation_matrix = Client.nexo_math3d.euler_to_matrix(
                Client.nexo_math3d.vector(
                    tran.rotation.x * math.pi / 180,
                    tran.rotation.y * math.pi / 180,
                    tran.rotation.z * math.pi / 180
                )
            )
            model.scale = Client.nexo_math3d.vector(
                tran.scale.x,
                tran.scale.y,
                tran.scale.z
            )
            model.visible = rend.visible
            rend.model = model
        elif type(rend.gim) == list:
            model = Client.nexo_world.primitives(Client.scene)
            model.create_line(rend.gim)
            model.visible = rend.visible
            rend.model = model

    def create_grand(self, tran, rend):
        if type(rend.grand_gim) == str:
            model = Client.nexo_world.model(rend.grand_gim, Client.scene)
            model.position = Client.nexo_math3d.vector(
                tran.position.x,
                tran.position.y,
                tran.position.z
            )
            model.rotation_matrix = Client.nexo_math3d.euler_to_matrix(
                Client.nexo_math3d.vector(
                    tran.rotation.x * math.pi / 180,
                    tran.rotation.y * math.pi / 180,
                    tran.rotation.z * math.pi / 180
                )
            )
            model.scale = Client.nexo_math3d.vector(
                tran.scale.x,
                tran.scale.y,
                tran.scale.z
            )
            rend.grand_model = model

    @ClientOnly
    def start(self, *args, **kwargs):
        for entity, (tran, rend) in self.world.get_components(Transform, Renderer):
            if not rend.model:
                self.create_model(tran, rend)
            if not rend.grand_model:
                self.create_grand(tran, rend)

    @ClientOnly
    def update(self, dt, *args, **kwargs):
        for entity, (tran, rend) in self.world.get_components(Transform, Renderer):
            if rend.model:
                if tran.static:
                    continue
                rend.model.visible = rend.visible
                if rend.grand_model:
                    rend.grand_model.visible = rend.visible
                rend.model.position = Client.nexo_math3d.vector(
                    tran.position.x,
                    tran.position.y,
                    tran.position.z
                )
                rend.model.rotation_matrix = Client.nexo_math3d.euler_to_matrix(
                    Client.nexo_math3d.vector(
                        tran.rotation.x * math.pi / 180,
                        tran.rotation.y * math.pi / 180,
                        tran.rotation.z * math.pi / 180
                    )
                )
            else:
                self.create_model(tran, rend)


class AnimatorProcessor(universe.Processor):
    def __init__(self):
        super(AnimatorProcessor, self).__init__()

    @ClientOnly
    def start(self, *args, **kwargs):
        for entity, (rend, anim, state) in self.world.get_components(Renderer, Animator, StateMachine):
            if rend.model:
                rend.model.play_animation(
                    anim.animations.get(state.state, {}).get('name', 'idle'),
                    -1.0,
                    0,
                    0,
                    int(anim.animations.get(state.state, {}).get('loop', 2)),
                    anim.animations.get(state.state, {}).get('rate', 1.0)
                )

    @ClientOnly
    def update(self, dt, *args, **kwargs):
        for entity, (rend, anim, state) in self.world.get_components(Renderer, Animator, StateMachine):
            if state.transited:
                state.transited = False
                if rend.model:
                    rend.model.play_animation(
                        anim.animations.get(state.state, {}).get('name', 'idle'),
                        -1.0,
                        0,
                        0,
                        int(anim.animations.get(state.state, {}).get('loop', 2)),
                        anim.animations.get(state.state, {}).get('rate', 1.0)
                    )