# -*- coding: GBK -*-
import conf
from header import SimpleHeader


class MsgSCMapLoad(SimpleHeader):
    # notify clients load map
    def __init__(self, seed):
        super(MsgSCMapLoad, self).__init__(conf.MSG_SC_MAP_LOAD)
        self.append_param('seed', seed, 'i')


class MsgCSLoadFinished(SimpleHeader):
    def __init__(self):
        super(MsgCSLoadFinished, self).__init__(conf.MSG_CS_LOAD_FINISHED)
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 0


class MsgSCLoginResult(SimpleHeader):
    def __init__(self, ok=0, message=''):
        super(MsgSCLoginResult, self).__init__(conf.MSG_SC_LOGIN_RESULT)
        # if ok = 0 normal login
        # if ok = 1 user in an arena already
        # if ok = 2 user login already
        # if ok = -1 error
        self.append_param('ok', ok, 'i')
        self.append_param('message', message, 's')


class MsgCSRegister(SimpleHeader):
    def __init__(self, username='', password=''):
        super(MsgCSRegister, self).__init__(conf.MSG_CS_REGISTER)
        self.append_param('username', username, 's')
        self.append_param('password', password, 's')
        self.sid = conf.USER_SERVICES
        self.cmdid = 0


class MsgCSMatchRequest(SimpleHeader):
    def __init__(self):
        super(MsgCSMatchRequest, self).__init__(conf.MSG_CS_MATCH_REQUEST)
        self.sid = conf.USER_SERVICES
        self.cmdid = 3


class MsgCSMatchCancel(SimpleHeader):
    def __init__(self):
        super(MsgCSMatchCancel, self).__init__(conf.MSG_CS_MATCH_CANCEL)
        self.sid = conf.USER_SERVICES
        self.cmdid = 4


class MsgCSLogin(SimpleHeader):
    def __init__(self, username='', password=''):
        super(MsgCSLogin, self).__init__(conf.MSG_CS_LOGIN)
        self.append_param('username', username, 's')
        self.append_param('password', password, 's')
        self.sid = conf.USER_SERVICES
        self.cmdid = 1


class MsgCSLogout(SimpleHeader):
    def __init__(self, client_id=-1):
        super(MsgCSLogout, self).__init__(conf.MSG_CS_LOGOUT)
        self.append_param('client_id', client_id, 'i')
        self.sid = conf.USER_SERVICES
        self.cmdid = 2


class MsgSCStartGame(SimpleHeader):
    def __init__(self):
        super(MsgSCStartGame, self).__init__(conf.MSG_SC_START_GAME)


class MsgSCPlayerBorn(SimpleHeader):
    '''
        @describe:
                  player born message
        @log:
             1. add role_id. very player may load diff role
    '''

    def __init__(self, pid, ptype, name, health, px, py, pz, rx, ry, rz, role_id=0):
        super(MsgSCPlayerBorn, self).__init__(conf.MSG_SC_PLAYER_BORN)
        self.append_param('pid', pid, 'i')
        self.append_param('ptype', ptype, 'i')  # ptype: 0->myself, 1->others
        self.append_param('name', name, 's')
        self.append_param('health', health, 'i')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('rx', rx, 'f')
        self.append_param('ry', ry, 'f')
        self.append_param('rz', rz, 'f')
        self.append_param('role_id', role_id, 'i') # prefab id


class MsgCSPlayerMove(SimpleHeader):
    def __init__(self, pid=-1, px=0, py=0, pz=0):
        super(MsgCSPlayerMove, self).__init__(conf.MSG_CS_PLAYER_MOVE)
        self.append_param('pid', pid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 1


class MsgCSPlayerIdle(SimpleHeader):
    def __init__(self, pid=-1, px=0, py=0, pz=0):
        super(MsgCSPlayerIdle, self).__init__(conf.MSG_CS_PLAYER_IDLE)
        self.append_param('pid', pid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 2


class MsgCSPlayerAttack(SimpleHeader):
    def __init__(self, pid=-1):
        super(MsgCSPlayerAttack, self).__init__(conf.MSG_CS_PLAYER_ATTACK)
        self.append_param('pid', pid, 'i')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 3


class MsgCSPlayerHit(SimpleHeader):
    def __init__(self, pid=-1, fx=0, fy=0, fz=0, face_to=0):
        super(MsgCSPlayerHit, self).__init__(conf.MSG_CS_PLAYER_HIT)
        self.append_param('pid', pid, 'i')
        self.append_param('fx', fx, 'f')
        self.append_param('fy', fy, 'f')
        self.append_param('fz', fz, 'f')
        self.append_param('face_to', face_to, 'f')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 4


class MsgCSPlayerCollect(SimpleHeader):
    def __init__(self, pid=-1, seller_id= -1, target_id = -1):
        super(MsgCSPlayerCollect, self).__init__(conf.MSG_CS_PLAYER_COLLECT)
        self.append_param('pid', pid, 'i')
        self.append_param('seller_id', seller_id, 'i')
        self.append_param('target_id', target_id, 'i')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 5


class MsgSCGameWin(SimpleHeader):
    def __init__(self):
        super(MsgSCGameWin, self).__init__(conf.MSG_SC_GAME_WIN)


class MsgSCGameOver(SimpleHeader):
    def __init__(self):
        super(MsgSCGameOver, self).__init__(conf.MSG_SC_GAME_OVER)


class MsgSCRoommateAdd(SimpleHeader):
    def __init__(self, username=''):
        super(MsgSCRoommateAdd, self).__init__(conf.MSG_SC_ROOMMATE_ADD)
        self.append_param("username", username, 's')


class MsgSCRoommateDel(SimpleHeader):
    def __init__(self, username):
        super(MsgSCRoommateDel, self).__init__(conf.MSG_SC_ROOMMATE_DEL)
        self.append_param("username", username, 's')


'''
@describe:
          如果有单位死亡，服务器广播死亡消息
'''


class MsgSCGameObjectDie(SimpleHeader):
    def __init__(self, entity_id):
        super(MsgSCGameObjectDie, self).__init__(conf.MSG_SC_GAME_OBJECT_DIE)
        self.append_param("entity_id", entity_id, 'i')

'''
@describe:
           player drop backpack object to the ground
'''


class MsgCSPlayerDrop(SimpleHeader):
    def __init__(self, pid=-1, ID = -1, num = 0, posx = 0 ,posy = 0):
        super(MsgCSPlayerDrop, self).__init__(conf.MSG_CS_PLAYER_DROP)
        self.append_param("pid", pid, 'i')
        self.append_param("ID", ID, 'i')
        self.append_param("num", num, 'i')
        self.append_param("pos_x", posx, 'f')
        self.append_param("pos_y", posy, 'f')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 6

