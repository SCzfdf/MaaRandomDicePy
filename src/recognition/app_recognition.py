from typing import Union, Optional

from deps.binding.Python.maa.context import Context
from deps.binding.Python.maa.custom_recognition import CustomRecognition
from deps.binding.Python.maa.define import RectType


class AppRecognition(CustomRecognition):
    def analyze(self,
                context: Context,
                argv: CustomRecognition.AnalyzeArg
                ) -> Union[CustomRecognition.AnalyzeResult, Optional[RectType]]:
        recognition = context.run_recognition("pipeline_open_app")
        print(f'-------------recognition:{recognition}')

        pass
