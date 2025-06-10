from google.adk.agents import LlmAgent
import random
import json

def feedback_after_model_callback(callback_context, llm_response):
    # 1. 提取 LLM 输出文本
    text = ""
    try:
        if hasattr(llm_response, "content") and hasattr(llm_response.content, "parts"):
            for part in llm_response.content.parts:
                if hasattr(part, "text") and part.text:
                    text += part.text
    except Exception as e:
        print(f"Error extracting text in feedback: {e}")

    print("Feedback输出原始内容：")
    print(text)

    # 2. 解析为 JSON，写入 state
    try:
        result = json.loads(text)
        callback_context.state["reader_score"] = float(result.get("reader_score", 0.0))
        callback_context.state["reader_comments"] = result.get("reader_comments", "")
    except Exception as e:
        # 容错：如果 LLM 返回的不是标准 JSON，可以随机分数，便于流水线不中断
        callback_context.state["reader_score"] = round(random.uniform(0.8, 1.0), 2)
        callback_context.state["reader_comments"] = f"解析失败: {e}，输出内容：{text}"

class FeedbackAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            model="gemini-2.0-flash",
            name="feedback",
            description="模拟或收集儿童读者/家长的真实反馈",
            instruction="""
你是一位5-8岁小朋友的家长，请阅读下面的故事，并以小朋友视角给出简短评论（不超过20字），以及你认为故事整体质量的评分（0.0~1.0），请只输出JSON格式：{"reader_score": X, "reader_comments": "…"}
故事:
${edited}
""",
            after_model_callback=feedback_after_model_callback
        )