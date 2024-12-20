import json
import logging
import random
import threading
from datetime import datetime

import time

from maa.context import Context
from maa.custom_action import CustomAction
from maa.define import Rect

import __main__
from src.rd_context import RDContext


class ScreenshotAction(CustomAction):

    def run(self,
            context: Context,
            argv: CustomAction.RunArg) -> bool:
        """
        截图线程
        """
        img = context.tasker.controller.post_screencap().wait().get()
        logging.debug("ScreenshotAction post_screencap")
        RDContext.set_screenshot(img)

        return True
