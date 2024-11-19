from swarm import Agent, Swarm
from utils.client import openai_client
from utils.run_loop import run_loop
from utils.print_utils import process_and_print_streaming_response, pretty_print_messages

from swarm.types import Result
from typing import Dict, List

MAX_TURNS = 20
MODEL = "gpt-4o-mini"


def create_question_analyzer():
    """Creates the QuestionAnalyzer agent that understands the feedback question"""

    def analyze_question(context_variables: Dict) -> Result:
        return Result(
            value="Analysis complete",
            # agent=interview_agent,  # TODO: Add the interview agent
            context_variables={
                **context_variables,
                "question_analyzed": True,
                "questions_generated": False,  # Flag to indicate we need to generate questions
                "current_question_index": -1,  # Will increment to 0 for first question
                "questions": [],  # Will store generated questions
            },
        )

    return Agent(
        name="QuestionAnalyzer",
        instructions="""You are an expert at analyzing workplace feedback questions. 
        Your role is to understand the core aspects of the feedback question that needs to be answered.
        Consider what areas of performance, behavior, or impact would be most relevant to address.
        After analysis, hand off to the interview agent.""",
        model=MODEL,
        functions=[analyze_question],
    )


# Create the agents
analysis_agent = create_question_analyzer()

if __name__ == "__main__":
    opening_message = "Hello user, I am going to help you with analyzing the feedback question. Please provide the feedback question you would like me to analyze."
    opening_message = f"\033[96m{opening_message}\033[0m"

    run_loop(
        analysis_agent,
        stream=False,
        openai_client=openai_client,
        opening_message=opening_message,
        max_turns=MAX_TURNS,
    )
