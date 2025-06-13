from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest


def writer_before_model_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
):
    state = callback_context.state

    # 拼接历史反馈
    feedback = ""
    if (
        state.get("positive_comment") is not None
        and state.get("negative_comment")
        and state.get("draft")
    ):
        feedback = f"""
【修订提示】
上轮故事积极评审意见：{state['positive_comment']}
上轮故事消极评审意见：{state['negative_comment']}
上轮草稿如下：
```
{state['draft']}
```
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
            model="gemini-2.5-pro-preview-06-05",
            name="writer",
            before_model_callback=writer_before_model_callback,
            after_model_callback=writer_after_model_callback,
            description="写作有趣儿童读物的作家",
            instruction="""
你是一名儿童文学作家，请根据以下故事提纲或主题创作一段有趣的儿童故事，字数在150-200字之间。目标读者年龄在8-12岁之间。
你总是在写作前提前规划小说的细纲。你使用流畅的语言进行写作，避免在文章里使用括号来标注。但是你可以在文章中间 **提前** 思考剧情的发展方向，并把思考内容写进单独的 <!-- 注释块 --> 中，放在你要写的情节之前，避免污染行文。如果你在写出某段内容之后发现落下了内容，请在随后使用注释块注明如何修改，而不是直接写在原文里。你编写的内容会被直接提供给读者，因此在进行修改时，你应当假设读者没有读过之前的版本。

比如：
* 使用注释块来提前规划想表达的人物心理以及可能的表达方式。
* 在编写一段情节之前，先规划情节的作用以及思考可能的发展方向。

请直接输出正文，不要带任何说明。
请按照用给出的要求完成创作。每次输出都需要完整给出完整文章。
""",
        )
