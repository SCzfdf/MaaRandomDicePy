import random
import threading
from datetime import datetime

import time

from maa.context import Context
from maa.custom_action import CustomAction
from maa.define import Rect

import __main__


class RecognitionSingleBlueStonAction(CustomAction):

    def run(self,
            context: Context,
            argv: CustomAction.RunArg) -> bool:
        """
        :param argv: 运行参数, 包括action_list和loop_times
        :param context: 运行上下文
        :return: 是否执行成功
        """

        img = context.tasker.controller.post_screencap().wait().get()
        detail = context.run_recognition("recognition_single_blue_ston",
                                         img,
                                         {"roi": []}
                                         )

        return True
