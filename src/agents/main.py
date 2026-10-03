"""Entry point: ask DevMind a question using the tool-calling agent."""

from agent import Agent
from prompts import SYSTEM_PROMPT

QUESTION = (
    "Find the implementation of hybrid retrieval in this project. "
    "Inspect the relevant source files and explain how dense retrieval, "
    "BM25, RRF, and reranking are connected in the actual implementation. "
    "Do not answer until you have inspected the relevant source code."
)

def main() -> None:
    agent = Agent(system_prompt=SYSTEM_PROMPT)
    answer = agent.ask(QUESTION)
    print("Final answer:", answer)


if __name__ == "__main__":
    main()