"""Originally from OpenAI's Swarm CLI example, modified for use in the CLI.
https://github.com/openai/swarm/blob/main/swarm/repl/repl.py
"""

from typing import Any
from swarm import Agent, Swarm

from utils.print_utils import (
    pretty_print_messages,
    process_and_print_streaming_response,
)


def run_loop(
    starting_agent: Agent,
    context_variables: dict | None = None,
    stream: bool = False,
    debug: bool = False,
    openai_client: Any | None = None,
    opening_message: str | None = None,
    **kwargs,
) -> None:
    client = Swarm(client=openai_client)
    print("Starting Swarm CLI 🐝")

    messages = []
    agent = starting_agent

    if opening_message:
        print(opening_message)

    while True:
        user_input = input("\033[90mUser\033[0m: ")
        messages.append({"role": "user", "content": user_input})

        response = client.run(
            agent=agent,
            messages=messages,
            context_variables=context_variables or {},
            stream=stream,
            debug=debug,
            **kwargs,
        )

        if stream:
            response = process_and_print_streaming_response(response)
        else:
            pretty_print_messages(response.messages)

        messages.extend(response.messages)
        agent = response.agent
