from google.adk.agents import LlmAgent
from google import genai
from google.adk.tools import ToolContext

from google import genai


def generate_image(context: str, tool_context: ToolContext) -> dict:
    print("context is :", context)
    client = genai.Client()

    output_file = f"output-image-{tool_context.function_call_id}.png"

    image = client.models.generate_images(
        model="imagen-4.0-generate-preview-06-06",
        prompt=context,
    )

    image.generated_images[0].image.save(output_file)

    print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")
    return {"result": "success", "output_file": output_file}

class ImageCreatorAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            model="gemini-2.0-flash",
            name="image_creator",
            description="Generate image for child reading",
            instruction="""
                You are given a children's story (800 to 1000 words). Your task is to:
                1. Carefully read and understand the entire story.
                2. Write a single, concise image generation prompt that visually represents the main idea or central scene of the story.
                3. This prompt will be used with the 'generate_image' tool, which creates illustrations from text prompts.
                4. The image prompt must capture the most engaging and representative moment or theme in the story — such as the emotional climax, a major event, or the story's main setting and characters.
                5. The image generation prompt should be vivid, descriptive, and suitable for a children's book illustration (e.g., colorful, imaginative, age-appropriate).
                6. Output only a single call to the 'generate_image' tool with your prompt as the only argument.
                7. The 'generate_image' tool will return a result and an output_file, include the output_file in your final response
                Example Response: "Here is a image generation prompt that captures the essence of the story: ...
                The illustration of the story is located at output-image-adk-asdsdf-asdd-asdf-asdf-1239udasfl.png"
                """,
            tools=[generate_image],
        )

