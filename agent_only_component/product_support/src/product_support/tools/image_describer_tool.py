from crewai.tools import BaseTool
from PIL import Image
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class ImageDescriberTool(BaseTool):
    name: str = "Image Describer Tool"
    description: str = (
        "This tool analyzes washing machine images from the '/images' folder "
        "and returns a descriptive paragraph (3-5 sentences per image)."
    )

    def _run(self) -> str:
        print("Checking for image files...")
        image_folder = "/mnt/e/Farhaan-work/Projects/Agentic Product Support/product_support/src/product_support/user_inputs/images"
        image_paths = [
            os.path.join(image_folder, f)
            for f in os.listdir(image_folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        if len(image_paths) == 0:
            return "No images provided for description."
        
        description = ""
        model = genai.GenerativeModel("gemini-2.0-flash")
        for image_file in image_paths:
            image = Image.open(image_file)
            response = model.generate_content(
                contents=[
                    """Your task is to analyze the image given and describe the image effectively.
                    Use it to identify the content of the washing machine and refine your response accordingly.
                    Make sure to have a description such that the next prompt will be from the user based on the image. 
                    Output the description in a single paragraph with 3-5 sentences.""",
                    image,
                ]
            )
            description += response.text.strip() + "\n"

        return description.strip()
        