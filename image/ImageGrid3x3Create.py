import torch
import torch.nn.functional as F
from comfy_api.latest import io


class FyImageGrid3x3Create(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="ImageGrid3x3Create",
            display_name="Fy九宫格创建",
            category="飞羽/图像",
            inputs=[
                io.Image.Input(f"image{i}") for i in range(1, 10)
            ] + [
                io.Int.Input("cell_size", display_name="格子尺寸", default=256, min=32, max=1024),
                io.Int.Input("gap", display_name="间隙", default=0, min=0, max=100),
            ],
            outputs=[io.Image.Output()],
        )

    @classmethod
    def execute(cls, **kwargs):

        cell_size = kwargs["cell_size"]
        gap = kwargs["gap"]

        images = [kwargs[f"image{i}"] for i in range(1, 10)]

        # resize到统一尺寸
        resized = []
        for img in images:
            img = img.permute(0, 3, 1, 2)
            img = F.interpolate(img, size=(cell_size, cell_size), mode="bilinear")
            resized.append(img)

        # 拼每一行
        rows = []
        for i in range(0, 9, 3):
            row = resized[i]

            for j in range(1, 3):
                if gap > 0:
                    gap_tensor = torch.zeros(
                        (1, 3, cell_size, gap), device=row.device
                    )
                    row = torch.cat([row, gap_tensor], dim=3)

                row = torch.cat([row, resized[i + j]], dim=3)

            rows.append(row)

        # 拼列
        out = rows[0]
        for i in range(1, 3):
            if gap > 0:
                gap_tensor = torch.zeros(
                    (1, 3, gap, out.shape[3]), device=out.device
                )
                out = torch.cat([out, gap_tensor], dim=2)

            out = torch.cat([out, rows[i]], dim=2)

        out = out.permute(0, 2, 3, 1)

        return io.NodeOutput(out)