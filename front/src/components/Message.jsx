import { useEffect, useState } from 'react'
import CommonBtn from '@/components/CommonBtn'
import useGeoLocation from '@/hooks/useGeoLocation'
import styles from '@/assets/style/components/message.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

const Message = (props) => {
  // const { currentLocation } = useGeoLocation()
  const saveSessionMapData = () => {
    const savedMapData = sessionStorage.getItem('mapData')
    savedMapData && sessionStorage.removeItem('mapData')
    const mapData = { items: props.cont, nearestIndex: props.nearestIndex, currentLocation: props.currentLocation }
    sessionStorage.setItem('mapData', JSON.stringify(mapData))
  }

  return (
    <div className={props.fromWho == 'bot' ? `${styles.message} ${styles.replies} ${props.className}` : `${styles.message} ${styles.sent} ${props.className}`}>
      {/* <img className={styles.profile_img} src="http://emilcarlsson.se/assets/mikeross.png" alt="" /> */}
      {props.fromWho == 'bot' ? <FontAwesomeIcon icon="fa-solid fa-robot" className={styles.profile_img} /> : <FontAwesomeIcon icon="fa-solid fa-user" className={styles.profile_img} />}
      {props.type == 'text' && (
        <div className={styles.box_wrap}>
          {typeof props.cont === 'string' ? (
            <div className={styles.box}>
              <span>{props.cont}</span>
            </div>
          ) : (
            props.cont.map((item, index) => (
              <div className={styles.box} key={`cont-${index}`}>
                <span>{item}</span>
              </div>
            ))
          )}
        </div>
      )}
      {props.type == 'list' && (
        <div className={styles.box_wrap}>
          {props.cont.map((item, index) => {
            if (index < 5)
              return (
                <div className={styles.list} key={`res-list-${index}`}>
                  <div className={styles.box}>
                    {/* <div className={styles.food_info}> */}
                    <div className={styles.food_title} dangerouslySetInnerHTML={{ __html: item.title }} />
                    <div className={styles.food_address}>{item.address}</div>
                    {/* </div> */}
                    {/* <div className={styles.food_link}>{item.link}</div> */}
                  </div>
                  <div className={styles.btn}>{item.link && <CommonBtn type="a" text={<FontAwesomeIcon icon="fa-solid fa-link" />} linkTo={item.link} />}</div>
                </div>
              )
          })}
          <CommonBtn type="link" text="전체 보기" linkTo="/map" onClick={saveSessionMapData} />
        </div>
      )}
    </div>
  )
}

export default Message
