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


class MsgCSAlive(SimpleHeader):
    def __init__(self):
        super(MsgCSAlive, self).__init__(conf.MSG_CS_ALIVE)
        self.sid = conf.USER_SERVICES
        self.cmdid = 5


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
    def __init__(self, pid=-1, px=0, py=0, pz=0, rx=0, ry=0, rz=0, vx=0, vy=0, vz=0,
                 ax=0, ay=0, az=0, send_time=0, ani_name=''):
        super(MsgCSPlayerMove, self).__init__(conf.MSG_CS_PLAYER_MOVE)
        self.append_param('pid', pid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('rx', rx, 'f')
        self.append_param('ry', ry, 'f')
        self.append_param('rz', rz, 'f')
        self.append_param('vx', vx, 'f')
        self.append_param('vy', vy, 'f')
        self.append_param('vz', vz, 'f')
        self.append_param('ax', ax, 'f')
        self.append_param('ay', ay, 'f')
        self.append_param('az', az, 'f')
        self.append_param('send_time', send_time, 'd')
        self.append_param('ani_name', ani_name, 's')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 1


class MsgCSPlayerAttack(SimpleHeader):
    def __init__(self, pid=-1, px=0, py=0, pz=0, rx=0, ry=0, rz=0):
        super(MsgCSPlayerAttack, self).__init__(conf.MSG_CS_PLAYER_ATTACK)
        self.append_param('pid', pid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('rx', rx, 'f')
        self.append_param('ry', ry, 'f')
        self.append_param('rz', rz, 'f')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 2


class MsgCSPlayerHit(SimpleHeader):
    def __init__(self, pid=-1, px=0, py=0, pz=0, skill_id=0, node_name='', targets_str=''):
        super(MsgCSPlayerHit, self).__init__(conf.MSG_CS_PLAYER_HIT)
        self.append_param('pid', pid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('skill_id', skill_id, 'i')
        self.append_param('node_name', node_name, 's')
        self.append_param('targets_str', targets_str, 's')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 3


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
          
'''


class MsgSCGameObjectDie(SimpleHeader):
    def __init__(self, entity_id):
        super(MsgSCGameObjectDie, self).__init__(conf.MSG_SC_GAME_OBJECT_DIE)
        self.append_param("entity_id", entity_id, 'i')


class MsgCSPlayerCollect(SimpleHeader):
    def __init__(self, pid=-1, pos_x=0, pos_y=0,pos_z=0):
        super(MsgCSPlayerCollect, self).__init__(conf.MSG_CS_PLAYER_COLLECT)
        self.append_param('pid', pid, 'i')
        self.append_param('pos_x', pos_x, 'f')
        self.append_param('pos_y', pos_y, 'f')
        self.append_param('pos_z', pos_z, 'f')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 5


class MsgSCPlayerCollect(SimpleHeader):
    def __init__(self, pid=-1, ID = -1):
        super(MsgSCPlayerCollect, self).__init__(conf.MSG_SC_PLAYER_COLLECT)
        self.append_param('pid', pid, 'i')
        self.append_param("ID", ID , 'i')


class MsgCSPlayerReap(SimpleHeader):
    def __init__(self, pid=-1, pos_x=0, pos_y=0, pos_z=0, item_id=0):
        super(MsgCSPlayerReap, self).__init__(conf.MSG_CS_PLAYER_REAP)
        self.append_param('pid', pid, 'i')
        self.append_param('pos_x', pos_x, 'f')
        self.append_param('pos_y', pos_y, 'f')
        self.append_param('pos_z', pos_z, 'f')
        self.append_param('item_id', item_id, 'i')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 8


class MsgSCMapItemDestroy(SimpleHeader):
    def __init__(self, ID = -1):
        super(MsgSCMapItemDestroy, self).__init__(conf.MSG_SC_MAP_ITEM_DESTROY)
        self.append_param("ID", ID, "i")
        

class MsgSCPlayerLeave(SimpleHeader):
    def __init__(self, pid = -1):
        super(MsgSCPlayerLeave, self).__init__(conf.MSG_SC_PLAYER_LEAVE)
        self.append_param("pid", pid, "i")


'''********************************BackpackMessage*******************************************************'''


class MsgSCBackpackSyn(SimpleHeader):
    def __init__(self, format="", data = ""):
        super(MsgSCBackpackSyn, self).__init__(conf.MSG_SC_BACKPACK_SYN)
        self.append_param("format", format, "s")
        self.append_param("data", data, "s")


class MsgCSMakeRequest(SimpleHeader):
    def __init__(self, pid = -1, ID = -1, num = 1):
        super(MsgCSMakeRequest, self).__init__(conf.MSG_CS_MAKE_REQUEST)
        self.append_param("pid",pid, 'i')
        self.append_param("ID", ID, 'i')
        self.append_param("num", num, 'i')


class MsgCSArmorInstall(SimpleHeader):
    def __init__(self, pid = -1, entity_id = -1):
        super(MsgCSArmorInstall, self).__init__(conf.MSG_CS_ARMOR_INSTALL)
        self.append_param("pid", pid, 'i')
        self.append_param("entity_id", entity_id, 'i')


class MsgCSWeaponInstall(SimpleHeader):
    def __init__(self, pid=-1, entity_id=-1, slot_index = -1):
        super(MsgCSWeaponInstall, self).__init__(conf.MSG_CS_WEAPON_INSTALL)
        self.append_param("pid", pid, 'i')
        self.append_param("entity_id", entity_id, 'i')
        self.append_param("slot_index", slot_index, 'i')


class MsgCSHatInstall(SimpleHeader):
    def __init__(self, pid=-1, entity_id=-1):
        super(MsgCSHatInstall, self).__init__(conf.MSG_CS_HAT_INSTALL)
        self.append_param("pid", pid, 'i')
        self.append_param("entity_id", entity_id, 'i')


class MsgCSWeaponUninstall(SimpleHeader):
    def __init__(self, pid=-1, entity_id=-1):
        super(MsgCSWeaponUninstall, self).__init__(conf.MSG_CS_WEAPON_UNINSTALL)
        self.append_param("pid", pid, 'i')
        self.append_param("entity_id", entity_id, 'i')


class MsgSCWeaponInstall(SimpleHeader):
    def __init__(self, pid=-1, ID=-1):
        super(MsgSCWeaponInstall, self).__init__(conf.MSG_SC_WEAPON_INSTALL)
        self.append_param("pid", pid, 'i')
        self.append_param("ID", ID, 'i')


class MsgSCWeaponUninstall(SimpleHeader):
    def __init__(self, pid=-1, ID = -1):
        super(MsgSCWeaponUninstall, self).__init__(conf.MSG_SC_WEAPON_UNINSTALL)
        self.append_param("pid", pid, 'i')
        self.append_param("ID", ID, 'i')


class MsgCSPlayerDrop(SimpleHeader):
    def __init__(self, pid=-1, entity_id = -1, x=0, y=0, z=0):
        super(MsgCSPlayerDrop, self).__init__(conf.MSG_CS_PLAYER_DROP)
        self.append_param("pid", pid, 'i')
        self.append_param("entity_id", entity_id, 'i')
        self.append_param("x", x, 'f')
        self.append_param("y", y, 'f')
        self.append_param("z", z, 'f')


class MsgCSWeaponActive(SimpleHeader):
    def __init__(self, pid=-1, entity_id=-1):
        super(MsgCSWeaponActive, self).__init__(conf.MSG_CS_WEAPON_ACTIVE)
        self.append_param("pid", pid, 'i')
        self.append_param("entity_id", entity_id, 'i')
'''********************************BackpackMessage*******************************************************'''
