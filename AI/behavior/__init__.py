SUCCESS = 1
FAILURE = 2
RUNNING = 3
ERROR = 4

COMPOSITE = 'composite'
DECORATOR = 'decorator'
ACTION = 'action'
CONDITION = 'condition'

# core
from AI.behavior.core.Tick import Tick
from AI.behavior.core.BaseNode import BaseNode
from AI.behavior.core.Action import Action
from AI.behavior.core.Composite import Composite
from AI.behavior.core.Decorator import Decorator
from AI.behavior.core.Condition import Condition
from AI.behavior.core.Blackboard import Blackboard
from AI.behavior.core.BehaviorTree import BehaviorTree

# composites
from AI.behavior.composites.Sequence import Sequence
from AI.behavior.composites.Priority import Priority
from AI.behavior.composites.MemPriority import MemPriority
from AI.behavior.composites.MemSequence import MemSequence

# actions
from AI.behavior.actions.Succeeder import Succeeder
from AI.behavior.actions.Failer import Failer
from AI.behavior.actions.Runner import Runner
from AI.behavior.actions.Error import Error
from AI.behavior.actions.Wait import Wait

# decorators
from AI.behavior.decorators.Inverter import Inverter
from AI.behavior.decorators.Limiter import Limiter
from AI.behavior.decorators.MaxTime import MaxTime
from AI.behavior.decorators.Repeater import Repeater
from AI.behavior.decorators.RepeatUntilFailure import RepeatUntilFailure
from AI.behavior.decorators.RepeatUntilSuccess import RepeatUntilSuccess
