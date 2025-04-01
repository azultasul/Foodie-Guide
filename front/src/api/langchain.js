export const langchain = async (features) => {
  try {
    const response = await fetch('/api/langchain', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: features }),
    })

    const data = await response.json()
    console.log('response data', data)

    return data
  } catch (error) {
    console.error('Error fetching recommendations:', error)
    return null
  }
}
