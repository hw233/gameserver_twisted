# -*- coding: GBK -*-
import conf
from header import SimpleHeader


class MsgCSLoginGuest(SimpleHeader):
    def __init__(self, uuid=""):
        super(MsgCSLoginGuest, self).__init__(conf.MSG_CS_LOGIN_GUEST)
        self.append_param('uuid', uuid, 's')


class MsgSCLoginGuestResult(SimpleHeader):
    def __init__(self, uuid=""):
        super(MsgSCLoginGuestResult, self).__init__(conf.MSG_SC_LOGIN_GUEST_RESULT)
        self.append_param('uuid', uuid, 's')


class MsgSCMapLoad(SimpleHeader):
    # notify clients load universe
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
    SINGLE_MATCH = 0
    NORMAL_MATCH = 1
    BATTLE_MATCH = 2

    def __init__(self, match_type=1):
        super(MsgCSMatchRequest, self).__init__(conf.MSG_CS_MATCH_REQUEST)
        self.append_param("match_type", match_type, 'i')  # 0 单人模式， 1 一般模式，2 竞技模式
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


class MsgSCGameWinCountDown(SimpleHeader):
    def __init__(self, remind_time=0):
        super(MsgSCGameWinCountDown, self).__init__(conf.MSG_SC_GAME_WIN_COUNT_DOWN)
        self.append_param("remind_time", remind_time, 'i')


class MsgCSPlayerQuit(SimpleHeader):
    def __init__(self, pid=-1):
        super(MsgCSPlayerQuit, self).__init__(conf.MSG_CS_PLAYER_QUIT)
        self.append_param('pid', pid, 'i')


class MsgSCPlayerBorn(SimpleHeader):
    def __init__(self, pid=-1, ptype=0, name='', health=0, px=0, py=0, pz=0,
                 rx=0, ry=0, rz=0, role_id=0, group_id=0):
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
        self.append_param('role_id', role_id, 'i')  # prefab id
        self.append_param('group_id', group_id, 'i')


class MsgCSPlayerMove(SimpleHeader):
    def __init__(self, pid=-1, px=0, py=0, pz=0, rx=0, ry=0, rz=0, vx=0, vy=0, vz=0,
                 ax=0, ay=0, az=0, state_names=''):
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
        self.append_param('state_names', state_names, 's')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 1


