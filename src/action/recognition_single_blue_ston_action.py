import json
import logging
import random
import threading
from datetime import datetime
from typing import List, Dict

import time
from datetime import datetime, timedelta

from maa.context import Context
from maa.custom_action import CustomAction
from maa.define import Rect

import __main__
from src.rd_context import RDContext


class RecognitionSingleBlueStonAction(CustomAction):
    monitor_dice: List[int]
    monitor_index: int
    recognition: Dict
    last_recognition_img = None

    # 上一次识别是否已经成功识别
    is_read: bool = False

    # 移动间隔和上次移动时间
    last_swipe: int = 0
    swipe_limit: int = 2

    def __init__(self, monitor_dice, monitor_index):
        super().__init__()
        self.monitor_dice = monitor_dice
        self.monitor_index = monitor_index
        self.recognition = {
            f"recognition_single_blue_ston_{self.monitor_index}": {
                "recognition": "TemplateMatch",
                "roi": self.monitor_dice,
                "roi_offset": [0, 0, 10, 10],
                "template": [
                    "blue_stone_4.png",
                    "blue_stone_3.png",
                    "blue_stone_2.png",
                    "blue_stone_1.png",
                ],
                "threshold": [0.7, 0.7, 0.7, 0.7],
                "pre_delay": 0,
                "post_delay": 0,
                "method": 5,
                "count": 16,
            }
        }

    def run(self,
            context: Context,
            argv: CustomAction.RunArg) -> bool:
        """
        :param argv: 运行参数, 包括action_list和loop_times
        :param context: 运行上下文
        :return: 是否执行成功
        """
        timestamp = int(datetime.now().timestamp())
        if timestamp < self.last_swipe + self.swipe_limit:
            return True

        if not self.is_read:
            screenshot = RDContext.get_screenshot()
            if screenshot is None:
                logging.debug('wait screenshot')
                return True

            if self.last_recognition_img == id(screenshot):
                logging.debug('img is recognition')
                return True

            self.last_recognition_img = id(screenshot)

            recognition_result = context.run_recognition(f"recognition_single_blue_ston_{self.monitor_index}",
                                                         screenshot,
                                                         self.recognition)
            if recognition_result is None:
                logging.debug(f'{self.monitor_index} is not blue')
                return True

        # 前面没有返回就表示可以抢占拖动
        self.is_read = True
        end_time = timestamp + 5
        while int(datetime.now().timestamp()) < end_time and RDContext.try_get_swipe_token():
            with RDContext.get_swipe_lock():
                if RDContext.red_stone_box is None:
                    logging.error("red_stone_box is None")
                else:
                    randint = random.randint(-30, 30)
                    logging.error("red_stone_box is None")
                    context.tasker.controller.post_swipe(
                        self.monitor_dice[0] + 45 + randint, self.monitor_dice[1] + 45 + randint,
                        RDContext.red_stone_box.x + 40, RDContext.red_stone_box.y + 40,
                        randint + 150
                    )
                    self.is_read = False
                    self.last_swipe = timestamp

        return True
