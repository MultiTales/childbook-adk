import json
from google.adk.agents import LlmAgent

def language_detector_after_model_callback(callback_context, llm_response):
    text = ""
    try:
        if hasattr(llm_response, "content") and hasattr(llm_response.content, "parts"):
            for part in llm_response.content.parts:
                if hasattr(part, "text") and part.text:
                    text += part.text
    except Exception as e:
        print(f"Error extracting text in language detector: {e}")

    try:
        data = json.loads(text)
        callback_context.state["language"] = data.get("language", "en")
    except Exception as e:
        print(f"Error parsing JSON in language detector: {e}")
        callback_context.state["language"] = "en"

class LanguageDetectorAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            model="gemini-2.0-flash",
            name="language_detector",
            description="Detect the language of the user input",
            instruction="""
You are a language detector. You are given a text. You need to detect the language of the text.
You need to output the language of the text in the following format:
{"language": "en"}
""",
            after_model_callback=language_detector_after_model_callback,
        )
