from swarm import Agent, Swarm
from utils.client import openai_client
from utils.run_loop import run_loop

from swarm.types import Result
from typing import Dict, List

MAX_TURNS = 20
MODEL = "gpt-4o-mini"


def create_question_analyzer():
    """Creates the QuestionAnalyzer agent that understands the feedback question"""

    def analyze_question(context_variables: Dict) -> Result:
        context_variables["question_analyzed"] = True
        context_variables["questions_generated"] = (
            False  # Flag to indicate we need to generate questions
        )
        context_variables["current_question_index"] = (
            -1
        )  # Will increment to 0 for first question
        context_variables["questions"] = []  # Will store generated questions
        context_variables["conversation_ended"] = (
            False  # Flag to indicate the conversation has ended
        )
        return Result(
            value="Analysis complete",
            agent=interview_agent,
            context_variables=context_variables,
        )

    def end_conversation(context_variables: Dict) -> Result:
        """End the conversation if there are no more questions to ask."""
        context_variables["conversation_ended"] = True
        return Result(
            value="Conversation ended",
            agent=None,
            context_variables=context_variables,
        )

    return Agent(
        name="QuestionAnalyzer",
        instructions="""You are an expert at analyzing workplace feedback questions. 
        Your role is to understand the core aspects of the feedback question that needs to be answered.
        Consider what areas of performance, behavior, or impact would be most relevant to address.
        After analysis, hand off to the interview agent.
        If the user indicates the conversation is over, end the conversation.""",
        model=MODEL,
        functions=[analyze_question, end_conversation],
    )


def create_interview_agent():
    """Creates the InterviewAgent that generates and asks relevant feedback questions"""

    def generate_questions(
        context_variables: Dict,
        question_1: str,
        question_2: str,
        question_3: str | None = None,
    ) -> Result:
        """Generate relevant questions based on the original feedback question. You should generate 2-3 questions."""
        questions = [question_1, question_2]
        if question_3:
            questions.append(question_3)
        questions.append(
            "Would you like to add any other specific examples or observations about your coworker?"
        )

        context_variables["questions"] = questions
        context_variables["questions_generated"] = True
        return Result(
            value="Questions generated",
            agent=interview_agent,
            context_variables=context_variables,
        )

    def ask_next_question(context_variables: Dict) -> Result:
        """Ask the next question in the sequence."""
        questions = context_variables.get("questions", [])
        current_index = context_variables["current_question_index"]
        next_index = current_index + 1

        if next_index >= len(questions):
            # We've asked all questions, move to feedback analyzer
            context_variables["interview_complete"] = True
            return Result(
                value="Interview complete",
                # agent=feedback_analyzer,  # TODO: Add feedback analyzer agent
                context_variables=context_variables,
            )

        # Return next question and update index
        context_variables["current_question_index"] = next_index
        return Result(
            value=questions[next_index],
            agent=interview_agent,
            context_variables=context_variables,
        )

    def process_response(context_variables: Dict, response: str) -> Result:
        """Process the user's response and store it."""
        responses = context_variables.get("responses", [])
        current_index = context_variables["current_question_index"]

        # Store the response with its corresponding question
        responses.append(
            {
                "question": context_variables["questions"][current_index],
                "response": response,
            }
        )

        context_variables["responses"] = responses
        return Result(
            value="Response processed",
            agent=interview_agent,
            context_variables=context_variables,
        )

    return Agent(
        name="InterviewAgent",
        instructions="""You are an expert at gathering specific, actionable feedback about coworkers.
        
        When generating questions:
        1. Consider the original feedback question carefully
        2. Generate 2-3 specific, open-ended questions that will help gather relevant examples and insights
        3. Make questions clear and focused on observable behaviors or outcomes
        4. Ensure questions cover different aspects of the feedback area
        5. Refer to the subject of the feedback as 'your coworker'
        
        When asking questions:
        1. Ask one question at a time
        2. Process and acknowledge each response
        3. Use the response content to inform the context of subsequent questions
        4. Be professional and courteous
        
        If you haven't generated questions yet:
        1. Call generate_questions() first
        
        If you have generated questions:
        1. Call ask_next_question() to get the next question
        2. After receiving a response, call process_response()
        3. Then call ask_next_question() again until all questions are asked
        
        Remember to maintain a natural conversation flow while gathering specific, relevant information.""",
        model=MODEL,
        functions=[generate_questions, ask_next_question, process_response],
    )


# Create the agents
analysis_agent = create_question_analyzer()
interview_agent = create_interview_agent()

if __name__ == "__main__":
    opening_message = "Hello user, I am going to help you with analyzing the feedback question. Please provide the feedback question you would like me to analyze."
    opening_message = f"\033[96m{opening_message}\033[0m"

    run_loop(
        analysis_agent,
        stream=False,
        openai_client=openai_client,
        opening_message=opening_message,
        max_turns=MAX_TURNS,
        debug=True,
    )
