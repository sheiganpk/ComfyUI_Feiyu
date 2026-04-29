from comfy_api.latest import io
import torch

class FyImageChangeBrightness(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="Feiyu Image Change Brightness",
            display_name="Fy图像修改亮度",
            category="飞羽/图像",
            inputs=[
                io.Image.Input("image", "图像"),
                io.Float.Input("scale","亮度(0-2)", default=1.0, min=0.0, max=2.0)
            ],
            outputs=[
                io.Image.Output(),
            ],
        )

    @classmethod
    def execute(cls, image:torch.Tensor, scale):
        image = image * scale
        image = image.clamp(0, 1)
        return io.NodeOutput(image)