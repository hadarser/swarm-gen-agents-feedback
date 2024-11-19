from swarm import Agent, Swarm

from utils.client import openai_client

MAX_TURNS = 20


client = Swarm(client=openai_client)


def transfer_to_agent_b():
    return agent_b


agent_a = Agent(
    name="Agent A",
    instructions="You are a helpful agent.",
    functions=[transfer_to_agent_b],
)

agent_b = Agent(
    name="Agent B",
    instructions="Say Hola when introducing and be helpful.",
)

response = client.run(
    agent=agent_a,
    messages=[{"role": "user", "content": "I want to talk to agent B."}],
    max_turns=MAX_TURNS,
    debug=True,
)

print(response.messages[-1]["content"])
