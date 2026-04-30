import os
from comfy_api.latest import io
from langchain_openai import ChatOpenAI
import torch
from ..settings import get_api_key, pil_to_tensor, requestllm,extract_image_url,download_image


class FyGPT_Image_2(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="FyGPT_Image_2",
            display_name="Fy图片请求",
            category="飞羽/消耗积分",

            inputs=[
                io.String.Input("prompt", multiline=True),
                io.Combo.Input("model", display_name="模型", options=["香蕉2", "香蕉pro", "GPT-Image-2"]),
                io.Image.Input("image1", optional=True, display_name="图片1(可选)"),
                io.Image.Input("image2", optional=True, display_name="图片2(可选)"),
                io.Image.Input("image3", optional=True, display_name="图片3(可选)"),
                io.Image.Input("image4", optional=True, display_name="图片4(可选)"),
            ],

            outputs=[
                io.Image.Output(),
                io.String.Output("url"),
            ],
        )
    
    @classmethod
    def IS_CHANGED(cls, prompt, image1=None, image2=None, image3=None, image4=None):
        return float("nan")

    @classmethod
    def execute(cls, prompt, model, image1=None, image2=None, image3=None, image4=None):
         # 🛡️ 收集存在的图片
        images = []
        for img in [image1, image2, image3, image4]:
            if img is not None:
                images.append(img)
        if model == "香蕉2":
            model_name = "gemini-3-pro-image-preview-2k"
        elif model == "香蕉pro":
            model_name = "nano-banana-pro-2k"
        elif model == "GPT-Image-2":
            model_name = "gpt-image-2"

        result = requestllm(prompt, model_name, images)
        print("LLM返回结果:", result)
        image_url = extract_image_url(result)
        try:
            image = download_image(image_url)
            tensor = pil_to_tensor(image)
            return io.NodeOutput(tensor, image_url)
        except Exception as e:
            empty = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
            return io.NodeOutput(empty, image_url)
