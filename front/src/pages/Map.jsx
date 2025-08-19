import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import CommonBtn from '@/components/CommonBtn'
import SidePanel from '@/components/SidePanel'
import styles from '@/assets/style/components/map.module.css'

const Map = () => {
  const savedMapData = sessionStorage.getItem('mapData')
  const [mapData, setMapData] = useState(savedMapData ? JSON.parse(savedMapData) : {})
  const [isSidePanelOpen, setIsSidePanelOpen] = useState(false)
  const mapElement = useRef(null)
  const mapRef = useRef(null) // 지도 객체를 저장할 ref
  const markersRef = useRef([]) // 마커들을 저장할 ref
  const [currentMarker, setCurrentMarker] = useState(mapData?.items ? mapData?.items[mapData?.nearestIndex] : -1)
  const navigate = useNavigate()

  const toggleSidePanel = () => {
    setIsSidePanelOpen(!isSidePanelOpen)
  }

  useEffect(() => {
    if (Object.keys(mapData).length === 0) {
      navigate('/', { replace: true }) // ✅ 메인 페이지로 리다이렉트
    }
  }, [navigate])

  useEffect(() => {
    if (Object.keys(mapData).length === 0) return
    if (window.naver) {
      // 지도 초기화 (처음 한 번만 실행)
      if (!mapRef.current) {
        mapRef.current = new window.naver.maps.Map(mapElement.current, {
          center: new window.naver.maps.LatLng(mapData.currentLocation.lat, mapData.currentLocation.lng),
          zoom: 15,
        })
      }

      // 기존 마커 제거
      markersRef.current.forEach((marker) => marker.setMap(null))
      markersRef.current = []

      // 현재 위치 마커 추가
      const userMarker = new window.naver.maps.Marker({
        position: new window.naver.maps.LatLng(mapData.currentLocation.lat, mapData.currentLocation.lng),
        map: mapRef.current,
        icon: {
          content: '<div style="font-size: 30px;">📍</div>',
          anchor: new naver.maps.Point(15, 15),
        },
      })
      markersRef.current.push(userMarker)
      // 음식점 마커 추가
      if (mapData.items) {
        mapData.items.forEach((item, index) => {
          const marker = new window.naver.maps.Marker({
            position: new window.naver.maps.LatLng(item.lat, item.lng),
            map: mapRef.current,
            icon: `https://maps.google.com/mapfiles/ms/icons/${mapData.nearestIndex == index ? 'red' : 'blue'}-dot.png`,
          })
          markersRef.current.push(marker)

          // 마커 클릭 시 현재 데이터 변경
          window.naver.maps.Event.addListener(marker, 'click', () => {
            setCurrentMarker({ ...item })

            markersRef.current.forEach((m, i) => {
              if (i == 0) return
              m.setIcon('https://maps.google.com/mapfiles/ms/icons/blue-dot.png')
            })
            marker.setIcon('https://maps.google.com/mapfiles/ms/icons/red-dot.png')
          })
        })
      }
    }
  }, [])

  return (
    <div id="frame" className="naver">
      <SidePanel
        isOpen={isSidePanelOpen}
        onToggle={toggleSidePanel}
        className={styles.info}
        showHamburger={true}
        hamburgerPosition="map"
      >
        <h2 dangerouslySetInnerHTML={{ __html: `${currentMarker?.title}` }}></h2>
        <hr />
        <h3>🍴 위치</h3>
        <p>{currentMarker?.address}</p>
        <h3>🍴 대표메뉴</h3>
        <p>{currentMarker?.menu}</p>
        {/* <iframe id="iframe" src={`https://map.naver.com/p/search/${mapData.currentAddress} ${mapData.items[mapData.nearestIndex]?.title}`} title="Naver Map"></iframe> */}
        {currentMarker?.link && <CommonBtn type="a" text="자세히 보기" linkTo={currentMarker?.link} />}
      </SidePanel>

      <div ref={mapElement} className="content" />
    </div>
  )
}

export default Map
