import os
from datetime import datetime

from maa.controller import AdbController
from maa.resource import Resource
from maa.tasker import Tasker
from maa.toolkit import Toolkit

from src.action.custom_swipe import CustomSwipe


def main():
    current_dir = os.getcwd()
    print(f'current_dir:{current_dir}')
    resource_path = os.path.join(current_dir, "assets", "resource")

    Toolkit.init_option(os.path.join(current_dir, "assets"))

    # 资源
    resource = Resource()
    resource.post_path(resource_path).wait()
    resource.register_custom_action("custom_swipe", CustomSwipe())

    # 模拟器
    controller = get_controller()

    # 任务
    task = get_task(resource, get_controller())

    while True:
        # print(f'-----------start:{datetime.now()}')
        # result = task.post_pipeline('recognition_monster').wait().get()
        # result = task.post_pipeline('start').wait().get()
        task.post_pipeline('recognition_monster').wait()
        # print(f'===========end:{datetime.now()} result:{result}')

    # Toolkit.pi_register_custom_action("MyAct", MyAction())


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
    main()
