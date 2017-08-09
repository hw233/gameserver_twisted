'''
   @describe:
             InputBase
'''



class InputBase(object):
    def __init__(self):
        super(InputBase, self).__init__()


class MovementInput(InputBase):
    def __init__(self):
        super(MovementInput, self).__init__()



class PlayerOperation(object):
    def __init__(self, data):
        super(PlayerOperation, self).__init__()
        self.data = data