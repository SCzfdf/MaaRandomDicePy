import logging
import time
from typing import Dict

from maa.context import Context
from maa.custom_action import CustomAction

from src.entity.dice import Dice
from src.rd_context import RDContext


class RecognitionStonAction(CustomAction):
    monitor_dice: Dice

    last_recognition_img = None

    recognition_blue_title: str
    recognition_blue: Dict

    recognition_red_title: str
    recognition_red: Dict

    # roi_offset = [10, 20, 10, 10]
    roi_offset = [0, 0, 30, 30]

    def __init__(self, monitor_dice):
        super().__init__()
        self.monitor_dice = monitor_dice

        self.recognition_blue_title = f"recognition_single_blue_ston_{self.monitor_dice.index}"
        self.recognition_blue = {
            f"recognition_single_blue_ston_{self.monitor_dice.index}": {
                "recognition": "TemplateMatch",
                # "recognition": "FeatureMatch",
                "roi": [self.monitor_dice.roi_x, self.monitor_dice.roi_y,
                        self.monitor_dice.roi_h, self.monitor_dice.roi_w],
                "roi_offset": self.roi_offset,
                "template": [
                    "b1a2.png", "b1b.png", "b2b.png", "b2b2.png", "b3a.png", "b3b.png", "b3b2.png", "b4a1.png",
                    "b4b.png", "b5a.png", "b5b.png", "b5b1.png", "b5b2.png", "b5b3.png", "b6a.png", "b6b.png",
                    "b7a.png", "b7b.png", "b7b1.png", "b7b2.png"
                ],
                "threshold": [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7,
                              0.7, 0.7],
                "pre_delay": 0,
                "post_delay": 0,
                "method": 5,
                "count": 4,
            }
        }

        self.recognition_red_title = f"recognition_single_blue_ston_{self.monitor_dice.index}"
        self.recognition_red = {
            f"recognition_single_blue_ston_{self.monitor_dice.index}": {
                "recognition": "TemplateMatch",
                # "recognition": "FeatureMatch",
                "roi": [self.monitor_dice.roi_x, self.monitor_dice.roi_y,
                        self.monitor_dice.roi_h, self.monitor_dice.roi_w],
                "roi_offset": self.roi_offset,
                "template": ["r1.png", "r2.png", "r3.png", "r4.png", "r5.png", "r6.png", "r7.png"],
                "threshold": [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                "pre_delay": 0,
                "post_delay": 0,
                "method": 5,
                "count": 4,
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
        screenshot = RDContext.get_screenshot()
        if screenshot is None:
            logging.debug('wait screenshot')
            return True

        if self.last_recognition_img == id(screenshot):
            logging.debug('is recognition screenshot')
            return True

        # 识别蓝色骰子
        now = time.time()
        recognition_blue_result = context.run_recognition(self.recognition_blue_title,
                                                          screenshot,
                                                          self.recognition_blue)

        # 识别红色骰子
        # logging.debug(f"1---{time.time() - now}---{recognition_blue_result.best_result.count if recognition_blue_result else None}")
        # logging.debug(recognition_blue_result)
        now = time.time()
        recognition_red_result = context.run_recognition(self.recognition_red_title,
                                                         screenshot,
                                                         self.recognition_red)
        # logging.debug(f"2---{time.time() - now}----{recognition_red_result.best_result.count if recognition_red_result else None}")
        # logging.debug(recognition_red_result)

        # 如果2个都识别不到就设置类型为-
        if recognition_blue_result is None and recognition_red_result is None:
            self.monitor_dice.type = "-"
            return True

        # 判断得分设置骰子类型
        # logging.debug(f'recognition blue:{recognition_blue_result.best_result.count}, red:{recognition_red_result.best_result.count}')
        if recognition_blue_result is not None and recognition_red_result is not None:
            # if recognition_blue_result.best_result.score > recognition_red_result.best_result.score:
            if recognition_blue_result.best_result.count > recognition_red_result.best_result.count:
                self.monitor_dice.type = "B"
            else:
                self.monitor_dice.type = "R"
        else:
            if recognition_blue_result is not None:
                self.monitor_dice.type = "B"
            elif recognition_red_result is not None:
                self.monitor_dice.type = "R"

        return True
