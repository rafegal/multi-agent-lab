from google.adk.agents import Agent

from vitra_ai import prompt

from vitra_ai.sub_agents.shop_mate.agent import attendant_agent
from vitra_ai.sub_agents.seller.agent import seller_agent
from vitra_ai.sub_agents.health_mate.agent import health_mate

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Um atendente de vendas e ajuda com cuidados do corpo com uso de multiplos sub-agents",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        attendant_agent,
        seller_agent,
        health_mate,
    ],
)
