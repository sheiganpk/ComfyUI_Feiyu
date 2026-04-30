from comfy_api.latest import io

class FyGetSize(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="Feiyu Image Get Size",
            display_name="Fy获取图像尺寸",
            category="飞羽/图像",
            inputs=[
                io.Image.Input("image", "图像")
            ],
            outputs=[
                io.Int.Output("width", "宽"),
                io.Int.Output("height", "高")
            ],
        )

    @classmethod
    def execute(cls, image):
        B, H, W, C = image.shape

        return io.NodeOutput(W, H)