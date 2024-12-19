import logging
import os
import threading
import time

from maa.controller import AdbController
from maa.resource import Resource
from maa.tasker import Tasker
from maa.toolkit import Toolkit

from src.action.blue_stone_action import BlueStoneAction
from src.action.custom_swipe import CustomSwipe
from src.action.monster_action import MonsterAction

monster_flag = False
red_stone_flag = False
red_stone_box = None
red_stone_lock = threading.Lock()


def main():
    current_dir = os.getcwd()
    print(f'current_dir:{current_dir}')
    resource_path = os.path.join(current_dir, "assets", "resource")

    Toolkit.init_option(os.path.join(current_dir, "assets"))

    # 资源
    resource = Resource()
    resource.post_path(resource_path).wait()
    resource.register_custom_action("custom_swipe", CustomSwipe())
    resource.register_custom_action("blue_stone_action", BlueStoneAction())
    resource.register_custom_action("red_stone_action", CustomSwipe())
    resource.register_custom_action("monster_action", MonsterAction())

    # 模拟器
    controller = get_controller()

    # 任务
    threading.Thread(target=run_recognition_monster_x_task, args=(resource, controller))
    # threading.Thread(target=run_recognition_monster_y_task, args=(resource, controller))
    # threading.Thread(target=run_recognition_red_stone_task, args=(resource, controller))
    # threading.Thread(target=recognition_blue_stone_task, args=(resource, controller))


def run_recognition_monster_x_task(resource, controller):
    task = get_task(resource, controller)
    while True:
        task.post_pipeline('recognition_monster').wait()


def run_recognition_monster_y_task(resource, controller):
    task = get_task(resource, controller)
    while True:
        task.post_pipeline('recognition_monster2').wait()


def run_recognition_red_stone_task(resource, controller):
    task = get_task(resource, controller)
    while True:
        task.post_pipeline('recognition_red_stone').wait()


def recognition_blue_stone_task(resource, controller):
    task = get_task(resource, controller)
    while True:
        task.post_pipeline('recognition_blue_stone').wait()
        time.sleep(5)


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
    # logging.basicConfig(
    #     level=logging.DEBUG,  # 设置日志级别
    #     format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志格式
    #     filename='app.log',  # 输出到文件
    #     filemode='w'  # 文件模式（覆盖写入）
    # )
    main()
