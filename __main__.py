import os

from deps.binding.Python.maa.controller import AdbController
from deps.binding.Python.maa.resource import Resource
from deps.binding.Python.maa.tasker import Tasker
from deps.binding.Python.maa.toolkit import Toolkit
from src.recognition.app_recognition import AppRecognition


def main():
    current_dir = os.getcwd()
    resource_path = os.path.join(current_dir, "assets", "resource")

    Toolkit.init_option(os.path.join(current_dir, "assets"))

    # 资源
    resource = Resource()
    resource.post_path(resource_path).wait()
    resource.register_custom_recognition("AppRecognition", AppRecognition())

    # 模拟器
    controller = get_controller()

    # 任务
    task = get_task(resource, get_controller())

    result = task.post_pipeline("pipeline").wait().get()
    print(f'===========result:{result}')

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
