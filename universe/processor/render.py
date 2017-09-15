# coding=utf-8
from universe import universe
from universe.component import Renderer, Shadow, Transform
from universe.manager import Client, ClientOnly
import math

class RenderProcessor(universe.Processor):
    def __init__(self):
        super(RenderProcessor, self).__init__()

    def create_model(self, tran, rend):
        if type(rend.gim) == str:
            if isinstance(rend, Shadow):
                if rend.block is None:
                    return
                gim = rend.gim % rend.block
            else:
                gim = rend.gim
            model = Client.nexo_world.model(gim, Client.scene)
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
                tran.scale.x * rend.scale.x,
                tran.scale.y * rend.scale.y,
                tran.scale.z * rend.scale.z
            )
            model.visible = rend.visible
            rend.model = model

            if rend.animator:
                rend.animator.bind_model(rend.model)

        elif type(rend.gim) == list:
            model = Client.nexo_world.primitives(Client.scene)
            model.create_line(rend.gim)
            model.visible = rend.visible
            rend.model = model

    @ClientOnly
    def start(self, *args, **kwargs):
        for entity, (tran, rend) in self.world.get_new_entities_components(Transform, Renderer):
            # 主模型
            if not rend.model:
                self.create_model(tran, rend)

            # 影子
            shadow = self.world.component_for_entity(entity, Shadow)
            if shadow and not shadow.model:
                self.create_model(tran, shadow)

    @ClientOnly
    def update(self, dt, *args, **kwargs):
        pass
