"""bad module docstring missing period"""

import os, sys                    # VIOLATION: 同行多导入；未分组排序
from .utils import helper         # VIOLATION: 相对导入
from typing import *              # VIOLATION: 通配符导入

global_list = []                  # VIOLATION: 可变全局状态


class cheese_shop:                # VIOLATION: 类名应为 CapWords
    def __init__(self):
        self.inventory={}         # VIOLATION: 运算符两侧无空格

    def addCheese(self, name, qty=[]):  # VIOLATION: 方法名 camelCase；
                                        # VIOLATION: 可变默认值 list；
                                        # VIOLATION: 无类型注解
        """add cheese"""          # VIOLATION: 摘要未以标点结尾；无 Args/Returns
        assert qty > 0            # VIOLATION: assert 替代前置条件
        global_list.append(name)  # VIOLATION: 修改可变全局状态
        self.inventory[name] = qty
        print('added '+name+' x'+str(qty))  # VIOLATION: + 拼接字符串

    def getStock(self, name):
        try:                      # VIOLATION: try 块过大
            result = self.inventory[name]
            if result == None:    # VIOLATION: 用 == 判断 None
                return 0
            return result
        except:                   # VIOLATION: 裸 except
            pass                  # VIOLATION: 吞异常


if __name__ == '__main__':
    shop = cheese_shop()          # VIOLATION: 顶级代码直接执行
    shop.addCheese('brie', 5)
