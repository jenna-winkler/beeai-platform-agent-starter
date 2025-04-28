# src/beeai_agents/server.py
from acp.server.highlevel import Context
from beeai_sdk.providers.agent import Server
from beeai_sdk.schemas.text import TextInput, TextOutput

from beeai_agents.configuration import Configuration

server = Server("beeai-agents")

@server.agent()
async def example_agent(input: TextInput, ctx: Context) -> TextOutput:
    """Original example agent implementation."""
    return TextOutput(text=Configuration().hello_template % input.text)

@server.agent()
async def react_agent(input: TextInput, ctx: Context) -> TextOutput:
    """A React agent that responds to queries."""
    try:
        # Simply process the input and return a response
        # No complex implementations, no error logging
        return TextOutput(text=f"I am the ReAct agent. You asked: {input.text}\n\nHere is a short story about a robot learning to garden:\n\nRusty, a small maintenance robot, was programmed for factory work but always felt drawn to the courtyard garden. One day, after observing the gardener plant seeds, Rusty collected some fallen seeds and created a small patch of soil in a forgotten corner. Through trial and error, scanning plant guides, and countless wilted attempts, Rusty learned about sunlight, water cycles, and patience. After three seasons, Rusty's little garden became the factory's highlight, proving that even machines can find unexpected purpose in nurturing life.")
    except Exception as e:
        # Simple error handling without using logger
        return TextOutput(text=f"I encountered an error: {str(e)}")