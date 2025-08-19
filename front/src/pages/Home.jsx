import { useEffect, useState, useRef } from 'react'
import { getAiagent } from '@/api/getAiagent'
import Message from '@/components/Message'
import CommonBtn from '@/components/CommonBtn'
import SidePanel from '@/components/SidePanel'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import sideBtnData from '@/data/sideButton'
import useGeoLocation from '@/hooks/useGeoLocation'
import useGetRestaurants from '@/hooks/useGetRestaurants'

const Home = () => {
  const savedMessage = sessionStorage.getItem('messageList')
  const [messageList, setMessageList] = useState(savedMessage ? JSON.parse(savedMessage) : [])
  const [buttonData, setButtonData] = useState(sideBtnData)
  const [userInput, setUserInput] = useState('')
  const [timeState, setTimeState] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [isSidePanelOpen, setIsSidePanelOpen] = useState(false)
  const { currentLocation, currentAddress, error: geoError, requestLocation } = useGeoLocation()

  const [menus, setMenus] = useState([])
  const [otherLocation, setOtherLocation] = useState('')

  const { restaurants, nearestIndex, loading, error: resError, getRestaurants } = useGetRestaurants(menus, currentLocation, currentAddress, otherLocation)
  const messageEndRef = useRef(null)
  const chatCategory = [
    // '일반 대화',
    // '음식점 메뉴 추천 없이 일반 질문',
    '음식점 메뉴 추천',
    '본인 상태 알림 및 관련 음식점 메뉴 추천',
    '먹고 싶은 음식점 메뉴 설명 및 추천',
  ]

  const addUserMessage = (input) => {
    const newMessage = {
      fromWho: 'user',
      type: 'text',
      cont: input,
    }
    setMessageList((prev) => [...prev, newMessage])
    setUserInput('')
  }
  const addBotMessage = async (query) => {
    const result = await getAiagent(query)
    const hasCat = chatCategory.includes(result.category)

    setIsLoading(false)
    if (!hasCat) {
      const newMessage = {
        fromWho: 'bot',
        type: 'text',
        cont: result.reply,
      }
      setMessageList((prev) => [...prev, newMessage])
    } else {
      // 식당 추천해주는 경우 -> list 불러오기
      const menus = result.menus.split(',')

      const newMessage = {
        fromWho: 'bot',
        type: 'text',
        cont: [result.reply, `추천 메뉴: ${menus}`],
      }
      setMessageList((prev) => [...prev, newMessage])
      setMenus(menus)
    }
  }

  const submitMessage = async (event, user_message) => {
    event.preventDefault()
    // 모바일에서 메시지 전송 후 사이드패널 닫기
    if (window.innerWidth <= 780) {
      setIsSidePanelOpen(false)
    }
    addUserMessage(user_message)
    setIsLoading(true)
    await addBotMessage(user_message)
  }

  const toggleSidePanel = () => {
    setIsSidePanelOpen(!isSidePanelOpen)
  }

  useEffect(() => {
    menus.length > 0 && getRestaurants()
  }, [menus])

  useEffect(() => {
    // 식당 list 추가
    if (restaurants.length == 0 && nearestIndex == -1) return

    const newMessage = {
      fromWho: 'bot',
      type: 'list',
      cont: restaurants,
      nearestIndex: nearestIndex,
      currentLocation: currentLocation,
    }

    setMessageList((prev) => [...prev, newMessage])
  }, [nearestIndex])

  useEffect(() => {
    sessionStorage.setItem('messageList', JSON.stringify(messageList))
    messageList.length > 0 && messageEndRef.current.scrollIntoView({ behavior: 'smooth' })
    messageList.length > 0 && setTimeState(-1)
  }, [messageList])

  return (
    <div id="frame">
      <SidePanel
        isOpen={isSidePanelOpen}
        onToggle={toggleSidePanel}
        showHamburger={false}
      >
        {Object.keys(buttonData).map((data) => {
          return (
            <div className="category" key={data}>
              <h2>{data}</h2>
              <div className="btn-wrap">
                {buttonData[data].map((item, index) => {
                  return <CommonBtn type={item.type} text={item.text} linkTo={item.linkTo ? item.linkTo : ''} onClick={(event) => submitMessage(event, item.message)} key={`${data}-${index}`} />
                })}
              </div>
            </div>
          )
        })}
      </SidePanel>

      <div className="content">
        <div className="title">
          <div>
            Foodie Guide <span>with ChatGPT</span>
          </div>
          <div className="title-right">
            <CommonBtn
              type="button"
              text="현재 위치 공유"
              onClick={(e) => {
                e.preventDefault()
                requestLocation()
                geoError && alert(geoError)
              }}
            />
            <button className="hamburger-btn" onClick={toggleSidePanel}>
              <FontAwesomeIcon icon={isSidePanelOpen ? "fa-solid fa-times" : "fa-solid fa-bars"} />
            </button>
          </div>
          <div className={timeState === 0 ? 'info show' : 'info'}>
            <p>위치 권한을 활성화한 후</p>
            <p>현재 위치를 공유해 주시면</p>
            <p>당신의 근처 식당을 추천해 드릴게요!</p>
          </div>
        </div>
        <div className="intro">
          <div className={messageList.length > 0 ? 'text-wrap' : 'text-wrap show'}>
            <p>맛있는 메뉴와 식당을 추천해 드릴게요!</p>
            <p>당신의 상태를 설명해주세요.</p>
            <p>🍚 🌮 🥘 🍔 🍣 🍜</p>
          </div>
        </div>
        <div className="messages">
          {messageList.length > 0 && (
            <>
              <div>
                {messageList.map((item, index) => {
                  return (
                    <Message
                      fromWho={item.fromWho}
                      type={item.type}
                      cont={item.cont}
                      linkToData={item.linkToData || {}}
                      nearestIndex={item.nearestIndex}
                      currentLocation={item.currentLocation}
                      key={index}
                    />
                  )
                })}
                <Message className={isLoading ? 'loading show' : 'loading'} fromWho="bot" type="text" cont="답변을 작성 중 입니다..." />
              </div>
              <div ref={messageEndRef}></div>
            </>
          )}
        </div>
        <div className="message-input">
          <div className="wrap">
            <form onSubmit={(event) => submitMessage(event, userInput)}>
              <input
                id="message-input"
                type="text"
                placeholder="Write your message..."
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                aria-label="메시지 입력"
                autoComplete="off"
              />
              <button
                type="submit"
                className="submit"
                aria-label="메시지 전송"
              >
                <FontAwesomeIcon icon="fa-solid fa-paper-plane" className="fa fa-paperclip attachment" />
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
