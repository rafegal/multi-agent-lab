from google.adk.agents import Agent, LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig

from vitra_ai.sub_agents.health_mate import prompt


nutra_specialist = Agent(
    model="gemini-2.0-flash",
    name="nutra_specialist",
    description="""Ajuda as pessoas a cuidar da pele, com dicas e recomendações de produtos e tratamentos.""",
    instruction=prompt.NUTRA_ESPECIALIT_INSTR,
)


workout_specialist = LlmAgent(
    model=LiteLlm("ollama_chat/llama3.1:8b"),
    name="workout_specialist",
    description="""Ajuda com dicas de treinos e exercícios para melhora da saúde.""",
    instruction=prompt.WORKOUT_INSTR,
)


health_mate = Agent(
    model="gemini-2.5-flash",
    name="health_mate",
    description="""Ajuda as pessoas a cuidar da saúde e bem-estar.""",
    instruction=prompt.HEALTH_MATE_INSTR,
    tools=[
        AgentTool(agent=nutra_specialist),
        AgentTool(agent=workout_specialist),
    ],
    generate_content_config=GenerateContentConfig(temperature=0.0, top_p=0.5),
)
