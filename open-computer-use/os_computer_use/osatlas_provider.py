from gradio_client import Client, handle_file
from os_computer_use.logging import logger
from os_computer_use.grounding import extract_bbox_midpoint

class OSAtlasProvider:
    def __init__(self):
        self.client = Client("maxiw/OS-ATLAS")

    def call(self, prompt, image_data):
        result = self.client.predict(
            image=handle_file(image_data),
            text_input=prompt + "\nReturn the response in the form of a bbox",
            model_id="OS-Copilot/OS-Atlas-Base-7B",
            api_name="/run_example",
        )
        position = extract_bbox_midpoint(result[1])
        image_url = result[2]
        logger.log(f"bbox {image_url}", "gray")
        return position
