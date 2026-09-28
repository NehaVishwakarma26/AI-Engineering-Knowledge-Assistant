"""A minimal tool-calling agent loop built on the Ollama chat API."""

import json
from dataclasses import dataclass, field

from ollama import chat, ChatResponse

from config import MODEL_NAME
from tools import available_functions, tool_schemas, TOOLS

def _is_error(tool_message: dict) -> bool:
    """Return True if a tool result contains an error."""
    try:
        content = json.loads(tool_message["content"])
        return isinstance(content, dict) and "error" in content
    except (json.JSONDecodeError, TypeError):
        return False

@dataclass
class Agent:
    """Repeatedly calls the model and dispatches any tool calls it makes,
    until it responds with a final answer (no further tool calls) or
    `max_turns` is reached.
    """

    model: str = MODEL_NAME
    system_prompt: str = ""
    verbose: bool = True
    messages: list = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.system_prompt:
            self.messages.append({"role": "system", "content": self.system_prompt})

    def _log(self, *args) -> None:
        if self.verbose:
            print(*args)

    def _dispatch_tool_call(self, tool_call) -> dict:
        """Validate and execute one tool call, returning a tool-role message."""
        name = tool_call.function.name
        arguments = tool_call.function.arguments

        if name not in available_functions:
            error = {"error": f"Tool '{name}' is not available"}
            return {"role": "tool", "tool_name": name, "content": json.dumps(error)}

        required = tool_schemas[name]["required"]
        missing = [arg for arg in required if arg not in arguments]
        if missing:
            error = {"error": "Missing required arguments", "missing": missing}
            return {"role": "tool", "tool_name": name, "content": json.dumps(error)}

        self._log(f"Calling {name} with arguments {arguments}")
        try:
            result = available_functions[name](**arguments)
        except Exception as exc:  # a crashing tool shouldn't kill the whole loop
            error = {"error": f"Tool '{name}' raised an exception: {exc}"}
            return {"role": "tool", "tool_name": name, "content": json.dumps(error)}

        self._log(f"Result: {result}")
        return {"role": "tool", "tool_name": name, "content": json.dumps(result)}

    def ask(self, question: str, max_turns: int = 10,max_nudges:int=2) -> str:
        """Send a user question through the agent loop and return the final answer."""
        self.messages.append({"role": "user", "content": question})
        
        last_round_failed=False
        nudges=0
        
        for _ in range(max_turns):
            response: ChatResponse = chat(
                model=self.model,
                messages=self.messages,
                tools=TOOLS,
                think=False,
            )
            self.messages.append(response.message)
            self._log("Thinking:", response.message.thinking)
            self._log("Content:", response.message.content)

            if not response.message.tool_calls:
                if last_round_failed and nudges<max_nudges:
                    nudges+=1
                    self.messages.append({
                    "role":"user",
                    "content":(
                        "Your last tool call failed. Do not answer from assumptions. Retry with a corrected argument, such as an exact path from list_files."
                    )
                    })
                    continue
                return response.message.content
            
            results=[self._dispatch_tool_call(tc) for tc in response.message.tool_calls]
            self.messages.extend(results)
            last_round_failed=any(_is_error(r) for r in results)
            
        return "Stopped: reached max_turns without a final answer"
            


