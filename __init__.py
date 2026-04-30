from typing_extensions import override
from comfy_api.latest import ComfyExtension

from .example_node import FeiyuTest
from .image.ImageChangeBrightness import FyImageChangeBrightness
from .image.ImageChangeSize import FyChangeSize
from .image.ImageConcat import FyImageConcat
from .image.ImageFlip import FyImageFlip
from .image.ImageCreate import FyImageCreate
from .image.ImageGrid3x3Create import FyImageGrid3x3Create
from .image.ImageGrid3x3Split import FyImageGridSplit
from .image.ImageGetSize import FyGetSize
from .FyString.StringTranslate import FyTranslateZH2EN
from .Request.GPT_Image_2 import FyGPT_Image_2


# 模块级别定义 - 让ComfyUI加载web目录
WEB_DIRECTORY = "./web"


class MyExtension(ComfyExtension):

    @override
    async def get_node_list(self):
        return [FyImageChangeBrightness, FyChangeSize, FyImageConcat, FyImageFlip, FyImageCreate, FyImageGrid3x3Create, FyImageGridSplit, FyGetSize, 
                FyTranslateZH2EN,
                FyGPT_Image_2]
    
    @override
    async def setup(self):
        print("Feiyu extension setup complete")

async def comfy_entrypoint():
    return MyExtension()