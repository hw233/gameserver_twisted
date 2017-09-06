class DebugAux(object):
    def __init__(self):
        super(DebugAux, self).__init__()

    def Log(self, *args):
        print(args)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls._instance = super(DebugAux, cls).__new__(cls, *args, **kwargs)

        return cls._instance


__debugaux = DebugAux()
Log = __debugaux.Log