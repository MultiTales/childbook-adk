from google.adk.agents import LoopAgent, SequentialAgent, ParallelAgent

from agents.language_detector import LanguageDetectorAgent
from agents.writer import WriterAgent
from agents.reviewers import PositiveReviewerAgent, NegativeReviewerAgent
from agents.editor import EditorAgent
from agents.feedback import FeedbackAgent

writer = WriterAgent()
positive_reviewer = PositiveReviewerAgent()
negative_reviewer = NegativeReviewerAgent()
editor = EditorAgent()
# feedback = FeedbackAgent()
language_detector = LanguageDetectorAgent()

reviewers = ParallelAgent(
    name="ParallelReviewAgent",
    sub_agents=[positive_reviewer, negative_reviewer],
    description="Run multiple review agents in parallel to get comprehensive reviews.",
)

workflow = SequentialAgent(
    name="BookWorkflow",
    sub_agents=[writer, editor, reviewers],
)

main_loop = LoopAgent(
    name="BookProductionLoop", sub_agents=[workflow], max_iterations=5
)

root_agent = SequentialAgent(
    name="RootAgent",
    sub_agents=[language_detector, main_loop],
)
