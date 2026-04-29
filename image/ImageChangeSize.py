from comfy_api.latest import io
import torch.nn.functional as F

class FyChangeSize(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="Feiyu Image Change Size",
            display_name="Fy图像缩放",
            category="飞羽/图像",
            inputs=[
                io.Image.Input("image", "图像"),
                io.Int.Input("target_width","宽", default=1920, min=64, max=4096),
                io.Int.Input("target_height","高", default=1080, min=64, max=4096),
                io.Combo.Input(
                    "mode", 
                    display_name = "模式",
                    options=["等比缩放，完整显示", "等比缩放，裁剪多余", "拉伸尺寸"]
                )
            ],
            outputs=[
                io.Image.Output(),
            ],
        )

    @classmethod
    def execute(cls, image, target_width,target_height,mode):
        B, H, W, C = image.shape

        # 转 BCHW
        image = image.permute(0, 3, 1, 2)

        # ===== stretch（直接拉伸）=====
        if mode == "拉伸尺寸":
            resized = F.interpolate(
                image,
                size=(target_height, target_width),
                mode="bilinear"
            )

        else:
            scale_w = target_width / W
            scale_h = target_height / H

            # ===== contain =====
            if mode == "等比缩放，完整显示":
                scale = min(scale_w, scale_h)

            # ===== cover =====
            elif mode == "等比缩放，裁剪多余":
                scale = max(scale_w, scale_h)

            new_w = int(W * scale)
            new_h = int(H * scale)

            resized = F.interpolate(
                image,
                size=(new_h, new_w),
                mode="bilinear"
            )

            # ===== cover 需要裁剪 =====
            if mode == "等比缩放，裁剪多余":
                start_h = (new_h - target_height) // 2
                start_w = (new_w - target_width) // 2

                resized = resized[
                    :,
                    :,
                    start_h:start_h + target_height,
                    start_w:start_w + target_width
                ]

        # 转回 BHWC
        resized = resized.permute(0, 2, 3, 1)

        return io.NodeOutput(resized)