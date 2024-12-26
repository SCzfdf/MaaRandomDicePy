import logging
import os
import random
import threading
import time
from typing import List

from maa.controller import AdbController
from maa.resource import Resource
from maa.tasker import Tasker
from maa.toolkit import Toolkit

from src.action.recognition_ston_action import RecognitionStonAction
from src.action.screenshot_action import ScreenshotAction
from src.entity.dice import Dice
from src.entity.list_node import list_to_circular_linkedlist
from src.rd_context import RDContext


def main():
    dice_coord_list = RDContext.init_dice_list()
    dice_list: List[Dice] = []

    current_dir = os.getcwd()
    print(f'current_dir:{current_dir}')
    resource_path = os.path.join(current_dir, "assets", "resource")

    Toolkit.init_option(os.path.join(current_dir, "assets"))

    # 资源
    resource = Resource()
    resource.post_path(resource_path).wait()
    resource.register_custom_action("screenshot_action", ScreenshotAction())
    for i in range(15):
        dice = Dice(dice_coord_list[i][0], dice_coord_list[i][1], i)
        dice_list.append(dice)
        resource.register_custom_action(f"recognition_ston_action_{i}", RecognitionStonAction(dice))

    # 模拟器
    controller = get_controller()

    # 任务
    threading.Thread(target=screenshot, args=(resource, controller)).start()
    threading.Thread(target=show_board, args=(dice_list,)).start()
    for i in range(15):
        threading.Thread(target=recognition_ston, args=(resource, controller, i)).start()

    # 动作线程, 执行动作(将蓝骰子拖拽到红骰子出)
    red_dice_node = None
    blue_dice_node = None
    while True:
        time.sleep(0.1)
        if red_dice_node is None:
            red_dice_node = list_to_circular_linkedlist(dice_list)
        if blue_dice_node is None:
            blue_dice_node = list_to_circular_linkedlist(dice_list)

        while True:
            red_dice_node = red_dice_node.next
            if red_dice_node.val.type == "R":
                break
            time.sleep(0.05)
            # logging.debug("find red")

        while True:
            blue_dice_node = blue_dice_node.next
            if blue_dice_node.val.type == "B":
                break
            # logging.debug("find red")

        logging.debug("swipe")
        # randint = random.randint(20, 55)
        randint = 35
        controller.post_swipe(blue_dice_node.val.roi_x + randint, blue_dice_node.val.roi_y + randint,
                              red_dice_node.val.roi_x + randint, red_dice_node.val.roi_y + randint,
                              200)
        time.sleep(0.1)


def show_board(dice_list: List[Dice]):
    """
    打印骰子列表到日志，每5个数据换一行

    Args:
        dice_list: 骰子列表
    """
    while True:
        time.sleep(3)
        log_line = ""
        for i, dice in enumerate(dice_list):
            log_line += dice.type + " "

            # 每5个数据输出一行日志
            if (i + 1) % 5 == 0:
                logging.debug(log_line.strip())
                log_line = ""


def recognition_ston(resource: Resource, controller: AdbController, index: int):
    task = get_task(resource, controller)
    while True:
        task.post_pipeline(entry=f"custom_monitor_dice", pipeline_override={
            "custom_monitor_dice": {
                "action": "Custom",
                "custom_action": f"recognition_ston_action_{index}",
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
