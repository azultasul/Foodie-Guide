import { useState, useEffect } from 'react'
import { getRestaurantsByNaverMap } from '@/api/getRestaurantsByNaverMap'

const useGetRestaurants = (menus, currentLocation, currentAddress, otherLocation) => {
  const [restaurants, setRestaurants] = useState([])
  const [nearestIndex, setNearestIndex] = useState(-1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const getRestaurants = async () => {
    if (menus.length == 0 || !currentLocation) return // 필수 값이 없으면 실행하지 않음

    setLoading(true)
    setError(null)
    try {
      const results = []

      for (const menu of menus) {
        let query = otherLocation ? `${otherLocation} ${menu}` : `${currentAddress} ${menu}`

        const resultByNaverMap = await getRestaurantsByNaverMap(query)

        const mappedResults = resultByNaverMap.map((item) => ({
          title: item.title,
          address: item.address,
          link: item.link,
          lat: Number(item.mapy) / 10 ** 7,
          lng: Number(item.mapx) / 10 ** 7,
          menu: menu,
        }))

        results.push(...mappedResults)
      }

      const uniqueResults = Array.from(new Map(results.map((item) => [item.title, item])).values())

      setRestaurants([...uniqueResults])
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
  }
  const calculateNearestStoreIndex = () => {
    let minDistance = 10 ** 9
    let latitude = currentLocation.lat
    let longitude = currentLocation.lng

    restaurants.forEach((item, i) => {
      let distance = (item.lat - latitude) ** 2 + (item.lng - longitude) ** 2
      if (distance < minDistance) {
        minDistance = distance
        setNearestIndex(i)
      }
    })
  }

  useEffect(() => {
    if (!restaurants) return
    calculateNearestStoreIndex()
  }, [restaurants])

  return { restaurants, nearestIndex, loading, error, getRestaurants }
}

export default useGetRestaurants
