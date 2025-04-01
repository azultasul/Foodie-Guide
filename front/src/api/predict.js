export const predict = async (features) => {
  try {
    const response = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ features }),
    })

    const data = await response.json()
    return data.prediction
  } catch (error) {
    console.error('Error fetching prediction:', error)
    return null
  }
}
