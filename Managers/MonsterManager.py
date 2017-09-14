import random
from Configuration import MonsterRefresh
from GameObject.GameObject import GameObject
from common.timer import TimerManager


class MonsterCell(object):
    def __init__(self, ID=-1, num=-1):
        super(MonsterCell, self).__init__()
        self.ID = ID
        self.num = num


class StageCell(object):
    def __init__(self, waiting_time, monster_list, alert_time, interval_time, first_refresh_num, next_refresh_num):
        self.waiting_time = waiting_time
        self.monster_list = monster_list
        self.alert_time = alert_time
        self.interval_time = interval_time
        self.first_refresh_num = first_refresh_num
        self.next_refresh_num = next_refresh_num

        self.sub_stage_num = 0

    def get_sub_stage_monster_number(self):
        if self.sub_stage_num == 0:
            self.sub_stage_num += 1
            return self._get_sub_monster_list(self.first_refresh_num)
        else:
            self.sub_stage_num += 1
            return self._get_sub_monster_list(self.next_refresh_num)

    def _get_sub_monster_list(self, random_num):
        total_num = random.randint(random_num[0], random_num[1])

        ret_list = []

        for monster in self.monster_list:
            val = random.randint(0, min(total_num, monster.num))
            if val != 0:
                monster.num -= val
                total_num -= val
                cell = MonsterCell(monster.ID, val)
                ret_list.append(cell)

        if len(ret_list) > 0:
            return ret_list

        return None


class MonsterManager(GameObject):
    GAME_WIN_LISTENER = 0
    GAME_WIN_COUNT_DOWN_LISTENER = 1

    MONSTER_REMIND_LISTENER = 2
    MONSTER_REMIND_RED_LISTENER = 3
    MONSTER_COMING_LISTENER = 4

    def __init__(self, game_type):
        super(MonsterManager, self).__init__()

        self.game_type = game_type
        self.game_configuration = None
        self.timer_manager = TimerManager()
        self.stage_num = 0
        self.game_start = False
        self.win_timer = None
        self.win_count_down_timer = None

        self._init()

    def _init(self):
        if self.game_type == 1:
            self.game_configuration = MonsterRefresh.normal_model
        elif self.game_type == 2:
            self.game_configuration = MonsterRefresh.battle_model
        elif self.game_type == 0:
            self.game_configuration = MonsterRefresh.single_model
        else:
            raise "[server] [Monster Manager] game type error"

    def tick(self):
        if self.game_start is False:
            return

        self.timer_manager.scheduler()

    def start_game(self):
        self._game_win_setting()
        self._stage_setting()
        self.game_start = True

    def stop_game(self):
        self._game_win_unsetting()
        self.game_start = False

    # ***************************game win*******************begin
    def _game_win_setting(self):
        total_time = self.game_configuration["win_time"]
        remind_time = self.game_configuration["win_remind_time"]

        self.win_timer = self.timer_manager.add_timer(total_time, self._notify_game_win)
        self.win_count_down_timer = self.timer_manager.add_timer(total_time - remind_time,
                                                                 self._notify_game_win_count_down)

    def _game_win_unsetting(self):
        if self.win_timer is not None:
            self.timer_manager.cancel(self.win_timer)
        if self.win_count_down_timer is not None:
            self.timer_manager.cancel(self.win_count_down_timer)

    def _notify_game_win(self):
        self.trigger_event(MonsterManager.GAME_WIN_LISTENER)

    def _notify_game_win_count_down(self):
        self.trigger_event(MonsterManager.GAME_WIN_COUNT_DOWN_LISTENER, self.game_configuration["win_remind_time"])

    # ***************************game win*******************end

    def _stage_setting(self):
        stage = self._get_stage_data(self.stage_num)
        if stage is not None:
            self._each_stage_setting(stage)
        self.stage_num += 1

    def _get_stage_data(self, stage_num):
        if stage_num == 0:
            waiting_time = random.randint(self.game_configuration["first_stage_time"][0],
                                          self.game_configuration["first_stage_time"][1])
        else:
            waiting_time = random.randint(self.game_configuration["next_stage_time"][0],
                                          self.game_configuration["next_stage_time"][1])

        data = self.game_configuration["monster_setting"]
        monster_list = []
        for cell in data:
            arr = cell["total_num"]
            if stage_num < len(arr):
                monster = MonsterCell(cell["ID"], arr[stage_num])
                monster_list.append(monster)

        alert_time = self.game_configuration["alert_time"]
        interval_time = self.game_configuration["interval_time"]
        first_randome_num = self.game_configuration["first_random_num"]
        next_random_num = self.game_configuration["next_random_num"]

        if monster_list is not None:
            return StageCell(waiting_time, monster_list, alert_time,
                             interval_time, first_randome_num, next_random_num)

        return None

    def _each_stage_setting(self, stage):
        self.trigger_event(MonsterManager.MONSTER_REMIND_LISTENER, stage.waiting_time)
        self.timer_manager.add_timer(stage.waiting_time - stage.alert_time
                                     , self._notify_red_alter, stage)
        self.timer_manager.add_timer(stage.waiting_time, self._notify_refresh, stage)
        self.timer_manager.add_timer(stage.waiting_time, self._stage_setting)

    def _notify_refresh(self, stage):

        monster_list = stage.get_sub_stage_monster_number()

        if monster_list is not None:
            self.trigger_event(MonsterManager.MONSTER_COMING_LISTENER, monster_list)
        else:
            return

        refresh_time = random.randint(stage.interval_time[0], stage.interval_time[1])

        self.timer_manager.add_timer(refresh_time, self._notify_refresh, stage)

    def _notify_red_alter(self, stage):
        self.trigger_event(MonsterManager.MONSTER_REMIND_RED_LISTENER, stage.alert_time)
