from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.agents import tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_core.messages import messages_to_dict
from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver, InMemorySaver

from typing import Annotated, Dict, Optional
from typing_extensions import TypedDict

from RAG import RAG

# 환경 변수 로드
load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]
    health: Optional[str] = None
    menus: Optional[str] = None
    web: Optional[str] = None
    reply: Optional[str] = None
    last_tool: Optional[str] = None

memory = InMemorySaver()

graph_builder = StateGraph(State)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# RAG 인스턴스 준비
health_rag = RAG(RAG.HEALTH)
health_rag.load_vector_index()
ingredients_rag = RAG(RAG.INGREDIENTS)
ingredients_rag.load_vector_index()

# tool/tools 정의
@tool
def health_rag_tool(query: str) -> str:
    """의료 분야의 각 질환의 증상과 식이/생활 등의 정보를 제공합니다. 
    사용자가 자신의 건강 상태에 대해 언급한 경우 해당 도구를 사용하세요.
    사용자의 건강 상태에 따라 먹어도 되는 음식의 타입, 재료 등을 확인한 후 ingredient_rag_tool을 사용해 음식을 추천하세요."""
    
    prompt = health_rag.search_and_wrap(query)
    response = llm.invoke(prompt)
    result = response.content.strip() if hasattr(response, "content") else str(response)

    return result

@tool
def ingredient_rag_tool(query: str) -> str:
    """음식 메뉴에 따라 어떤 재료가 들어가는지 정보를 제공합니다.
    사용자에게 구체적인 음식 메뉴를 추천할 때 해당 도구를 사용하세요."""

    base_prompt = f"""
    다음 문장을 읽고 문장에 존재하는 재료로 이루어진 음식 메뉴 Top 5를 추천해줘.
    일반 음식점에서 팔지 않는 재료와 온수, 물은 제외하고, 차는 찻집으로 바꿔줘.
    고유대명사는 제외하고 일반적인 메뉴로만 답변 형식에 맞게 대답해줘.
    문장: "{query}"
    답변 형식: '메뉴1,메뉴2,메뉴3,메뉴4,메뉴5'
    """

    prompt = ingredients_rag.search_and_wrap(base_prompt)
    response = llm.invoke(prompt)
    result = response.content.strip() if hasattr(response, "content") else str(response)

    return result

@tool
def web_search_tool(query: str) -> str:
    """식당 후기와 같은 최신의 정보를 검색할 때 사용하세요."""
    result = TavilySearchResults(max_results=2)

    return result

tools = [health_rag_tool, ingredient_rag_tool, web_search_tool]

# agent node 정의
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    # agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    return_intermediate_steps=True
)

def agent_node(state: State) -> State:
    user_input = state["messages"][-1].content
    result = agent_executor.invoke({"input": user_input})
    
    # 툴 이름과 결과 추출
    tool_calls = result.get("intermediate_steps", [])
    tool_output_map = {"health_rag_tool": "health", "ingredient_rag_tool": "menus", "web_search_tool": "web"}

    new_state = {**state, "reply": result["output"]}

    for action, tool_output in tool_calls:
        tool_name = action.tool
        state_key = tool_output_map.get(tool_name)
        if state_key:
            new_state[state_key] = tool_output
            new_state["last_tool"] = tool_name

    return new_state

def ingredient_tool_node(state: State) -> State:
    user_input = state["messages"][-1].content
    result = ingredient_rag_tool.invoke(user_input)
    return {**state, "menus": result, "last_tool": "ingredient_rag_tool"}

# node/edge 추가
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("ingredient", ingredient_tool_node)

graph_builder.set_entry_point("agent")

def route_tool_condition(state: State) -> str:
    return str(state.get("last_tool") == "health_rag_tool")

graph_builder.add_conditional_edges(
    "agent",
    route_tool_condition,
    {
        "True": "ingredient",
        "False": END,
    }
)

# graph = graph_builder.compile()
graph = graph_builder.compile(checkpointer=memory)

def chat(user_message, message_list=[]):
    thread_id = "foodie-guide"
    config = {"configurable": {"thread_id": thread_id}}
    # checkpoint = memory.load_checkpoint(thread_id)

    print("memory", memory)
    messages = []
    if checkpoint := memory.get(config):
        messages = checkpoint["messages"] + [{"role": "user", "content": user_message}]
    else:
        messages = [
            {"role": "system", "content": "당신은 구체적인 음식 메뉴를 추천하는 AI입니다."},
            {"role": "system", "content": "입력된 문장에서 사용자의 기호를 파악해서 구체적인 음식 메뉴를 추천하거나, 사용자가 건강 상태를 나열할 경우 그 상태에 따라 먹어도 되는 구체적인 음식 메뉴를 제안하는 AI입니다."},
            {"role": "system", "content": "사용자가 원하는 음식을 파악하기 어려운 경우와 사용자가 음식 추천을 원하지 않는 경우 일반적인 대화를 이어갈 수 있는 유연한 AI입니다."},
            {"role": "user", "content": user_message}
        ]


    # messages = []
    # # 이전 메시지가 있으면 이어붙이기
    # if checkpoint and "messages" in checkpoint:
    #     messages = checkpoint["messages"] + [{"role": "user", "content": user_message}]
    # else:
    #     messages = [
    #         {"role": "system", "content": "당신은 구체적인 음식 메뉴를 추천하는 AI입니다."},
    #         {"role": "system", "content": "입력된 문장에서 사용자의 기호를 파악해서 구체적인 음식 메뉴를 추천하거나, 사용자가 건강 상태를 나열할 경우 그 상태에 따라 먹어도 되는 구체적인 음식 메뉴를 제안하는 AI입니다."},
    #         {"role": "system", "content": "사용자가 원하는 음식을 파악하기 어려운 경우와 사용자가 음식 추천을 원하지 않는 경우 일반적인 대화를 이어갈 수 있는 유연한 AI입니다."},
    #         {"role": "user", "content": user_message}
    #     ]

    initial_state = {"messages": messages}
    # initial_state = {"thread_id": "foodie-guide", "messages": messages}

    # final_state = graph.invoke(initial_state)
    final_state = graph.invoke(initial_state, config=config)
    bot_reply = final_state.get("reply")
    messages.append({"role": "assistant", "content": bot_reply})
    
    # memory.save_checkpoint(thread_id, final_state)
    
    print("final_state", final_state)

    menus = final_state.get("menus", '')
    menu_list = [item.strip() for item in menus.split(',')] if menus.strip() else []

    return {
        "reply": final_state.get("reply"),
        "menus": menu_list,
        "link_exist": '',
        "category": ''
    }

# chat("안녕 나 유다솔이라고 해")


# final_state = graph.invoke(initial_state)
# print("final_state", final_state)

# for step in graph.stream(initial_state):
#     print("현재 상태:", step)