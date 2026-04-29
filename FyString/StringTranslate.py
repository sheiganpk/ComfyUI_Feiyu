import requests
from comfy_api.latest import io


class FyTranslateZH2EN(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="FyTranslateZH2EN",
            display_name="Fy中文转英文",
            category="飞羽/文本",

            inputs=[
                io.String.Input("text", multiline=True),
            ],

            outputs=[
                io.String.Output(),
            ],
        )

    @classmethod
    def execute(cls, text):

        if not text or text.strip() == "":
            return io.NodeOutput("")

        # ===== 这里用一个简单的翻译API（你可以替换）=====
        try:
            response = requests.post(
                "https://api.mymemory.translated.net/get",
                params={
                    "q": text,
                    "langpair": "zh|en"
                }
            )

            data = response.json()
            result = data["responseData"]["translatedText"]

        except Exception as e:
            result = f"ERROR: {str(e)}"

        return io.NodeOutput(result)


NODE_CLASS_MAPPINGS = {
    "FyTranslateZH2EN": FyTranslateZH2EN
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FyTranslateZH2EN": "中文转英文"
}