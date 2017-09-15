# coding=utf-8
def _normalize_rect(rect):
    x1, y1, x2, y2 = rect
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    return (x1, y1, x2, y2)


def _loop_all_children(parent):
    for child in parent.children:
        if child.children:
            for sub_child in _loop_all_children(child):
                yield sub_child
        yield child


class _QuadNode(object):
    def __init__(self, item, rect):
        self.item = item
        self.rect = rect

    def __eq__(self, other):
        return self.item == other.item and self.rect == other.rect

    def __hash__(self):
        return hash(self.item)


class _QuadTree(object):
    def __init__(self, x, y, width, height, max_items, max_depth, _depth=0):
        '''
         :param x: 中心点x
         :param y: 中心点y
         :param width: 宽度
         :param height: 高度
         :param max_items: 包围盒内最多含有的元素
         :param max_depth: 最大深度
         '''
        self.nodes = []
        self.children = []
        self.center = (x, y)
        self.width, self.height = width, height
        self.max_items = max_items
        self.max_depth = max_depth
        self._depth = _depth

    def __iter__(self):
        for child in _loop_all_children(self):
            yield child

    def insert(self, item, bounding):
        '''
        插入元素
        :param item: 需要插入的元素
        :param bounding: 包围盒
        '''
        rect = _normalize_rect(bounding)
        if len(self.children) == 0:
            node = _QuadNode(item, rect)
            self.nodes.append(node)

            if len(self.nodes) > self.max_items and self._depth < self.max_depth:
                self._split()
        else:
            self._insert_into_children(item, rect)

    def remove(self, item, bounding):
        '''
        删除元素
        :param item: 需要删除的元素
        :param bounding: 包围盒
        '''
        rect = _normalize_rect(bounding)
        if len(self.children) == 0:
            node = _QuadNode(item, rect)
            self.nodes.remove(node)
        else:
            self._remove_from_children(item, rect)

    def intersect(self, rect, results=None):
        '''
        获取指定包围盒内的元素
        :param bounding: 包围盒
        :return: 包围盒内的元素
        '''
        if results is None:
            rect = _normalize_rect(rect)
            results = set()
        # search children
        if self.children:
            if rect[0] <= self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[0].intersect(rect, results)
                if rect[3] >= self.center[1]:
                    self.children[1].intersect(rect, results)
            if rect[2] >= self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[2].intersect(rect, results)
                if rect[3] >= self.center[1]:
                    self.children[3].intersect(rect, results)
        # search node at this level
        for node in self.nodes:
            if (node.rect[2] >= rect[0] and node.rect[0] <= rect[2] and
                node.rect[3] >= rect[1] and node.rect[1] <= rect[3]):
                results.add(node.item)
        return results

    def _insert_into_children(self, item, rect):
        # if rect spans center then insert here
        if (rect[0] <= self.center[0] and rect[2] >= self.center[0] and
            rect[1] <= self.center[1] and rect[3] >= self.center[1]):
            node = _QuadNode(item, rect)
            self.nodes.append(node)
        else:
            # try to insert into children
            if rect[0] <= self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[0]._insert(item, rect)
                if rect[3] >= self.center[1]:
                    self.children[1]._insert(item, rect)
            if rect[2] > self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[2]._insert(item, rect)
                if rect[3] >= self.center[1]:
                    self.children[3]._insert(item, rect)

    def _remove_from_children(self, item, rect):
        # if rect spans center then insert here
        if (rect[0] <= self.center[0] and rect[2] >= self.center[0] and
            rect[1] <= self.center[1] and rect[3] >= self.center[1]):
            node = _QuadNode(item, rect)
            self.nodes.remove(node)
        else:
            # try to remove from children
            if rect[0] <= self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[0]._remove(item, rect)
                if rect[3] >= self.center[1]:
                    self.children[1]._remove(item, rect)
            if rect[2] > self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[2]._remove(item, rect)
                if rect[3] >= self.center[1]:
                    self.children[3]._remove(item, rect)

    def _split(self):
        quartwidth = self.width / 4.0
        quartheight = self.height / 4.0
        halfwidth = self.width / 2.0
        halfheight = self.height / 2.0
        x1 = self.center[0] - quartwidth
        x2 = self.center[0] + quartwidth
        y1 = self.center[1] - quartheight
        y2 = self.center[1] + quartheight
        new_depth = self._depth + 1
        self.children = [_QuadTree(x1, y1, halfwidth, halfheight,
                                   self.max_items, self.max_depth, new_depth),
                         _QuadTree(x1, y2, halfwidth, halfheight,
                                   self.max_items, self.max_depth, new_depth),
                         _QuadTree(x2, y1, halfwidth, halfheight,
                                   self.max_items, self.max_depth, new_depth),
                         _QuadTree(x2, y2, halfwidth, halfheight,
                                   self.max_items, self.max_depth, new_depth)]
        nodes = self.nodes
        self.nodes = []
        for node in nodes:
            self._insert_into_children(node.item, node.rect)

    def __len__(self):
        """
        Returns:
        - A count of the total number of members/items/nodes inserted
        into this quadtree and all of its child trees.
        """
        size = 0
        for child in self.children:
            size += len(child)
        size += len(self.nodes)
        return size


MAX_ITEMS = 10
MAX_DEPTH = 20


class QuadTree(_QuadTree):
    def __init__(self, bounding=None, x=None, y=None, width=None, height=None, max_items=MAX_ITEMS, max_depth=MAX_DEPTH):

        if bounding is not None:
            x1, y1, x2, y2 = bounding
            width, height = abs(x2-x1), abs(y2-y1)
            mid_x, mid_y = x1+width/2.0, y1+height/2.0
            super(QuadTree, self).__init__(mid_x, mid_y, width, height, max_items, max_depth)

        elif None not in (x, y, width, height):
            super(QuadTree, self).__init__(x, y, width, height, max_items, max_depth)

        else:
            raise Exception("Either the bounding argument must be set, or the x, y, width, and height arguments must be set")
