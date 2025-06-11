from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest


def writer_before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    state = callback_context.state

    # 拼接历史反馈
    feedback = ""
    if state.get("positive_comment") is not None and state.get("negative_comment") and state.get("draft"):
        feedback = f"""
【修订提示】
上轮故事积极评审意见：{state['positive_comment']}
上轮故事消极评审意见：{state['negative_comment']}
上轮草稿如下：
{state['draft']}
请针对上述反馈进行优化改写。请保存积极评审意见中的优势。并且改进消极评审意见中提及的不足
"""
    # 如果有反馈，就插到 instruction 前面，否则保持原样
    if feedback:
        llm_request.append_instructions([feedback])

def writer_after_model_callback(callback_context, llm_response):
    text = ""
    try:
        if hasattr(llm_response, "content") and hasattr(llm_response.content, "parts"):
            for part in llm_response.content.parts:
                if hasattr(part, "text") and part.text:
                    text += part.text
    except Exception as e:
        print(f"Error extracting text: {e}")
    callback_context.state["draft"] = text.strip()

class WriterAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            model="gemini-2.0-flash",
            name="writer",
            before_model_callback = writer_before_model_callback,
            after_model_callback=writer_after_model_callback,
            description="自动生成有趣儿童读物的作家",
            instruction="""
你是一名儿童文学作家，请根据以下故事提纲或主题创作一段有趣的儿童故事，字数在150-200字之间。请直接输出正文，不要带任何说明。
请按照用给出的要求完成创作。每次输出都需要完整给出完整文章。
"""
        )
