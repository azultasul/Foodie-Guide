export const getAiagent = async (userMessage) => {
  const sessionData = JSON.parse(sessionStorage.getItem('messageList')).filter((item) => item.type == 'text')
  // console.log('sessionData', sessionData)

  try {
    const response = await fetch('/api/aiagent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userMessage, messageList: sessionData }),
    })

    const data = await response.json()
    console.log('chat response data', data)

    return data
  } catch (error) {
    console.error('Error fetching chat:', error)
    return null
  }
}
