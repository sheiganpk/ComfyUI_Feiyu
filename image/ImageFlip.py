import torch
from comfy_api.latest import io


class FyImageFlip(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="FyImageFlip",
            display_name="Fy图像翻转",
            category="飞羽/图像",
            inputs=[
                io.Image.Input("image"),
                io.Combo.Input(
                    "mode",
                    options=["horizontal", "vertical", "both"]
                ),
            ],
            outputs=[
                io.Image.Output(),
            ],
        )

    @classmethod
    def execute(cls, image, mode):

        if mode == "horizontal":
            # 左右翻转（宽度维）
            image = torch.flip(image, dims=[2])

        elif mode == "vertical":
            # 上下翻转（高度维）
            image = torch.flip(image, dims=[1])

        elif mode == "both":
            # 同时翻转
            image = torch.flip(image, dims=[1, 2])

        return io.NodeOutput(image)