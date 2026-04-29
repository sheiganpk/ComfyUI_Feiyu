import torch
import torch.nn.functional as F
from comfy_api.latest import io


class FyImageConcat(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="FyImageConcat",
            display_name="Fy图像拼接",
            category="飞羽/图像",
            inputs=[
                io.Image.Input("image1"),
                io.Image.Input("image2"),

                io.Combo.Input(
                    "direction",
                    options=["horizontal", "vertical"]
                ),
            ],
            outputs=[
                io.Image.Output(),
            ],
        )

    @classmethod
    def execute(cls, image1, image2, direction):

        # 转 BCHW
        img1 = image1.permute(0, 3, 1, 2)
        img2 = image2.permute(0, 3, 1, 2)

        B1, C1, H1, W1 = img1.shape
        B2, C2, H2, W2 = img2.shape

        # ===== 对齐尺寸 =====
        if direction == "horizontal":
            # 高度对齐
            target_h = min(H1, H2)

            img1 = F.interpolate(img1, size=(target_h, W1), mode="bilinear")
            img2 = F.interpolate(img2, size=(target_h, W2), mode="bilinear")

            # 拼接（宽度方向）
            out = torch.cat([img1, img2], dim=3)

        else:
            # 宽度对齐
            target_w = min(W1, W2)

            img1 = F.interpolate(img1, size=(H1, target_w), mode="bilinear")
            img2 = F.interpolate(img2, size=(H2, target_w), mode="bilinear")

            # 拼接（高度方向）
            out = torch.cat([img1, img2], dim=2)

        # 转回 BHWC
        out = out.permute(0, 2, 3, 1)

        return io.NodeOutput(out)