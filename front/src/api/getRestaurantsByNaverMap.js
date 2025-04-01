export const getRestaurantsByNaverMap = async (query) => {
  const display = 5
  const start = 1
  const sort = 'random'

  const url = `/v1/search/local.json?query=${query}&display=${display}&start=${start}&sort=${sort}`

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'plain/text',
        'X-Naver-Client-Id': import.meta.env.VITE_X_NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': import.meta.env.VITE_X_NAVER_CLIENT_SECRET,
      },
    })

    const data = await response.json()
    // console.log('response', data.items)
    return data.items || []
  } catch (error) {
    console.error('Fetching Error:', error)
    return null
  }
}
