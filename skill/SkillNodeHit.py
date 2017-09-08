# coding=utf-8
import time

from common import conf, events, util
from network import NetworkSocket
from skill.SkillNode import SkillNode


class SkillNodeHit(SkillNode):
    def __init__(self, skill, node_name, node_config):
        super(SkillNodeHit, self).__init__(skill, node_name, node_config)

    def start(self, params=None):
        targets = params.get('targets', ())
        if len(targets) == 0:
            return

        targets_str = util.pack_id_pos_list_to_string([x.get_id(), x.get_position()] for x in targets)
        pos = self.entity.get_position()
        msg = events.MsgCSPlayerHit(self.entity.get_id(), pos.x, pos.y, pos.z, self.skill().get_id(), self.node_name,
                                    targets_str, params.get('attack_percent', 1.0))
        self.entity.scene_manager.perform_player_hit_effect(msg, params.get('hit_point'))

        # 本地玩家才需要发送hit命中消息
        if self.entity.is_local():
            NetworkSocket.send(msg.marshal())
