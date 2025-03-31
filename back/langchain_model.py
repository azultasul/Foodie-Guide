from flask import session
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.schema import HumanMessage, SystemMessage
from langchain.schema.runnable import RunnableLambda, RunnableSequence
from langchain_community.chat_message_histories import ChatMessageHistory

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

from RAG import RAG

load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')
 
# 대화 category 설정 
CHAT_NORMAL = "일반 대화"
CHAT_ASKMORE = "음식점 메뉴 추천 없이 일반 질문"
CHAT_MENURCMD = "음식점 메뉴 추천"
CHAT_MENURCMD_MYCOND = "본인 상태 알림 및 관련 음식점 메뉴 추천"
CHAT_MENURCMD_MYTASTE = "먹고 싶은 음식점 메뉴 설명 및 추천"

CHAT_TYPES = [CHAT_NORMAL, CHAT_ASKMORE, CHAT_MENURCMD, CHAT_MENURCMD_MYCOND, CHAT_MENURCMD_MYTASTE]

memory = ConversationBufferMemory(memory_key="chat_history")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 카테고리 분류 chain
def classify_input(user_input):
    string_types = "".join([f"- {item}\n" for item in CHAT_TYPES])
    return {"string_types": string_types, "user_input": user_input}
    
def classify_prompt(data):
    prompt = f"""
    다음 문장이 어떤 유형인지 분류해줘. 가능한 카테고리는 다음과 같아:
    {data['string_types']}
    
    문장: "{data['user_input']}"
    
    답변 형식은 반드시 다음과 같이 해줘:
    
    분류: [카테고리명]
    """
    message = [
      SystemMessage(content="너는 입력된 문장을 카테고리로 분류하는 AI야."),
      HumanMessage(content=prompt)   
    ]
    return message

def classify_output(response):
    result_text = response.content
    category = result_text.split("분류: ")[-1].strip()
    return category

classify_chain = RunnableSequence(
    RunnableLambda(classify_input)
    | RunnableLambda(classify_prompt) 
    | llm 
    | RunnableLambda(classify_output)
)

# 메뉴 추천 chain
def get_menu_message(text):
    prompt = f"""
    다음 문장을 읽고 문장에 존재하는 재료로 이루어진 음식 메뉴 Top 5를 추천해줘. 
    일반 음식점에서 팔지 않는 재료는 메뉴에서 제외해줘.
    차는 찻집으로 바꿔줘.
    
    =======================================================
    문장: "{text}"
    =======================================================
    답변 형식은 반드시 중복없이 다음과 같이 해줘:
    
    메뉴1,메뉴2,메뉴3,메뉴4,메뉴5
    
    """

    rag = RAG(RAG.INGREDIENTS)
    rag.load_vector_index()
    message = [
      SystemMessage(content="너는 사용자의 상태를 입력된 문장에서 판단하여 먹기 좋은 메뉴를 제안하는 AI야."),
      SystemMessage(content="너는 입력된 문장에서 사용자가 메뉴 추천을 원하지 않고 상태만 나열할 경우 적절한 의학적 답변을 주거나 먹기 좋은 메뉴를 제안하는 AI야."),
      HumanMessage(content=rag.search_and_wrap(prompt))   
    ]
    return message

def get_menu_output(response):
    return response.content.split(",")

# 메뉴 추천 chain : 메시지 기록
get_menu_chain = RunnableSequence(
    RunnableLambda(get_menu_message)
    | llm 
    | RunnableLambda(get_menu_output)
)

def chat(user_message, message_list):
    rag = RAG(RAG.HEALTH)
    rag.load_vector_index()

    print("message_list", message_list)
    # if message_list is []:
    messages = []
    messages.append(SystemMessage(content="너는 음식 메뉴를 추천하는 AI야."))
    

    # 대화의 분류 및 봇 응답을 처리
    category = classify_chain.invoke({"user_input": user_message})

    conversation = ConversationChain(llm=llm, memory=memory)

    if category == CHAT_MENURCMD_MYCOND:
        messages.append(HumanMessage(content=rag.search_and_wrap(user_message)))
    else:
        messages.append(HumanMessage(content=user_message))
        
    
    for message in messages:
        conversation.memory.chat_history.add_message(message)

    try:
        bot_reply = conversation.predict(input=user_message)
    except Exception as e:
        bot_reply = f"오류 발생: {str(e)}"
    
    link_exist = False
    menus = []
    
    # 메뉴 추천이 필요한 경우
    if category in [CHAT_MENURCMD, CHAT_MENURCMD_MYTASTE, CHAT_MENURCMD_MYCOND]:
        menus = get_menu_chain.invoke({"user_input": bot_reply})
        link_exist = True
    
    if len(menus) > 0:
        add_str = "[{}]".format(",".join(menus))
    
    return {"reply": bot_reply, "menus": ",".join(menus), "link_exist": link_exist, "category": category}