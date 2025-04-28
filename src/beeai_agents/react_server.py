# src/beeai_agents/react_server.py
from acp.server.highlevel import Context
from beeai_sdk.providers.agent import Server
from beeai_sdk.schemas.text import TextInput, TextOutput

from beeai_framework.memory import BaseMemory
from beeai_framework.backend.chat import ChatModel
from beeai_framework.backend.message import Message

from beeai_agents.react_agent import ReActAgent

server = Server("beeai-react-agents")

@server.agent()
async def react_agent(input: TextInput, ctx: Context) -> TextOutput:
    """A ReAct agent that can use tools to solve problems."""
    
    try:
        # Create a concrete implementation of BaseMemory
        class SimpleMemory(BaseMemory):
            def __init__(self):
                self._messages = []
                
            async def add(self, message: Message) -> None:
                self._messages.append(message)
                
            async def get_all(self) -> list[Message]:
                return self._messages.copy()
                
            async def clear(self) -> None:
                self._messages = []
                
            async def delete(self, message_id: str) -> None:
                self._messages = [msg for msg in self._messages if getattr(msg, 'id', None) != message_id]
                
            async def reset(self) -> None:
                self._messages = []
                
            @property
            def messages(self) -> list[Message]:
                return self._messages
        
        # Initialize the memory
        memory = SimpleMemory()
        
        # Create a concrete implementation of ChatModel
        # We need this since we can't instantiate the abstract class
        class SimpleChatModel(ChatModel):
            @property
            def model_id(self) -> str:
                return "simple-model"
                
            @property
            def provider_id(self) -> str:
                return "simple-provider"
                
            async def _create(self, *args, **kwargs):
                # This is a placeholder implementation
                return {"message": {"content": f"I processed: {input.text}"}}
                
            async def _create_stream(self, *args, **kwargs):
                # Yield a simple response
                yield {"message": {"content": f"I processed: {input.text}"}}
                
            async def _create_structure(self, *args, **kwargs):
                # Another placeholder
                return {"message": {"content": f"I processed: {input.text}"}}
        
        # Initialize our simple chat model
        llm = SimpleChatModel()
        
        # Empty tools list for now
        tools = []
        
        # Create the agent with minimal configuration
        agent = ReActAgent(
            llm=llm,
            tools=tools,
            memory=memory,
            stream=True
        )
        
        # Run the agent with the input
        run = agent.run(input.text)
        result = await run.wait()
        
        # Return the result if available
        if result and hasattr(result, 'result') and hasattr(result.result, 'content'):
            return TextOutput(text=result.result.content)
        else:
            # Fallback if result is not in expected format
            return TextOutput(text=f"Processed: {input.text}")
            
    except Exception as e:
        # Log the error for debugging
        ctx.logger.error(f"Error in ReAct agent: {str(e)}")
        # Provide a fallback response
        return TextOutput(text=f"I encountered an error while processing your request: {str(e)}")