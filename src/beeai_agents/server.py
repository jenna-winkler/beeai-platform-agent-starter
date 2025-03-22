import asyncio

from acp.server.highlevel import Server, Context
from beeai_sdk.providers.agent import run_agent_provider
from beeai_sdk.schemas.metadata import UiDefinition, UiType
from beeai_sdk.schemas.text import TextInput, TextOutput
from travel_advisor import main as run_travel_advisor

async def run():
    server = Server("travel-advisor")

    @server.agent(
        name="travel-advisor",
        description="Travel advisor for recommendations",
        input=TextInput,
        output=TextOutput,
        ui=UiDefinition(type=UiType.hands_off, userGreeting="Where and when are you traveling?"),
    )
    async def travel_advisor_agent(input: TextInput, ctx: Context) -> TextOutput:
        await ctx.report_agent_run_progress(delta=TextOutput(text="Planning your trip..."))
        try:
            result = await run_travel_advisor(input.text, None)
            return TextOutput(text=result)
        except Exception as e:
            return TextOutput(text=f"Error: {str(e)}")

    await run_agent_provider(server)

def main():
    asyncio.run(run())