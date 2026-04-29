import torch
from comfy_api.latest import io

class FyImageGridSplit(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="FyImageGridSplit",
            display_name="Fy宫格切割",
            category="飞羽/图像",

            inputs=[
                io.Image.Input("image"),

                io.Int.Input("cell_width", default=256, min=1, max=4096),
                io.Int.Input("cell_height", default=256, min=1, max=4096),
            ],

            outputs=[
                io.Image.Output() for _ in range(9)
            ],
        )

    @classmethod
    def execute(cls, image,  cell_width, cell_height):

        rows=3
        cols=3

        B, H, W, C = image.shape

        # 转 BCHW
        image = image.permute(0, 3, 1, 2)

        outputs = []

        for r in range(rows):
            for c in range(cols):

                y1 = r * cell_height
                y2 = (r + 1) * cell_height

                x1 = c * cell_width
                x2 = (c + 1) * cell_width

                # 防止越界
                y2 = min(y2, H)
                x2 = min(x2, W)

                crop = image[:, :, y1:y2, x1:x2]

                outputs.append(crop)

        # 不足 9 张就补空（防止崩）
        while len(outputs) < 9:
            outputs.append(outputs[-1])

        # 转回 BHWC
        outputs = [
            o.permute(0, 2, 3, 1) for o in outputs
        ]

        return io.NodeOutput(*outputs)