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

        if time.time() - start_time >= 5:
            flag = False
            break

        time.sleep(0.2)

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
            with __main__.red_stone_lock:
                logging.log(f"{blue_box.x}-{blue_box.y} swipe {__main__.red_stone_box.x}-{__main__.red_stone_box.x.y}")
                randint = random.randint(20, 50)
                context.tasker.controller.post_swipe(blue_box.x + randint,
                                                     blue_box.y + randint,
                                                     __main__.red_stone_box.x + + randint,
                                                     __main__.red_stone_box.y + + randint,
                                                     random.randint(80, 200))

        return True
