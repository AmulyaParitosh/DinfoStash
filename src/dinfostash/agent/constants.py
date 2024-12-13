from dataclasses import dataclass
from typing import Literal

from pydantic_ai import Agent, RunContext

from dinfostash.data.models import Experience, Project

with open(
    "src/dinfostash/agent/prompts/project_system_prompt.txt", "r", encoding="utf-8"
) as f:
    project_system_prompt = f.read()
    if not project_system_prompt.split():
        raise ValueError("System prompt is empty")

with open(
    "src/dinfostash/agent/prompts/experience_system_prompt.txt", "r", encoding="utf-8"
) as f:
    experience_system_prompt = f.read()
    if not experience_system_prompt.split():
        raise ValueError("System prompt is empty")


@dataclass
class TailorSection:
    section: Literal["Project"] | Literal["Experience"]
    data: list[Project] | list[Experience]


project_agent = Agent(
    "groq:llama-3.1-70b-versatile",
    deps_type=TailorSection,
    result_type=list[Project],
    system_prompt=project_system_prompt,
)
experience_agent = Agent(
    "groq:llama-3.1-70b-versatile",
    deps_type=TailorSection,
    result_type=list[Experience],
    system_prompt=experience_system_prompt,
)


def add_json_data(ctx: RunContext[TailorSection]) -> str:
    return f"json data: [{'\n'.join([str(item) for item in ctx.deps.data])}]"


project_agent.system_prompt(add_json_data)
experience_agent.system_prompt(add_json_data)
