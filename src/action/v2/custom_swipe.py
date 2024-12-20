import random
import threading
from datetime import datetime

import time

from maa.context import Context
from maa.custom_action import CustomAction
from maa.define import Rect


class CustomSwipe(CustomAction):
    red_stone_list: list[Rect] = []
    board_roi = [0, 0, 0, 0]

    find_red_stone_thread_flag = False
    lock = threading.Lock()

    RED = "\033[91m"
    RESET = "\033[0m"  # 重置颜色

    def run(self,
            context: Context,
            argv: CustomAction.RunArg) -> bool:
        """
        :param argv: 运行参数, 包括action_list和loop_times
        :param context: 运行上下文
        :return: 是否执行成功
        """
        # 读取 custom_param 的参数：{"action_list": ["A", "B", "C"], "loop_times": x}
        # print(f"CustomSwipe start:{datetime.now()}")

        if not self.find_red_stone_thread_flag:
            print("CustomSwipe find_red_stone_thread start")
            self.find_red_stone(context)
            self.find_red_stone_thread_flag = True

        blue_stone = self.find_blue_stone(context)
        if blue_stone is None:
            print("blue_stone not fond")
        else:
            red_stone = random.choice(self.red_stone_list)
            print(self.RED + f"blue_stone fond {blue_stone.x}-{blue_stone.y}   {red_stone.x}-{red_stone.y}" + self.RESET)
            randint = random.randint(20, 50)
            context.tasker.controller.post_swipe(blue_stone.x + randint,
                                                 blue_stone.y + randint,
                                                 red_stone.x + + randint,
                                                 red_stone.y + + randint,
                                                 random.randint(80, 200))

        # print(f"CustomSwipe end:{datetime.now()}")
        return True

    def find_red_stone(self, context: Context):
        if self.red_stone_list:
            print("find_red_stone is has")
        else:
            resource = context.tasker.resource
            recognition_pipeline = context.run_pipeline("recognition_red_stone")
            with self.lock:
                if recognition_pipeline.nodes:
                    for item in recognition_pipeline.nodes:
                        self.red_stone_list.append(item.recognition.box)
                else:
                    print("recognition_red_stone error")

    def find_blue_stone(self, context: Context):
        # img = context.tasker.controller.post_screencap().wait().get()
        # recognition = context.run_recognition("recognition_blue_stone", img, {"recognition_blue_stone": {
        #     "recognition": "FeatureMatch",
        #     "roi": [110, 648, 600, 450],
        #     "template": [
        #         "blue_stone_4.png"
        #     ],
        #     "pre_delay": 0,
        #     "post_delay": 0,
        #     "rate_limit": 100,
        #     "method": 5,
        #     "count": 16
        # }})

        # return recognition.box

        recognition_pipeline = context.run_pipeline("recognition_blue_stone")
        if not recognition_pipeline or not recognition_pipeline.nodes:
            print("recognition_red_stone error")
            return None

        return recognition_pipeline.nodes[0].recognition.box
