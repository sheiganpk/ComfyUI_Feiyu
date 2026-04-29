from comfy_api.latest import io
import torch

class FeiyuTest(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="FeiyuTest2",
            display_name="Feiyu Test3",
            category="飞羽",
            inputs=[
                io.Latent.Input("latent"),
                io.Float.Input("scale", default=1.0)
            ],
            outputs=[
                io.Latent.Output(),
            ],
        )

    @classmethod
    def execute(cls, latent, scale):
        samples = latent["samples"] * scale
        noise = torch.randn_like(samples) * scale
        samples = samples + noise
        samples = samples.clamp(-10, 10)
        latent["samples"] = samples
        return io.NodeOutput(latent)