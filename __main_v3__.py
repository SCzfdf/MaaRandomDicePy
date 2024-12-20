import logging
import os
import threading
from typing import List

import time

from maa.controller import AdbController, Controller
from maa.resource import Resource
from maa.tasker import Tasker
from maa.toolkit import Toolkit

from src.action.recognition_single_blue_ston_action import RecognitionSingleBlueStonAction
from src.action.screenshot_action import ScreenshotAction
from src.action.v2.blue_stone_action import BlueStoneAction
from src.action.v2.monster_action import MonsterAction
from src.action.v2.red_stone_action import RedStoneAction
from src.rd_context import RDContext


def main():
    dice_list = RDContext.init_dice_list()

    current_dir = os.getcwd()
    print(f'current_dir:{current_dir}')
    resource_path = os.path.join(current_dir, "assets", "resource")

    Toolkit.init_option(os.path.join(current_dir, "assets"))

    # 资源
    resource = Resource()
    resource.post_path(resource_path).wait()
    resource.register_custom_action("screenshot_action", ScreenshotAction())
    # resource.register_custom_action("red_stone_action", RedStoneAction())
    for i in range(15):
        resource.register_custom_action(f"recognition_single_blue_ston_action_{i}",
                                        RecognitionSingleBlueStonAction(dice_list[i], i))

    # 模拟器
    controller = get_controller()

    # 任务
    threading.Thread(target=run_recognition_red_stone_task, args=(resource, controller)).start()
    threading.Thread(target=run_recognition_red_stone_task, args=(resource, controller)).start()
    threading.Thread(target=run_recognition_red_stone_task2, args=(resource, controller)).start()
    #
    threading.Thread(target=screenshot, args=(resource, controller)).start()
    time.sleep(5)
    # threading.Thread(target=blue_ston, args=(resource, controller, 13)).start()
    for i in range(15):
        threading.Thread(target=blue_ston, args=(resource, controller, i)).start()


def run_recognition_red_stone_task(resource, controller):
    task = get_task(resource, controller)
    while True:
        task.post_pipeline('recognition_red_stone').wait()
        time.sleep(1)


def run_recognition_red_stone_task2(resource, controller):
    task = get_task(resource, controller)
    while True:
        task.post_pipeline('recognition_red_stone2').wait()
        time.sleep(10)


def blue_ston(resource: Resource, controller: AdbController, index: int):
    task = get_task(resource, controller)
    while True:
        task.post_pipeline(entry=f"custom_monitor_dice", pipeline_override={
            "custom_monitor_dice": {
                "action": "Custom",
                "custom_action": f"recognition_single_blue_ston_action_{index}",
                "pre_delay": 0,
                "post_delay": 0
            }
        }).wait()


def screenshot(resource: Resource, controller: AdbController):
    task = get_task(resource, controller)
    while True:
        task.post_pipeline('screenshot').wait()


def get_task(resource: Resource, controller: AdbController) -> Tasker:
    tasker = Tasker()
    tasker.bind(resource, controller)

    if not tasker.inited:
        print("Failed to init MAA.")
        exit()

    return tasker


def get_controller() -> AdbController:
    adb_devices = Toolkit.find_adb_devices()
    if not adb_devices:
        print("No ADB device found...")
        exit()

    # for demo, we just use the first device
    device = adb_devices[0]
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
        screencap_methods=device.screencap_methods,
        input_methods=device.input_methods,
        config=device.config,
    )
    controller.post_connection().wait()
    return controller


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(thread)s %(levelname)s - %(message)s',
    )
    logging.info("xxx")
    main()
