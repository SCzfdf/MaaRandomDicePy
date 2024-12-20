import logging
import threading
import time
from typing import List

from readerwriterlock import rwlock


class RDContext:
    # 初始坐标, 棋盘左上角 也即是第一个骰子的左上角(差不多)
    # init_x = 160
    # init_y = 720
    init_x = 150
    init_y = 700

    # 骰子大小
    dice_size = 70

    dice_list: List[List[int]] = None

    # 截图
    _screenshot_lock = rwlock.RWLockFair()
    _screenshot_img = None

    # 移动
    _swipe_lock = threading.Lock

    # 需要移动次数
    _need_swipe_num = 0
    _need_swipe_lock = threading.Lock

    # 红骰子下标
    # _red_ston_list: List[int] = []
    # 红骰子坐标
    red_stone_box = None

    def __init__(self):
        pass

    @staticmethod
    def init_dice_list() -> List[List[int]]:
        RDContext.dice_list = list()
        for i in range(3):
            for o in range(5):
                dice_roi = [RDContext.init_x + (RDContext.dice_size + 10) * o,
                            RDContext.init_y + (RDContext.dice_size + 10) * i,
                            RDContext.dice_size + 10, RDContext.dice_size + 10]
                logging.info(f'init_dice_list [{i}, {o}] = [{dice_roi}]')
                RDContext.dice_list.append(dice_roi)
        return RDContext.dice_list

    @staticmethod
    def set_screenshot(img):
        with RDContext._screenshot_lock.gen_wlock():
            RDContext._screenshot_img = img

    @staticmethod
    def get_screenshot():
        with RDContext._screenshot_lock.gen_rlock():
            return RDContext._screenshot_img

    @staticmethod
    def get_swipe_lock():
        return RDContext._swipe_lock

    @staticmethod
    def try_get_swipe_token() -> bool:
        if RDContext._need_swipe_num > 0:
            with RDContext._need_swipe_lock:
                if RDContext._need_swipe_num <= 0:
                    return False
                else:
                    time.sleep(0.01)
                    RDContext._need_swipe_num -= 1
                    return True
        else:
            return False
