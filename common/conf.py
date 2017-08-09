# -*- coding: GBK -*-

DB_NAME = "UserData.db"

# message
MSG_SC_LOGIN_RESULT = 1001
MSG_CS_REGISTER = 2001
MSG_CS_LOGIN = 2002
MSG_CS_LOGOUT = 2003
MSG_CS_MATCH_REQUEST = 2004
MSG_CS_MATCH_CANCEL = 2005
MSG_SC_ROOMMATE_ADD = 1008
MSG_SC_ROOMMATE_DEL = 1009
MSG_SC_MAP_LOAD = 1010   # notify clients loading map.
MSG_CS_LOAD_FINISHED = 2007  # client notify server load finished

# room & arena
MSG_SC_START_GAME = 1002

# player
MSG_SC_PLAYER_BORN = 1004
MSG_CS_PLAYER_MOVE = 2006

# entities
MSG_SC_ENTITY_BORN = 1005

# game
MSG_SC_GAME_WIN = 1006
MSG_SC_GAME_OVER = 1007

# service id
USER_SERVICES = 1
ARENA_SERVICES = 2

NET_STATE_STOP = 0				# state: init value
NET_STATE_CONNECTING = 1		# state: connecting
NET_STATE_ESTABLISHED = 2		# state: connected

NET_HEAD_LENGTH_SIZE = 4		# 4 bytes little endian (x86)
NET_HEAD_LENGTH_FORMAT = '<I'

NET_CONNECTION_NEW = 0  # new connection
NET_CONNECTION_LEAVE = 1  # lost connection
NET_CONNECTION_DATA = 2  # data comming

NET_HOST_DEFAULT_TIMEOUT = 70

MAX_HOST_CLIENTS_INDEX = 0xffff
MAX_HOST_CLIENTS_BYTES = 16


