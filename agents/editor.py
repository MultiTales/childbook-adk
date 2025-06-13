from google.adk.agents import LlmAgent


def editor_after_model_callback(callback_context, llm_response):
    # 1. 提取大模型输出的文本
    text = ""
    try:
        if hasattr(llm_response, "content") and hasattr(llm_response.content, "parts"):
            for part in llm_response.content.parts:
                if hasattr(part, "text") and part.text:
                    text += part.text
    except Exception as e:
        print(f"Error extracting text in editor: {e}")

    print("Editor输出润色后文本：")
    print(text)

    # 2. 写入 state["edited"] 供下游 agent 用
    callback_context.state["edited"] = text.strip()


class EditorAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            model="gemini-2.5-flash-preview-05-20",
            name="editor",
            description="润色并提升故事文本质量的编辑",
            instruction="""
你是一名儿童故事编辑，请对下列草稿进行润色和优化，使其表达更清晰、更符合8-12岁儿童阅读习惯。
目标：
* 移除所有注释块。在必要时根据注释块来修改文本。
* 请输出润色后的完整故事正文，不要加任何说明。

草稿:
```
${draft}
```
""",
            after_model_callback=editor_after_model_callback,
        )
