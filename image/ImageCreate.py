from comfy_api.latest import io
import torch

class FyImageCreate(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="Fy Image Create",
            display_name="Fy纯色图像",
            category="飞羽/图像",
            inputs=[
                io.Int.Input("width", default=512, min=1, max=4096),
                io.Int.Input("height", default=512, min=1, max=4096),

                io.Float.Input("r", default=1.0, min=0.0, max=1.0),
                io.Float.Input("g", default=1.0, min=0.0, max=1.0),
                io.Float.Input("b", default=1.0, min=0.0, max=1.0),
            ],
            outputs=[
                io.Image.Output(),
            ],
        )

    @classmethod
    def execute(cls, width, height, r, g, b):
         # 创建空图（全0）
        image = torch.zeros((1, height, width, 3), dtype=torch.float32)

        # 填充颜色
        image[:, :, :, 0] = r
        image[:, :, :, 1] = g
        image[:, :, :, 2] = b

        return io.NodeOutput(image)