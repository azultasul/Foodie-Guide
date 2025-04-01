import { useEffect, useRef, useState } from 'react'
import useGeoLocation from '@/hooks/useGeoLocation'
import styles from '@/assets/style/components/map.module.css'

// props.data.items
// restaurants: 네이버 지도 검색 api의 결과의 items 배열

const NaverMap = (props) => {
  const { currentLocation, error, requestLocation } = useGeoLocation()
  const mapElement = useRef(null)
  const mapRef = useRef(null) // 지도 객체를 저장할 ref
  const markersRef = useRef([]) // 마커들을 저장할 ref
  const infoWindowRef = useRef(null) // InfoWindow 객체를 저장할 ref
  const [currentMarker, setCurrentMarker] = useState(props.data.items[props.data.nearestIndex])

  useEffect(() => {
    if (window.naver && currentLocation) {
      // 지도 초기화 (처음 한 번만 실행)
      if (!mapRef.current) {
        mapRef.current = new window.naver.maps.Map(mapElement.current, {
          center: new window.naver.maps.LatLng(currentLocation.lat, currentLocation.lng),
          zoom: 15,
        })
      }

      // 기존 마커 제거
      markersRef.current.forEach((marker) => marker.setMap(null))
      markersRef.current = []

      // 현재 위치 마커 추가
      const userMarker = new window.naver.maps.Marker({
        position: new window.naver.maps.LatLng(currentLocation.lat, currentLocation.lng),
        map: mapRef.current,
        icon: {
          content: '<div style="font-size: 30px;">📍</div>',
          anchor: new naver.maps.Point(15, 15),
        },
      })
      markersRef.current.push(userMarker)

      // 음식점 마커 추가
      if (props.data.items) {
        props.data.items.forEach((loc) => {
          const { title, lng, lat } = loc
          const marker = new window.naver.maps.Marker({
            position: new window.naver.maps.LatLng(lat, lng),
            map: mapRef.current,
          })
          markersRef.current.push(marker)

          // 마커 클릭 시 현재 데이터 변경
          window.naver.maps.Event.addListener(marker, 'click', () => {
            // console.log('marker', marker)
            setCurrentMarker({ ...loc })
          })
        })
      }
    }
  }, [currentLocation, props.data.items])

  return (
    <div className={styles.map}>
      <div className={styles.info}>
        <h2>title: {currentMarker?.title}</h2>
        <p>lng: {currentMarker?.lng}</p>
        <p>lat: {currentMarker?.lat}</p>
      </div>
      <div ref={mapElement} className={styles.navermap} />
      {/* <iframe id="iframe" src={`https://map.naver.com/p/search/${props.data.currentAddress} ${props.data.items[props.data.nearestIndex]?.title}`} title="Naver Map"></iframe> */}
    </div>
  )
}

export default NaverMap
