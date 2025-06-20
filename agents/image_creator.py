from google.adk.agents import LlmAgent
from google import genai
from google.adk.tools import ToolContext
from google.adk.tools import load_artifacts

from google import genai
import google.genai.types as types
from agents.pdf_creator import text_to_pdf


async def generate_image(context: str, tool_context: ToolContext) -> dict:
    client = genai.Client()
    """Generates an image based on the prompt."""
    response = client.models.generate_images(
        model='imagen-4.0-generate-preview-06-06',
        prompt=context,
        config={'number_of_images': 1},
    )
    # if not response.generated_images:
    #     return {'status': 'failed'}
    image_bytes = response.generated_images[0].image.image_bytes
    await tool_context.save_artifact(
        'image.png',
        types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
    )
    return {
        'result': 'success',
        'detail': 'Image generated successfully and stored in artifacts.',
        'output_file': 'image.png',
    }

async def create_pdf(tool_context: ToolContext):
    image = await tool_context.load_artifact(filename="image.png")
    image_data = image.inline_data.data
    
    text = tool_context.state["edited"]
    pdf_bytes = text_to_pdf(image_data, text)

    await tool_context.save_artifact(
        'story.pdf',
        types.Part.from_bytes(data=pdf_bytes, mime_type='application/pdf'),
    ) 
    print("Artifact saved successfully")
    return {
       "status": "success",
       "filename": "story.pdf"
    }



class ImageCreatorAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            model="gemini-2.0-flash",
            name="image_creator",
            description="Generate image for child reading",
            instruction="""
                You are given a children's story (800 to 1000 words). Your task is to:
                1. Carefully read and understand the entire story.
                2. Write a single, concise image generation prompt that visually represents the main idea or central scene of the story. Make sure to keep it really short, avoid names in the story.
                3. This prompt will be used with the 'generate_image' tool, which creates illustrations from text prompts.
                4. The image prompt must capture the most engaging and representative moment or theme in the story — such as the emotional climax, a major event, or the story's main setting and characters.
                5. The image generation prompt should be vivid, descriptive, and suitable for a children's book illustration (e.g., colorful, imaginative, age-appropriate).
                6. Output only a single call to the 'generate_image' tool with your prompt as the only argument.
                7. You should also describe the image to the user, for example: This image depicts ...
                8. Create a pdf using the 'create_pdf' tool after image is created. Display the 'story.pdf' when it is created.
                Respond in the language ${language}

                Here is the story ${edited}
                """,
            tools=[generate_image, create_pdf, load_artifacts],
        )

