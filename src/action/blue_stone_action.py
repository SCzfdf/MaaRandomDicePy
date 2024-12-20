import logging
import random
import threading
from datetime import datetime

import time

from maa.context import Context
from maa.custom_action import CustomAction
from maa.define import Rect

import __main__


def check_status():
    start_time = time.time()

    while True:
        if __main__.monster_flag and __main__.red_stone_flag:
            flag = True
            break

        print(f"{__main__.monster_flag} + {__main__.red_stone_flag}")

        if time.time() - start_time >= 5:
            flag = False
            break

    return flag


class BlueStoneAction(CustomAction):

    def run(self,
            context: Context,
            argv: CustomAction.RunArg) -> bool:
        """
        :param argv: 运行参数, 包括action_list和loop_times
        :param context: 运行上下文
        :return: 是否执行成功
        """
        if check_status():
            blue_box = argv.box
            if is_within_distance(blue_box[0], blue_box[1], __main__.last_x, __main__.last_y):
                print("is swipe")
                return True

            with __main__.swipe_lock:
                # logging.log(f"{blue_box.x}-{blue_box.y} swipe {__main__.red_stone_box.x}-{__main__.red_stone_box.x.y}")
                print(f"1{blue_box} + {__main__.red_stone_box}")
                randint = random.randint(20, 50)
                context.tasker.controller.post_swipe(blue_box.x + randint,
                                                     blue_box.y + randint,
                                                     __main__.red_stone_box.x + randint,
                                                     __main__.red_stone_box.y, + randint,
                                                     random.randint(80, 150))
                __main__.last_x = blue_box.x
                __main__.last_y = blue_box.y
                # __main__.monster_flag = False

        return True


def is_within_distance(x1, y1, x2, y2, threshold=20):
    # 计算两点之间的距离
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    # 判断是否在阈值范围内
    return distance <= threshold


def calculate_overlap_area(rect1: Rect, rect2: Rect) -> float:
    """
    计算两个矩形ROI的重叠面积

    Args:
        rect1: 第一个矩形ROI，包含x,y,w,h属性
        rect2: 第二个矩形ROI，包含x,y,w,h属性

    Returns:
        float: 重叠的面积。如果没有重叠则返回0
    """
    # 计算两个矩形的坐标范围
    x1_left = rect1.x
    x1_right = rect1.x + rect1.w
    y1_top = rect1.y
    y1_bottom = rect1.y + rect1.h

    x2_left = rect2.x
    x2_right = rect2.x + rect2.w
    y2_top = rect2.y
    y2_bottom = rect2.y + rect2.h

    # 判断是否有重叠
    if (x1_right <= x2_left or  # rect1在rect2左边
            x2_right <= x1_left or  # rect1在rect2右边
            y1_bottom <= y2_top or  # rect1在rect2上边
            y2_bottom <= y1_top):  # rect1在rect2下边
        return 0

    # 计算重叠区域的坐标
    overlap_left = max(x1_left, x2_left)
    overlap_right = min(x1_right, x2_right)
    overlap_top = max(y1_top, y2_top)
    overlap_bottom = min(y1_bottom, y2_bottom)

    # 计算重叠面积
    overlap_width = overlap_right - overlap_left
    overlap_height = overlap_bottom - overlap_top
    overlap_area = overlap_width * overlap_height

    return overlap_area


def point_in_rect(rect: Rect, point_x: float, point_y: float) -> bool:
    """
    判断点是否在矩形ROI内部

    Args:
        rect: 矩形ROI，包含x,y,w,h属性
        point_x: 点的x坐标
        point_y: 点的y坐标

    Returns:
        bool: 如果点在ROI内部（包括边界）返回True，否则返回False
    """
    return (point_x >= rect.x and
            point_x <= (rect.x + rect.w) and
            point_y >= rect.y and
            point_y <= (rect.y + rect.h))
