# coding=utf-8
from universe import universe
from universe.component import Monster, Transform, Renderer, Animator, Collider, Player, StateMachine
from universe.misc import Vector3

class MonsterProcessor(universe.Processor):
    def __init__(self):
        super(MonsterProcessor, self).__init__()

    def start(self, *args, **kwargs):
        pass

    def update(self, dt, *args, **kwargs):

        for entity, (rend, tran, monster, anim, coll, state) \
                in self.world.get_components(Renderer, Transform, Monster, Animator, Collider, StateMachine):

            for entity, (player_tran, player) in self.world.get_components(Transform, Player):
                target_pos = player_tran.position
                dist = Vector3.distance(tran.position, target_pos)
                if dist < monster.attack_range:
                    state.trigger('attack')
                elif dist > monster.detection_range:
                    state.trigger('idle')
                else:
                    state.trigger('walk')
                    delta_pos = target_pos - tran.position
                    tran.position += delta_pos.normalized * dt * monster.move_speed
                    monster.target_rotation = Vector3(0, Vector3.angle_to_axis(delta_pos, Vector3.forward(), Vector3.up()), 0)
                    tran.rotation = monster.target_rotation
