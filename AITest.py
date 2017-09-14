
import behavior
from ai.monster_ai import AI_Lib

tree = behavior.BehaviorTree()

tree.load(AI_Lib.ChaseMonster)
blackboard = behavior.Blackboard()

tree.tick({}, blackboard)

kk = 10