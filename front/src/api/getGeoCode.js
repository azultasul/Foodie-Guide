export const getGeoCode = async (lat, lng) => {
  const url = `/v2/gc?coords=${lng}%2C${lat}&output=json&orders=legalcode%2Cadmcode`

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'plain/text',
        'X-NCP-APIGW-API-KEY-ID': import.meta.env.VITE_X_NCP_APIGW_API_KEY_ID,
        'X-NCP-APIGW-API-KEY': import.meta.env.VITE_X_NCP_APIGW_API_KEY,
      },
    })

    const data = await response.json()
    console.log('response', data)
    return data.results[0].region || []
  } catch (error) {
    console.error('Fetching Error:', error)
    return null
  }
}
