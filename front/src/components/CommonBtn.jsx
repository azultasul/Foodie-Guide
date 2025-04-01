import styles from '@/assets/style/components/btn.module.css'
import { Link } from 'react-router-dom'

const CommonBtn = (props) => {
  return (
    <>
      {props.type == 'button' && (
        <button className={styles.btn} onClick={props.onClick}>
          {props.text}
        </button>
      )}
      {props.type == 'link' && (
        <Link to={props.linkTo} className={styles.btn} onClick={props.onClick}>
          {props.text}
        </Link>
      )}
      {props.type == 'a' && (
        <a href={props.linkTo} className={styles.btn} target="_blank">
          {props.text}
        </a>
      )}
    </>
  )
}

export default CommonBtn
