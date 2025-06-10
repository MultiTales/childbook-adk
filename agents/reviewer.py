from google.adk.agents import LlmAgent
import json

def reviewer_after_model_callback(callback_context, llm_response):
    print("############")
    # 1. 提取大模型返回的文本内容
    text = ""
    try:
        if hasattr(llm_response, "content") and hasattr(llm_response.content, "parts"):
            for part in llm_response.content.parts:
                if hasattr(part, "text") and part.text:
                    text += part.text
    except Exception as e:
        print(f"Error extracting text in reviewer: {e}")

    print("Reviewer输出原始内容：")
    print(text)

    # 2. 尝试解析为 JSON，并写入 state
    try:
        result = json.loads(text)
        callback_context.state["review_score"] = float(result.get("score", 0.0))
        callback_context.state["review_notes"] = result.get("notes", "")
    except Exception as e:
        # 容错处理
        callback_context.state["review_score"] = 0.0
        callback_context.state["review_notes"] = f"评分解析失败: {e}，输出内容：{text}"


class ReviewerAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            model="gemini-2.0-flash",
            name="reviewer",
            description="评审儿童故事质量并给出分数和评语",
            instruction="""
你是一名儿童故事专家，请根据rubric对草稿进行评审，并只输出JSON：{"score": X, "notes": "简要评语"}
rubric:
1. 语言是否流畅；
2. 故事结构是否完整；
3. 是否适合5-8岁儿童阅读；
请严格输出JSON格式。
草稿如下：
${draft}
""",
            after_model_callback=reviewer_after_model_callback
        )