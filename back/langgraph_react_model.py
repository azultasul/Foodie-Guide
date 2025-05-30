from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_react_agent, tool

from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage, HumanMessage, AnyMessage

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from typing import Annotated, Dict, Optional
from typing_extensions import TypedDict

from dotenv import load_dotenv

from RAG import RAG
from ReActAgent import ReActAgent

# 환경변수 로드 및 LLM 정의
load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 📦 LangGraph 상태 정의
class GraphState(TypedDict):
    input: Annotated[list, add_messages]
    health: Optional[str] = None
    menus: Optional[str] = None
    web: Optional[str] = None
    reply: Optional[str] = None

# 🔧 ReAct Agent Node
def react_agent_node(state: GraphState) -> Dict:
    print("state", state)
    react_agent = ReActAgent()
    result = react_agent.run(state["input"])
    print("result", result)
    # result = react_agent_executor.invoke({"input": state["input"]})
    
    health = None
    menus = None
    web = None

    # result는 dict, 'output' 필드에 최종 답변 있음
    if "health" in str(result):
        health = result["health"]
    if "menus" in str(result):
        menus = result["menus"]
    if "web" in str(result):
        web = result["web"]

    return {
        "health": health,
        "menus": menus,
        "web": web,
        "reply": result["output"] if isinstance(result, dict) and "output" in result else str(result),
    }

# 💬 LLM Chat Node (결과를 재정리하거나 요약 가능)
def chat_node(state: GraphState) -> Dict:
    print("chat_node - state", state)
    messages = [
        HumanMessage(content=f"""
        아래는 도구를 통해 수집된 정보야. 이걸 바탕으로 사용자에게 이해하기 쉬운 자연스러운 형태로 대답해줘.

        건강 정보: {state["health"]}
        추천 메뉴: {state["menus"]}
        웹 검색 결과: {state["web"]}
        """)
    ]
    response = llm.invoke({"input": messages})
    return {"reply": response.content.strip()}

# 🌐 LangGraph 구성
graph_builder = StateGraph(GraphState)

graph_builder.add_node("react_agent_node", react_agent_node)
graph_builder.add_node("chat_node", chat_node)

# 엣지 정의
graph_builder.set_entry_point("react_agent_node")
graph_builder.add_edge("react_agent_node", "chat_node")
graph_builder.add_edge("chat_node", END)

# Graph 완성
graph = graph_builder.compile()
print("graph", graph)
# display(Image(graph.get_graph().draw_mermaid_png()))

def chat(user_message):
    final_state = graph.invoke({"input": [HumanMessage(content=user_message)]})
    # final_state = graph.invoke({"input": user_message})

    # final_state = graph.invoke(user_message)
    # final_state = graph.invoke([HumanMessage(user_message)])
    print("final_state", final_state)


# chat("나 알레르기 때문인지 피부가 가려워")