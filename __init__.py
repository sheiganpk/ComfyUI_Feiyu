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
from .FyString.StringTranslate import FyTranslateZH2EN


class MyExtension(ComfyExtension):
    @override
    async def get_node_list(self):
        return [FyImageChangeBrightness, FyChangeSize, FyImageConcat, FyImageFlip, FyImageCreate, FyImageGrid3x3Create, FyImageGridSplit
                , FyTranslateZH2EN]
    
    @override
    async def setup(self):
        print("Feiyu extension setup complete")

async def comfy_entrypoint():
    return MyExtension()