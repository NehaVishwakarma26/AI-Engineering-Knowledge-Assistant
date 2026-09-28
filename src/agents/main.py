"""Entry point: ask DevMind a question using the tool-calling agent."""

from agent import Agent
from prompts import SYSTEM_PROMPT

QUESTION = (
    "Compare the reranking implementation in this project with the reranking architecture described in the knowledge base. Inspect the actual project implementation."
)


def main() -> None:
    agent = Agent(system_prompt=SYSTEM_PROMPT)
    answer = agent.ask(QUESTION)
    print("Final answer:", answer)


if __name__ == "__main__":
    main()