import json
import re
from google.adk.agents import LlmAgent


def extract_comment_and_score(llm_response):
    text = ""
    try:
        if hasattr(llm_response, "content") and hasattr(llm_response.content, "parts"):
            for part in llm_response.content.parts:
                if hasattr(part, "text") and part.text:
                    text += part.text
    except Exception as e:
        print(f"Error extracting text in reviewer: {e}")

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        json_str = match.group(0)
        result = json.loads(json_str)
    else:
        result = json.loads(text)
    return result.get("comment", ""), float(result.get("score", 0.0))


def positive_reviewer_after_model_callback(callback_context, llm_response):
    (
        callback_context.state["positive_comment"],
        callback_context.state["positive_score"],
    ) = extract_comment_and_score(llm_response)


def negative_reviewer_after_model_callback(callback_context, llm_response):
    (
        callback_context.state["negative_comment"],
        callback_context.state["negative_score"],
    ) = extract_comment_and_score(llm_response)


class PositiveReviewerAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            model="gemini-2.0-flash",
            name="positive_reviewer",
            description="评审儿童故事质量并给积极评语",
            instruction="""
你是一名儿童故事专家，请根据 rubric 对儿童故事草稿进行积极评价，并为文章打分。
请你始终以首次阅读者的视角，真诚、热情地指出故事中值得肯定和保留的亮点，帮助作者明确哪些地方做得好。禁止任何负面或批评性评价。

输出必须为标准 JSON 格式。

返回的JSON包含两个字段：
{
    "comment": [
        // 用简明扼要的短句/项目符号列出故事最值得肯定和保留的优点、亮点，3-5条最佳
    ],
    "score": 数字 // 整体正面评价分数，范围在 0~1 之间，1 为极好，0.7 以上为良好，0.5 以下为一般
}

rubric（评分标准）如下：
1. 故事结构是否完整、有条理？
2. 语言是否生动有趣，适合儿童？
3. 是否包含积极正面的价值观？
4. 角色设定是否有趣、富有创意？

故事草稿如下：
${edited}
""",
            after_model_callback=positive_reviewer_after_model_callback,
        )


class NegativeReviewerAgent(LlmAgent):
    def __init__(self):
        super().__init__(
            model="gemini-2.0-flash",
            name="negative_reviewer",
            description="批判性评审儿童故事质量，指出不足并给出分数",
            instruction="""
你是一名儿童故事领域的专业批评家，请根据 rubric 对以下草稿进行严格、批判性的审查，重点指出故事中存在的不足、弱点或可以明显改进的地方。
禁止正面鼓励性评论，全部内容必须直言不讳地指出问题。

输出必须为标准 JSON 格式。

返回的JSON包含两个字段：
{
    "comment": [
        // 用简明扼要的短句/项目符号列出故事中存在的不足、缺点、改进建议，3-5条最佳
    ],
    "score": 数字 // 整体负面评价分数，范围在 0~1 之间，1 为极好，0.7 以上为良好，0.5 以下为一般，0.5 以下为较差
}

rubric（评分标准）如下：
1. 故事结构是否存在混乱、不完整或缺乏条理？
2. 语言是否生硬、枯燥或不适合儿童？
3. 是否缺少积极的价值观或存在不良暗示？
4. 角色是否刻板单一或缺乏吸引力？
5. 其他你认为的任何明显不足或可以改进之处

故事草稿如下：
${edited}
""",
            after_model_callback=negative_reviewer_after_model_callback,
        )
