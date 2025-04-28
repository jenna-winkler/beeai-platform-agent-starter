# src/beeai_agents/server.py
from acp.server.highlevel import Context
from beeai_sdk.providers.agent import Server
from beeai_sdk.schemas.text import TextInput, TextOutput

from beeai_framework.backend.chat import ChatModel
from beeai_framework.memory import InMemoryMemory
from beeai_framework.tools.calculator import Calculator
from beeai_framework.tools.search import Search

from beeai_agents.configuration import Configuration
from beeai_agents.react_agent import ReActAgent

server = Server("beeai-agents")

@server.agent()
async def react_agent(input: TextInput, ctx: Context) -> TextOutput:
    """A ReAct agent that can use tools to solve problems."""
    
    # Initialize the LLM
    llm = ChatModel.from_anthropic("claude-3-sonnet-20240229")
    
    # Initialize memory
    memory = InMemoryMemory()
    
    # Initialize tools
    tools = [
        Calculator(),
        Search()
    ]
    
    # Create the agent
    agent = ReActAgent(
        llm=llm,
        tools=tools,
        memory=memory,
        stream=True
    )
    
    # Run the agent with the input
    run = agent.run(input.text)
    result = await run.wait()
    
    # Return the result
    return TextOutput(text=result.result.content)

# Keep the example agent for reference
@server.agent()
async def example_agent(input: TextInput, ctx: Context) -> TextOutput:
    """Original example agent implementation."""
    return TextOutput(text=Configuration().hello_template % input.text)
