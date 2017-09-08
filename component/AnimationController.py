# coding=utf-8
import time

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class AnimationController(object):
    def __init__(self, anim_time_module='data.animation_data.explorer2_ani',
                 ags_file_name='data/animation_data/explorer2.ags'):
        super(AnimationController, self).__init__()
        self.events = {}
        self.load_anim_events(anim_time_module, ags_file_name)
        self.cur_anim = None
        self.cur_anim_start_time = None
        self.cur_anim_speed_rate = 1.0

    def load_anim_events(self, anim_time_module, ags_file_name):
        """
        读取每个动画中的各个事件的触发时间
        """
        try:
            data_module = __import__(anim_time_module, fromlist=[''])
            anim_time_data = getattr(data_module, 'data', None)
            tree = ET.parse(ags_file_name)
            root = tree.getroot()
            anim_nodes = root[1]
            for anim_node in anim_nodes:
                anim_name = anim_node.tag[len('EventTrack_'):]
                anim_time = anim_time_data[anim_name]
                print anim_name
                for c in anim_node:
                    self.events[c.attrib['Name']] = float(c.attrib['TimeRatio']) * anim_time
        except:
            print 'Error load anim events.'

    def play_anim(self, anim, speed_rate):
        self.cur_anim = anim
        self.cur_anim_speed_rate = speed_rate
        self.cur_anim_start_time = time.time()

    # def register_anim_key_event(self, anim, key, func):
    #     """
    #     注册角色模型动作关键帧回调事件响应函数
    #     """
    #     if self.model is None:
    #         return
    #     self.model.register_anim_key_event(anim, key, func)
    #
    # def un_register_anim_key_event(self, anim, key, func):
    #     """
    #     注册角色模型动作关键帧回调事件响应函数
    #     """
    #     if self.model is None:
    #         return
    #     self.model.unregister_event(func, key, anim)
    #
    # def is_anim_at_end(self):
    #     """
    #     判断动画播放是否结束
    #     """
    #     if not self.model:
    #         return False
    #     return self.model.is_anim_at_end and not self.model.get_anim_ctrl(world.ANIM_TYPE_SKELETAL).anim_loop
    #
    # def stop_animation(self):
    #     """
    #     停止播放当前动画
    #     """
    #     if not self.model:
    #         return
    #     self.model.stop_animation()
    #
    # def pause_animation(self):
    #     """
    #     暂停当前动画播放
    #     """
    #     if not self.model or not self.model.is_playing:
    #         return False
    #     self.is_ani_pause = True
    #     self.last_ani_name = self.model.cur_anim_name
    #     self.last_ani_time = self.model.anim_time
    #     self.model.stop_animation()
    #     return True
    #
    # def resume_animation(self):
    #     # 恢复动画播放
    #     if not self.is_ani_pause or not self.model:
    #         return
    #     self.is_ani_pause = False
    #     # print 'resume'
    #     self.play_animation(self.last_ani_name, init_time=self.last_ani_time)
    #
    # def get_current_ani_name(self):
    #     if not self.model:
    #         return None
    #     return self.model.cur_anim_name
    #
    # def get_ani_time(self, anim_name):
    #     if self.model is None:
    #         return None
    #     return self.model.get_anim_length(anim_name) / 1000.0
    #
    # def is_playing_loop_anim(self):
    #     """
    #     是否正在播放loop动画
    #     """
    #     if self.model and self.model.is_playing and self.model.get_anim_ctrl(world.ANIM_TYPE_SKELETAL).anim_loop:
    #         return True
    #     return False
    #
    # def is_playing_anim(self, ani_name):
    #     return self.model and ani_name == self.model.cur_anim_name and self.model.is_playing
    #
    # def is_playing_any_anim(self):
    #     if self.model and self.model.is_playing:
    #         return True
    #     return False
    #
    #
    # def set_cur_anim(self, anim):
    #     self.cur_anim = anim
    #
    # def get_cur_anim(self):
    #     return self.cur_anim
    #
    # def get_ani_tag_time(self, tag):
    #     """
    #     返回动画中tag的时间
    #     """
    #     return self.events.get(tag)
