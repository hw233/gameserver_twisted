# coding=utf-8

from GameObject import GameObject
from common import Util, GameTime


class Bullet(GameObject):
    def __init__(self, arena, pos, direct, owner, skill_id, node_name):
        super(Bullet, self).__init__(100, pos)
        self.arena = arena
        self.owner = owner
        self.skill_id = skill_id
        self.node_name = node_name

        self.node_config = self.owner.skill_handler.get_skill_node_config(skill_id, node_name)
        self.damage_data = self.node_config.get('damage')

        bullet_data = self.damage_data.get('bullet')

        self.group_id = owner.get_group_id()  # 子弹所属的group

        self.set_position(pos)
        self.origin_pos = pos

        self.move_velocity = direct * bullet_data.get('speed')
        self.accelerate_velocity = direct * bullet_data.get('acceleration')

        # 特效最大飞行距离
        self.max_dis = bullet_data.get('max_dis')

    def update(self):
        if self.is_dead():
            return

        self.move()

    def move(self):
        target_pos = self.get_position() + Util.calculate_move_distance(self.move_velocity, self.accelerate_velocity,
                                                                        GameTime.delta_time)

        if (target_pos - self.origin_pos).magnitude > self.max_dis:
            self.destroy_me()
            return
        if self.check_hit_target(self.get_position(), target_pos):
            return
        self.set_position(target_pos)
        self.move_velocity += self.accelerate_velocity * GameTime.delta_time

    def check_hit_target(self, src_pos, target_pos):
        # 静态检测  FIX ME !!!
        # 伤害检测
        min_dis = None
        hit_target = None
        for gid, group in self.arena.group_map.iteritems():
            if gid == self.group_id:
                continue
            for other in group:
                pos = other.get_position()

                if Util.segment_circle_intersect(src_pos, target_pos, pos, other.get_body_radius()):
                    dis = (src_pos - pos).magnitude
                    if min_dis is None or dis < min_dis:
                        min_dis = dis
                        hit_target = other

        if hit_target is None:
            return False

        self.arena.handle_player_hit_move(self.get_position(), [hit_target, ], self.node_config, hit_time=0)

        self.destroy_me(hit_target)
        return True

    def destroy_me(self, hit_target=None):
        if self.is_dead():
            return
        self.set_dead()
        self.arena.handle_bullet_hit(self, hit_target)
