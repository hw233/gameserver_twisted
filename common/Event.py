# -*- coding: utf-8 -*-
import weakref
import types


def parse_callable(func):
    if isinstance(func, types.FunctionType):  # 全局函数
        return func, None
    elif isinstance(func, types.MethodType):
        if func.im_self:  # 实例方法
            return func.im_func, weakref.ref(func.im_self)  # 使用弱引用可以不增加引用计数
        else:  # 类方法
            return func.im_func, None
    else:
        raise Exception('未知类型')


class Event(object):
    def __init__(self):
        """
		事件(观察者模式)
		"""
        super(Event, self).__init__()
        self.event_handler_list = []

    def clear_observer(self):
        self.event_handler_list = []

    # 返回观察者数量
    def observer_count(self):
        return len(self.event_handler_list)

    def __iadd__(self, handler_tuple):
        """
		增加观察者
		重载 += 运算符
		"""
        self.clear_dead()  # 尝试清理死掉的事件响应函数
        if not isinstance(handler_tuple, tuple):
            handler_tuple = (handler_tuple, None)
        handler = parse_callable(handler_tuple[0])
        for add_handler, param in self.event_handler_list:
            if handler == add_handler:
                return self
        self.event_handler_list.append((handler, handler_tuple[1]))
        return self

    def clear_dead(self):
        """
		删掉死亡的观察者
		"""
        for i in xrange(len(self.event_handler_list) - 1, -1, -1):
            handler_tuple = self.event_handler_list[i]
            handler, wr = handler_tuple[0]
            if wr and not wr():  # 是实例方法,但是观察者已死
                self.event_handler_list.pop(i)

    def __isub__(self, sub_handler):
        """
		减少观察者
		重载 -= 运算符
		"""
        self.clear_dead()  # 尝试清理死掉的事件响应函数
        handler_weak = parse_callable(sub_handler)
        for i in xrange(len(self.event_handler_list) - 1, -1, -1):  # 从后往前pop,才不会有跳跃行为
            handler, func_param = self.event_handler_list[i]
            if handler == handler_weak:
                self.event_handler_list.pop(i)
        return self

    def __call__(self, *t_args, **d_args):
        """
		触发事件
		重载()运算符
		"""
        ret = has_dead = False
        for iIdx, handler_tuple in enumerate(self.event_handler_list):
            handler, wr = handler_tuple[0]
            try:
                if not wr:
                    if handler_tuple[1]:
                        ret = handler(handler_tuple[1], *t_args, **d_args)
                    else:
                        ret = handler(*t_args, **d_args)
                elif wr():
                    if handler_tuple[1]:
                        ret = handler(wr(), handler_tuple[1], *t_args, **d_args)
                    else:
                        ret = handler(wr(), *t_args, **d_args)
                else:
                    has_dead = True
                if ret:  # 本次监听函数中断事件流
                    break
            except Exception:
                print "event call error"
                raise

        if has_dead:
            self.clear_dead()
        return ret
