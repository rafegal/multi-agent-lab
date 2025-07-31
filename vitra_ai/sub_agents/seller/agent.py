from google.adk.agents import Agent, LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig


from vitra_ai.sub_agents.seller import prompt
from vitra_ai.sub_agents.seller.tools import (
    generate_order,
    generate_order_detail,
    generate_invoice,
    update_stock,
)

create_order = LlmAgent(
    model=LiteLlm("anthropic/claude-3-5-sonnet-20240620"),
    name="create_order",
    description="""Cria uma ordem e insere produtos na ordem""",
    instruction=prompt.CREATE_ORDER_INSTR,
    tools=[generate_order, generate_order_detail],
)

billing = LlmAgent(
    model=LiteLlm("anthropic/claude-3-5-sonnet-20240620"),
    name="billing",
    description="""Criar fatura com base em ordem já criada.""",
    instruction=prompt.BILLING_INSTR,
    tools=[generate_invoice],
)

manage_stock = LlmAgent(
    model=LiteLlm("anthropic/claude-3-5-sonnet-20240620"),
    name="manage_stock",
    description="""Faz a baixa no estoque.""",
    instruction=prompt.MANAGE_STOCK_INSTR,
    tools=[update_stock],
)


seller_agent = LlmAgent(
    model=LiteLlm("anthropic/claude-3-5-sonnet-20240620"),
    name="seller_agent",
    description="""Faça o processamento do pedido do cliente, criando ordem, os detalhes da ordem e dando baixa no estoque e gerando fatura.""",
    instruction=prompt.SELLER_INSTR,
    tools=[
        AgentTool(agent=create_order),
        AgentTool(agent=billing),
        AgentTool(agent=manage_stock),
    ],
    generate_content_config=GenerateContentConfig(temperature=0.0, top_p=0.5),
)
