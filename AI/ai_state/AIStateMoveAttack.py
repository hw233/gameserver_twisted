# coding=utf-8
from state.StateIdle import StateIdle
from state.StateBase import StateBase


# 这个类暂时不用，如果以后需要做动作融合，可以作参考
class StateMoveAttack(StateBase):
    pass
    # run_clip = "run"
    # attack_clip = "attack"
    #
    # def __init__(self, entity, name):
    #     super(StateMoveAttack, self).__init__(entity, name)
    #     self.tree = self.rebuild_move_attack_tree(self)
    #
    # def on_enter(self):
    #     self.entity().model.get_animator().SetAnimationTree(self.tree)
    #     self.entity().model.get_animator().ActivateAnimationTree()
    #
    # def playing(self):
    #     return True
    #
    # def rebuild_move_attack_tree(self, move_attack_node):
    #     animator = self.entity().model.get_animator()
    #     # 创建一个layer节点作为动画树的根。
    #     # layer节点必须有子节点。最后一个子节点位于最高层，第一个子节点位于最低层。
    #     # 高层覆盖低层。通过设置骨骼权重可以实现按身体部位覆盖。
    #     root = animator.CreateNode("Layer")
    #     root.smoothWeightsDuration = 0  # 子节点的权重渐变到targetWeight的时间。
    #
    #     # 创建一个source节点作为layer节点的第一个儿子。
    #     # source节点是叶子节点，它从一个动画clip读取动画数据。
    #     run = animator.CreateNode("Source")
    #     run.clipName = StateIdle.ani_clip_name
    #     run_state = root.AddChild(run)  # AddChild返回子节点状态对象。
    #     run_state.targetWeight = 1  # 设置子节点的权重为1，会从当前权重（默认0）渐变为1，经过0.3秒。
    #
    #     # 创建一个blend节点作为layer节点的第二个儿子。
    #     # blend节点必须有子节点。blend节点输出的动画为所有子节点的加权平均值。
    #     upbody_motion = animator.CreateNode("Blend")
    #     upbody_motion.smoothWeightsDuration = 1  # 子节点的权重渐变到targetWeight的时间。
    #     upbody_motion_state = root.AddChild(upbody_motion)
    #     upbody_motion_state.SetBoneTreeWeight("biped spine", 0)
    #     # upbody_motion_state.SetBoneTreeWeight("biped l thigh", 0)  # 去掉左腿权重
    #     # upbody_motion_state.SetBoneTreeWeight("biped r thigh", 0)  # 去掉右腿权重
    #     # upbody_motion_state.SetBoneTreeWeight("biped pelvis", 0)  # 去掉右腿权重
    #     upbody_motion_state.targetWeight = 1  # 完全覆盖低层动画，但因为两条腿的骨骼权重设成了0，所以两条腿完全由run控制
    #
    #     # 创建一个source节点作为blend节点的第一个儿子
    #     skill = animator.CreateNode("Source")
    #     skill.clipName = type(move_attack_node).run_clip  # FIX ME !!!
    #     skill_state = upbody_motion.AddChild(skill)
    #     skill_state.targetWeight = 1
    #
    #     # 创建一个source节点作为blend节点的第二个儿子
    #     # guard = animator.CreateNode("Source")
    #     # guard.clipName = "guard1h"
    #     # guardState = upbody_motion.AddChild(guard)
    #     # guardState.SetBoneTreeWeight("biped", 0)  # 去掉全身权重
    #     # guardState.SetBoneTreeWeight("biped r clavicle", 1)  # 右臂权重设为1
    #     # guardState.targetWeight = 9  # blend节点的两个儿子之间以1:9混合
    #
    #     # animator.SetAnimationTree(root)
    #     # animator.ActivateAnimationTree()
    #     return root
