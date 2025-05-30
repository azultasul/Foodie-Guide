from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_react_agent, tool
from dotenv import load_dotenv

from RAG import RAG  # 사용자가 정의한 RAG 클래스

class ReActAgent:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0):
        # Load environment variables
        load_dotenv()

        # Initialize LLM
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)

        # Initialize RAG instances
        self.health_rag = RAG(RAG.HEALTH)
        self.health_rag.load_vector_index()

        self.ingredients_rag = RAG(RAG.INGREDIENTS)
        self.ingredients_rag.load_vector_index()

        # Initialize tools
        self.tools = [
            self._define_health_tool(),
            self._define_ingredient_tool(),
            self._define_tavily_search_tool()
        ]

        self.reply = {
            "health": None,
            "menus": None,
            "web": None,
            "output": None
        }

        # Create prompt and agent
        self.prompt = self._create_prompt()
        self.agent = create_react_agent(self.llm, tools=self.tools, prompt=self.prompt)

        # Create AgentExecutor
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def _define_health_tool(self):
        @tool
        def health_rag_tool(query: str) -> str:
            """의료 분야의 각 질환의 증상과 식이/생활 등의 정보를 제공합니다. 
            사용자가 자신의 건강 상태에 대해 언급한 경우 해당 도구를 사용하세요.
            사용자의 건강 상태에 따라 먹어도 되는 음식의 타입, 재료 등을 확인한 후 ingredient_rag_tool을 사용해 음식을 추천하세요."""

            prompt = self.health_rag.search_and_wrap(query)
            response = self.llm.invoke(prompt)
            content = response.content.strip() if hasattr(response, "content") else str(response)
            print("content", content)

            self.reply["health"] = content
            print("???? health", self.reply)
            return content

        return health_rag_tool

    def _define_ingredient_tool(self):
        @tool
        def ingredient_rag_tool(query: str) -> str:
            """음식 메뉴에 따라 어떤 재료가 들어가는지 정보를 제공합니다.
            사용자에게 구체적인 음식 메뉴를 추천할 때 해당 도구를 사용하세요."""

            base_prompt = f"""
            다음 문장을 읽고 문장에 존재하는 재료로 이루어진 음식 메뉴 Top 5를 추천해줘.
            일반 음식점에서 팔지 않는 재료와 온수, 물은 제외하고, 차는 찻집으로 바꿔줘.
            고유대명사는 제외하고 일반적인 메뉴로만 대답해줘.
            문장: "{query}"
            답변 형식: 메뉴1,메뉴2,메뉴3,메뉴4,메뉴5
            """

            prompt = self.ingredients_rag.search_and_wrap(base_prompt)
            response = self.llm.invoke(prompt)
            content = response.content.strip() if hasattr(response, "content") else str(response)

            self.reply["menus"] = content.replace('답변: \n', '').split(',')
            print("???? menus", self.reply)
            return content
        
        # self.reply["menus"] = ingredient_rag_tool()
        return ingredient_rag_tool

    def _define_tavily_search_tool(self):
        search_result = TavilySearchResults(max_results=2)
        print("???? search_result", search_result)

        # self.reply["web"] = search_result
        return search_result

    def _create_prompt(self) -> PromptTemplate:
        template = """
        당신은 구체적인 음식 메뉴를 추천하는 AI입니다. 
        입력된 문장에서 사용자의 기호를 파악해서 구체적인 음식 메뉴를 추천하거나,
        사용자가 건강 상태를 나열할 경우 그 상태에 따라 먹어도 되는 구체적인 음식 메뉴를 제안하는 AI입니다. 
        사용자가 원하는 음식을 파악하기 어려운 경우와 사용자가 음식 추천을 원하지 않는 경우 일반적인 대화를 이어갈 수 있는 유연한 AI입니다. 

        사용자의 질문에 단계적으로 사고하고 다음 질문에 최선을 다해 답변하세요. 당신은 다음 도구들에 접근할 수 있습니다:
        {tools}

        다음 형식을 사용하세요:

        Question: 답변해야 하는 입력 질문
        Thought: 무엇을 할지 항상 생각하세요
        Action: 취해야 할 행동, [{tool_names}] 중 하나여야 합니다. 리스트에 있는 도구 중 1개를 택하십시오.
        Action Input: 행동에 대한 입력값
        Observation: 행동의 결과
        ... (이 Thought/Action/Action Input/Observation의 과정이 N번 반복될 수 있습니다)
        Thought: 이제 최종 답변을 알겠습니다
        Final Answer: 원래 입력된 질문에 대한 최종 답변

        ## 추가적인 주의사항
        - 반드시 [Thought -> Action -> Action Input format] 이 사이클의 순서를 준수하십시오. 항상 Action 전에는 Thought가 먼저 나와야 합니다.
        - 최종 답변에는 최대한 많은 내용을 포함하십시오.
        - 한 번의 검색으로 해결되지 않을 것 같다면 문제를 분할하여 푸는 것은 중요합니다.
        - 정보가 취합되었다면 불필요하게 사이클을 반복하지 마십시오.
        - 묻지 않은 정보를 찾으려고 도구를 사용하지 마십시오.

        시작하세요!

        Question: {input}
        Thought: {agent_scratchpad}"""

        return PromptTemplate.from_template(template)

    def run(self, user_input: str):
        output = self.executor.invoke({"input": user_input})
        self.reply["output"] = output["output"]
        return self.reply

