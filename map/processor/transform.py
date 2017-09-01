from map import universe
from map.component import Transform, Renderer
import math

class TransformProcessor(universe.Processor):
    def __init__(self):
        super(TransformProcessor, self).__init__()

    def start(self, *args, **kwargs):
        for entity, (tran, rend) in self.world.get_components(Transform, Renderer):
            if rend.model:
                import math3d
                rend.model.position = math3d.vector(
                    tran.position.x,
                    tran.position.y,
                    tran.position.z
                )
                rend.model.scale = math3d.vector(
                    tran.scale.x,
                    tran.scale.y,
                    tran.scale.z
                )
                rend.model.rotation_matrix = math3d.euler_to_matrix(
                    math3d.vector(
                        tran.rotation.x * math.pi / 180,
                        tran.rotation.y * math.pi / 180,
                        tran.rotation.z * math.pi / 180
                    )
                )

    def update(self, dt, *args, **kwargs):
        pass