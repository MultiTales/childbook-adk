from google.adk.agents import LoopAgent, SequentialAgent

from agents.writer import WriterAgent
from agents.reviewer import ReviewerAgent
from agents.editor import EditorAgent
from agents.feedback import FeedbackAgent

writer = WriterAgent()
reviewer = ReviewerAgent()
editor = EditorAgent()
feedback = FeedbackAgent()


workflow = SequentialAgent(
    name="BookWorkflow",
    sub_agents=[writer, reviewer, editor, feedback],
)

root_agent = LoopAgent(
    name="BookProductionLoop",
    sub_agents=[workflow],
    max_iterations=5
)