class MsgCSPlayerPosition(SimpleHeader):
    def __init__(self, pid=-1, px=0, pz=0, ry=0, is_moving=False):
        super(MsgCSPlayerPosition, self).__init__(conf.MSG_CS_PLAYER_POSITION)
        self.append_param('pid', pid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('ry', ry, 'f')
        self.append_param('is_moving', is_moving, '?')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 11


class MsgCSPlayerAttack(SimpleHeader):
    def __init__(self, pid=-1, button_down=True, px=0, py=0, pz=0, rx=0, ry=0, rz=0):
        super(MsgCSPlayerAttack, self).__init__(conf.MSG_CS_PLAYER_ATTACK)
        self.append_param('pid', pid, 'i')
        self.append_param('button_down', button_down, '?')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('rx', rx, 'f')
        self.append_param('ry', ry, 'f')
        self.append_param('rz', rz, 'f')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 2


class MsgCSPlayerRunActNode(SimpleHeader):
    def __init__(self, pid=-1, skill_id=0, node_name=''):
        super(MsgCSPlayerRunActNode, self).__init__(conf.MSG_CS_PLAYER_RUN_ACT_NODE)
        self.append_param('pid', pid, 'i')
        self.append_param('skill_id', skill_id, 'i')
        self.append_param('node_name', node_name, 's')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 12


class MsgCSPlayerHitRecover(SimpleHeader):
    def __init__(self, pid=-1, is_lie_down=False):
        super(MsgCSPlayerHitRecover, self).__init__(conf.MSG_CS_PLAYER_HIT_RECOVER)
        self.append_param('pid', pid, 'i')
        self.append_param('is_lie_down', is_lie_down, '?')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 13


class MsgCSPlayerHit(SimpleHeader):
    def __init__(self, pid=-1, px=0, py=0, pz=0, rx=0, ry=0, rz=0, skill_id=0, node_name=''):
        super(MsgCSPlayerHit, self).__init__(conf.MSG_CS_PLAYER_HIT)
        self.append_param('pid', pid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('rx', rx, 'f')
        self.append_param('ry', ry, 'f')
        self.append_param('rz', rz, 'f')
        self.append_param('skill_id', skill_id, 'i')
        self.append_param('node_name', node_name, 's')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 3


class MsgSCPlayerHit(SimpleHeader):
    def __init__(self, pid=-1, px=0, py=0, pz=0, rx=0, ry=0, rz=0, skill_id=0, node_name='', tag='', hit_idx=0,
                 targets_str=''):
        super(MsgSCPlayerHit, self).__init__(conf.MSG_SC_PLAYER_HIT)
        self.append_param('pid', pid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('rx', rx, 'f')
        self.append_param('ry', ry, 'f')
        self.append_param('rz', rz, 'f')
        self.append_param('skill_id', skill_id, 'i')
        self.append_param('node_name', node_name, 's')
        self.append_param('tag', tag, 's')
        self.append_param('hit_idx', hit_idx, 'i')
        self.append_param('targets_str', targets_str, 's')


class MsgCSPlayerDefend(SimpleHeader):
    def __init__(self, pid=-1, px=0, py=0, pz=0, rx=0, ry=0, rz=0):
        super(MsgCSPlayerDefend, self).__init__(conf.MSG_CS_PLAYER_DEFEND)
        self.append_param('pid', pid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('rx', rx, 'f')
        self.append_param('ry', ry, 'f')
        self.append_param('rz', rz, 'f')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 4


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
    def __init__(self, pid=-1, pos_x=0, pos_y=0, pos_z=0):
        super(MsgCSPlayerCollect, self).__init__(conf.MSG_CS_PLAYER_COLLECT)
        self.append_param('pid', pid, 'i')
        self.append_param('pos_x', pos_x, 'f')
        self.append_param('pos_y', pos_y, 'f')
        self.append_param('pos_z', pos_z, 'f')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 5


class MsgSCPlayerCollect(SimpleHeader):
    def __init__(self, pid=-1):
        super(MsgSCPlayerCollect, self).__init__(conf.MSG_SC_PLAYER_COLLECT)
        self.append_param('pid', pid, 'i')


class MsgCSPlayerReap(SimpleHeader):
    def __init__(self, pid=-1, button_down=True, pos_x=0, pos_y=0, pos_z=0, entity_id=0):
        super(MsgCSPlayerReap, self).__init__(conf.MSG_CS_PLAYER_REAP)
        self.append_param('pid', pid, 'i')
        self.append_param('button_down', button_down, '?')
        self.append_param('pos_x', pos_x, 'f')
        self.append_param('pos_y', pos_y, 'f')
        self.append_param('pos_z', pos_z, 'f')
        self.append_param('entity_id', entity_id, 'i')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 8


class MsgCSPlayerReapHit(SimpleHeader):
    def __init__(self, pid=-1, pos_x=0, pos_y=0, pos_z=0, entity_id=0, blood_percent=0, power_percent=0,
                 attack_percent=0):
        super(MsgCSPlayerReapHit, self).__init__(conf.MSG_CS_PLAYER_REAP_HIT)
        self.append_param('pid', pid, 'i')
        self.append_param('pos_x', pos_x, 'f')
        self.append_param('pos_y', pos_y, 'f')
        self.append_param('pos_z', pos_z, 'f')
        self.append_param('entity_id', entity_id, 'i')
        self.append_param('blood_percent', blood_percent, 'f')
        self.append_param('power_percent', power_percent, 'f')
        self.append_param('attack_percent', attack_percent, 'f')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 9


class MsgCSBulletSpawn(SimpleHeader):
    def __init__(self, pid=-1, px=0, py=0, pz=0, dx=0, dy=0, dz=0, skill_id=0, node_name=''):
        super(MsgCSBulletSpawn, self).__init__(conf.MSG_CS_BULLET_SPAWN)
        self.append_param('pid', pid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('dx', dx, 'f')
        self.append_param('dy', dy, 'f')
        self.append_param('dz', dz, 'f')
        self.append_param('skill_id', skill_id, 'i')
        self.append_param('node_name', node_name, 's')
        self.sid = conf.ARENA_SERVICES
        self.cmdid = 10


class MsgSCBulletSpawn(SimpleHeader):
    def __init__(self, pid=-1, owner_id=-1, px=0, py=0, pz=0, vx=0, vy=0, vz=0, ax=0, ay=0, az=0, skill_id=0,
                 node_name=''):
        super(MsgSCBulletSpawn, self).__init__(conf.MSG_SC_BULLET_SPAWN)
        self.append_param('pid', pid, 'i')
        self.append_param('owner_id', owner_id, 'i')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('vx', vx, 'f')
        self.append_param('vy', vy, 'f')
        self.append_param('vz', vz, 'f')
        self.append_param('ax', ax, 'f')
        self.append_param('ay', ay, 'f')
        self.append_param('az', az, 'f')
        self.append_param('skill_id', skill_id, 'i')
        self.append_param('node_name', node_name, 's')


# class MsgSCBulletMove(SimpleHeader):
#     def __init__(self, pid=-1, px=0, py=0, pz=0):
#         super(MsgSCBulletMove, self).__init__(conf.MSG_SC_BULLET_MOVE)
#         self.append_param('pid', pid, 'i')
#         self.append_param('px', px, 'f')
#         self.append_param('py', py, 'f')
#         self.append_param('pz', pz, 'f')


class MsgSCBulletHit(SimpleHeader):
    def __init__(self, pid=-1, px=0, py=0, pz=0, targets_str=''):
        super(MsgSCBulletHit, self).__init__(conf.MSG_SC_BULLET_HIT)
        self.append_param('pid', pid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('py', py, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('targets_str', targets_str, 's')


class MsgSCPlayerReapHit(SimpleHeader):
    def __init__(self, pid=-1, health=0, spirit=0):
        super(MsgSCPlayerReapHit, self).__init__(conf.MSG_SC_PLAYER_REAP_HIT)
        self.append_param('pid', pid, 'i')
        self.append_param('health', health, 'i')
        self.append_param('spirit', spirit, 'i')


class MsgSCMapItemDrop(SimpleHeader):
    def __init__(self, x=0, y=0, z=0, ID=-1):
        super(MsgSCMapItemDrop, self).__init__(conf.MSG_SC_MAP_ITEM_DROP)
        self.append_param('x', x, 'f')
        self.append_param('y', y, 'f')
        self.append_param('z', z, 'f')
        self.append_param("ID", ID, 'i')


class MsgSCMapItemDestroy(SimpleHeader):
    def __init__(self, ID=-1):
        super(MsgSCMapItemDestroy, self).__init__(conf.MSG_SC_MAP_ITEM_DESTROY)
        self.append_param("ID", ID, "i")


class MsgSCPlayerLeave(SimpleHeader):
    def __init__(self, pid=-1):
        super(MsgSCPlayerLeave, self).__init__(conf.MSG_SC_PLAYER_LEAVE)
        self.append_param("pid", pid, "i")


'''********************************BackpackMessage*******************************************************'''


class MsgSCBackpackSyn(SimpleHeader):
    def __init__(self, format="", data=""):
        super(MsgSCBackpackSyn, self).__init__(conf.MSG_SC_BACKPACK_SYN)
        self.append_param("format", format, "s")
        self.append_param("data", data, "s")


class MsgCSMakeRequest(SimpleHeader):
    def __init__(self, pid=-1, ID=-1, num=1):
        super(MsgCSMakeRequest, self).__init__(conf.MSG_CS_MAKE_REQUEST)
        self.append_param("pid", pid, 'i')
        self.append_param("ID", ID, 'i')
        self.append_param("num", num, 'i')


class MsgCSArmorInstall(SimpleHeader):
    def __init__(self, pid=-1, entity_id=-1):
        super(MsgCSArmorInstall, self).__init__(conf.MSG_CS_ARMOR_INSTALL)
        self.append_param("pid", pid, 'i')
        self.append_param("entity_id", entity_id, 'i')


class MsgCSWeaponInstall(SimpleHeader):
    def __init__(self, pid=-1, entity_id=-1, slot_index=-1):
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
    def __init__(self, pid=-1, ID=-1):
        super(MsgSCWeaponUninstall, self).__init__(conf.MSG_SC_WEAPON_UNINSTALL)
        self.append_param("pid", pid, 'i')
        self.append_param("ID", ID, 'i')


class MsgCSPlayerDrop(SimpleHeader):
    def __init__(self, pid=-1, entity_id=-1, x=0, y=0, z=0):
        super(MsgCSPlayerDrop, self).__init__(conf.MSG_CS_PLAYER_DROP)
        self.append_param("pid", pid, 'i')
        self.append_param("entity_id", entity_id, 'i')
        self.append_param("x", x, 'f')
        self.append_param("y", y, 'f')
        self.append_param("z", z, 'f')


class MsgCSWeaponActive(SimpleHeader):
    def __init__(self, pid=-1, entity_id=-1, action=0):
        super(MsgCSWeaponActive, self).__init__(conf.MSG_CS_WEAPON_ACTIVE)
        self.append_param("pid", pid, 'i')
        self.append_param("entity_id", entity_id, 'i')
        self.append_param("action", action, 'i')  # if action 0 deactive 1 active


class MsgCSGMBPCmd(SimpleHeader):
    def __init__(self, pid=-1, ID=-1, num=1):
        super(MsgCSGMBPCmd, self).__init__(conf.MSG_CS_GM_BP_CMD)
        self.append_param("pid", pid, 'i')
        self.append_param("ID", ID, 'i')
        self.append_param("num", num, 'i')


class MsgCSGMRoomCmd(SimpleHeader):
    def __init__(self, num=1):
        super(MsgCSGMRoomCmd, self).__init__(conf.MSG_CS_GM_ROOM_CMD)
        self.append_param("num", num, "i")


class MsgSCSpiritSyn(SimpleHeader):
    def __init__(self, pid=-1, spirit=0):
        super(MsgSCSpiritSyn, self).__init__(conf.MSG_SC_SPIRIT_SYN)
        self.append_param("pid", pid, 'i')
        self.append_param("spirit", spirit, 'i')


class MsgCSEatFood(SimpleHeader):
    def __init__(self, pid=-1, entity_id=-1):
        super(MsgCSEatFood, self).__init__(conf.MSG_CS_EAT_FOOD)
        self.append_param("pid", pid, 'i')
        self.append_param("entity_id", entity_id, 'i')


class MsgSCWeaponDeduce(SimpleHeader):
    def __init__(self, pid=-1, weapon=-1, armor=-1, hat=-1):
        '''
        :param pid: player id
        :param entity_id: weapon id
        :param num: weapon blood or weapon quantity
        '''
        super(MsgSCWeaponDeduce, self).__init__(conf.MSG_SC_WEAPON_DEDUCE)
        self.append_param("pid", pid, 'i')
        self.append_param("weapon", weapon, 'i')
        self.append_param("armor", armor, 'i')
        self.append_param("hat", hat, 'i')


class MsgSCSpiritBloodSyn(SimpleHeader):
    def __init__(self, pid=-1, spirit=0, blood=0):
        super(MsgSCSpiritBloodSyn, self).__init__(conf.MSG_SC_SPIRIT_BLOOD_SYN)
        self.append_param('pid', pid, 'i')
        self.append_param('spirit', spirit, 'i')
        self.append_param('blood', blood, 'i')


class MsgSCBackpackAdd(SimpleHeader):
    def __init__(self, pid=-1, entity_id=-1, health=-1, ID=-1, num=-1):
        super(MsgSCBackpackAdd, self).__init__(conf.MSG_SC_BACKPACK_ADD)
        self.append_param('pid', pid, 'i')
        self.append_param('entity_id', entity_id, 'i')
        self.append_param('ID', ID, 'i')
        self.append_param('health', health, 'i')
        self.append_param('num', num, 'i')


class MsgSCBackpackDel(SimpleHeader):
    def __init__(self, pid=-1, entity_id=-1, health=-1, ID=-1, num=-1):
        super(MsgSCBackpackDel, self).__init__(conf.MSG_SC_BACKPACK_DEL)
        self.append_param('pid', pid, 'i')
        self.append_param('entity_id', entity_id, 'i')
        self.append_param('ID', ID, 'i')
        self.append_param('health', health, 'i')
        self.append_param('num', num, 'i')


'''********************************BackpackMessage*******************************************************'''

'''***********************************Monster message *****************************************************'''


class MsgSCMonsterBorn(SimpleHeader):
    def __init__(self, entity_id=-1, ID=-1, health=-1, x=0, y=0, z=0, group_id=0):
        super(MsgSCMonsterBorn, self).__init__(conf.MSG_SC_MONSTER_BORN_MSG)
        self.append_param("entity_id", entity_id, 'i')
        self.append_param("ID", ID, 'i')
        self.append_param("health", health, 'i')
        self.append_param("x", x, 'f')
        self.append_param("y", y, 'f')
        self.append_param("z", z, 'f')
        self.append_param('group_id', group_id, 'i')


class MsgSCMonsterMove(SimpleHeader):
    def __init__(self, mid=-1, px=0, pz=0, ry=0, vx=0, vz=0, ax=0, az=0):
        super(MsgSCMonsterMove, self).__init__(conf.MSG_SC_MONSTER_MOVE)
        self.append_param('mid', mid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('ry', ry, 'f')
        self.append_param('vx', vx, 'f')
        self.append_param('vz', vz, 'f')
        self.append_param('ax', ax, 'f')
        self.append_param('az', az, 'f')


class MsgSCMonsterAttack(SimpleHeader):
    def __init__(self, mid=-1, px=0, pz=0, ry=0, skill_id=0):
        super(MsgSCMonsterAttack, self).__init__(conf.MSG_SC_MONSTER_ATTACK)
        self.append_param('mid', mid, 'i')
        self.append_param('px', px, 'f')
        self.append_param('pz', pz, 'f')
        self.append_param('ry', ry, 'f')
        self.append_param('skill_id', skill_id, 'i')


class MsgSCMonsterWaitTime(SimpleHeader):
    def __init__(self, wait_time=0):
        super(MsgSCMonsterWaitTime, self).__init__(conf.MSG_SC_MONSTER_WAITING_TIME)
        self.append_param("wait_time", wait_time, 'i')


class MsgSCMonsterAlertTime(SimpleHeader):
    def __init__(self, alert_time=0):
        super(MsgSCMonsterAlertTime, self).__init__(conf.MSG_SC_MONSTER_ALERT_TIME)
        self.append_param("alert_time", alert_time, 'i')


class MsgSCMonsterStateSyn(SimpleHeader):
    MONSTER_PATROL = 0
    MONSTER_DIE = 1
    MONSTER_ATTACK = 2
    MONSTER_IDLE = 3
    MONSTER_CHASE = 4
    MONSTER_BEATEN = 5

    def __init__(self, entity_id=-1, state=-1, x=0, y=0, z=0, target_id=-1):
        super(MsgSCMonsterStateSyn, self).__init__(conf.MSG_SC_MONSTER_STATE_SYN)
        self.append_param("entity_id", entity_id, 'i')
        self.append_param("state", state, 'i')
        self.append_param('x', x, 'f')
        self.append_param('y', y, 'f')
        self.append_param('z', z, 'f')
        self.append_param("target_id", target_id, 'i')


'''***********************************Monster message *****************************************************'''

'''******************************************QA message***************************************************'''


class MsgSCDelayQA(SimpleHeader):
    def __init__(self, hid=-1, send_time=0.0, back_time=0.0):
        super(MsgSCDelayQA, self).__init__(conf.MSG_SC_DELAY_QA)
        self.append_param('hid', hid, 'i')
        self.append_param('send_time', send_time, 'f')
        self.append_param('back_time', back_time, 'f')


'''******************************************QA message***************************************************'''
