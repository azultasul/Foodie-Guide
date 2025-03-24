import { useEffect, useState } from 'react'
import { getGeoCode } from '@/api/getGeoCode'

const useGeoLocation = (options) => {
  const [currentLocation, setCurrentLocation] = useState({ lat: 37.5665, lng: 126.978 })
  const [currentAddress, setCurrentAddress] = useState('')
  // const [currentAddress, setCurrentAddress] = useState('서울특별시 중구 태평로1가')
  const [error, setError] = useState('')

  const handleSuccess = (pos) => {
    const { latitude, longitude } = pos.coords
    setCurrentLocation({ lat: latitude, lng: longitude })
    console.log('??', latitude, longitude)
  }

  const handleError = (err) => {
    setError(err.message)
    console.log('err', err.message)
  }

  const requestLocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser.')
      return
    }

    const defaultOptions = {
      enableHighAccuracy: false,
      timeout: 5000,
      maximumAge: 0,
    }

    // 사용자가 버튼을 눌렀을 때 위치 요청 실행 → 팝업이 자동으로 뜸
    navigator.geolocation.getCurrentPosition(handleSuccess, handleError, options || defaultOptions)
    console.log('??', navigator.geolocation)
  }

  const getcurrentAddress = async () => {
    const geoCode = await getGeoCode(currentLocation.lat, currentLocation.lng)
    const address = `${geoCode.area1.name} ${geoCode.area2.name} ${geoCode.area3.name}`
    setCurrentAddress(address)
  }

  useEffect(() => {
    requestLocation()
  }, [])

  useEffect(() => {
    getcurrentAddress()
    // const latitude = currentLocation?.lat ? currentLocation.lat : 37.5665 //  위도 (서울)
    // const longitude = currentLocation?.lng ? currentLocation.lng : 126.978 // 경도 (서울)
    // setCurrentLocation({ lat: latitude, lng: longitude })
  }, [currentLocation])

  return { currentLocation, currentAddress, error, requestLocation }
}

export default useGeoLocation
