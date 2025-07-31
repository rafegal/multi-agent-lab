"""Agente especialiazado em ajudar o cliente a encontrar produtos adequados às suas necessidades."""

from google.adk.agents import Agent, LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig

from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from vitra_ai.sub_agents.shop_mate import prompt


help_customer = LlmAgent(
    model=LiteLlm("anthropic/claude-3-5-sonnet-20240620"),
    name="help_customer",
    description="""Faz busca de produtos, planos de pagamentos e outras informações adicionais para ajudar o cliente durante sua busca.""",
    instruction=prompt.HELP_CUSTOMER_INSTR,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uv",
                    args=[
                        "--directory",
                        "/Users/galleani/projetos/multi_agent_lab/search_mcp_server",
                        "run",
                        "help_customer.py",
                    ],
                ),
                timeout=30,
            )
        )
    ],
)

attendant_agent = LlmAgent(
    model=LiteLlm("anthropic/claude-3-5-sonnet-20240620"),
    name="attendant_agent",
    description="""Agente especializado em ajuda com o usuário, mostrando os produtos disponíveis e planos de pagamento.""",
    instruction=prompt.ATTENDANT_INSTR,
    tools=[
        AgentTool(agent=help_customer),
    ],
    generate_content_config=GenerateContentConfig(temperature=0.0, top_p=0.5),
)
