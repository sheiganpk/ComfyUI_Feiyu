import io
import os
import folder_paths
from langchain_openai import ChatOpenAI
from PIL import Image
import re
import requests

def download_image(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": url,  # 很关键
    }
    resp = requests.get(url, headers=headers, timeout=20)
    print("状态码:", resp.status_code)
    print("Content-Type:", resp.headers.get("Content-Type"))
    resp.raise_for_status()
    if "image" not in resp.headers.get("Content-Type", ""):
        print("返回内容前100字节:", resp.content[:100])
        raise ValueError("不是图片")
    img = Image.open(io.BytesIO(resp.content))
    print("PIL格式:", img.mode, img.size)
    return img.convert("RGB")

def pil_to_tensor(img):
    import numpy as np
    import torch

    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.ascontiguousarray(arr)

    tensor = torch.from_numpy(arr).unsqueeze(0)
    return tensor

def extract_image_url(text: str):
    # 提取Markdown格式中的图片URL，格式为 ![alt text](image_url)
    pattern = r'!\[.*?\]\((.*?)\)'
    match = re.search(pattern, text)

    if match:
        return match.group(1)
    else:
        return "生图失败"

def get_api_key():
    # 尝试从comfy.settings.json中读取API Key
    try:
        import json, os
        path = os.path.join(folder_paths.base_path, "user/default", "comfy.settings.json")

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("feiyu_api_key", "")
    except Exception as e:
        print("读取设置失败:", e)
    return ""

def tensor_to_base64(tensor):
    # 将PyTorch张量转换为PIL图像，然后编码为Base64字符串
    import base64
    from io import BytesIO
    from PIL import Image
    import numpy as np
    img = (tensor[0].cpu().numpy() * 255).astype("uint8")
    pil = Image.fromarray(img)
    buffer = BytesIO()
    pil.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def requestllm(prompt, model="gemini-3.1-flash-lite-preview-thinking-medium", images=[]):
        api_key = get_api_key()
        # ===== 1. 选择API Key =====
        key = api_key.strip() if api_key else ""
        if not key:
            key = os.environ.get("ZhenZhenApiKey", "")
        # ===== 2. 没有key直接返回 =====
        if not key:
            return io.NodeOutput("没有提供API Key，请到https://ai.t8star.cn/register?aff=nCZC115614 获取APIKey，然后在设置页面输入")
        # ===== 3. 请求LLM =====
        try:
            llm = ChatOpenAI(
                api_key=key,
                base_url="https://ai.t8star.cn/v1",
                model= model, 
                temperature=0.2
            )
            content = [{"type": "text", "text": prompt}]
            for idx, img in enumerate(images):
                bs64 = tensor_to_base64(img)
                content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{bs64}", "detail":"high"}})
            #print("请求内容:", content)
            response = llm.invoke([{"role": "user", "content": content}])
            result = response.content
        except Exception as e:
            result = f"ERROR: {str(e)}"
        return result