from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import END
from langchain_core.messages import SystemMessage, AIMessage
from typing import Literal
from langgraph.types import Command
from github_ai_agent.core.tools.repo import get_repo_info, get_repo_file, get_all_projects
from github_ai_agent.core.llm_model import model
from github_ai_agent.core.state import State
import github_ai_agent.core.prompts as prompts
from github_ai_agent.core.schemas import CardDecision
from github_ai_agent.core.Enums import UserInfo


tools = [get_repo_info, get_repo_file, get_all_projects]

tool_node = ToolNode(tools)

def llm_or_card(state:State) -> Command[Literal['llm', '__end__']]:
    system_prompt = prompts.LLM_OR_CARD_SYSTEM_PROMPT
    message = state['messages'][-1]
    full_message = [SystemMessage(content=system_prompt)] + [message]
    response = model.with_structured_output(CardDecision).invoke(full_message).model_dump()
    if response['is_card']:
        return Command(
            update={'card':response['card'],'messages':[AIMessage(content = UserInfo.CardContent.value[response['card']])]},
            goto='__end__'
        )
    return Command(goto='llm')


def llm(state:State):
    full_message = [SystemMessage(content=prompts.AGENT_SYSTEM_PROMPT)] + state['messages']
    response = model.bind_tools(tools).invoke(full_message)
    return {'messages':[response],'card':None}