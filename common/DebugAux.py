class DebugAux(object):
    def __init__(self):
        super(DebugAux, self).__init__()

    def Log(self, *args, **kwargs):
        pass
        #print(args, kwargs)


    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(DebugAux, cls).__new__(cls, *args, **kwargs)

        return cls._instance


__debugaux = DebugAux()
Log = __debugaux.Log