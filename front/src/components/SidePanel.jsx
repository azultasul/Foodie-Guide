import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

const SidePanel = ({
    isOpen,
    onToggle,
    children,
    className = '',
    showHamburger = false,
    hamburgerPosition = 'default'
}) => {
    return (
        <>
            {/* 사이드패널 */}
            <div id="sidepanel" className={`${className} ${isOpen ? 'mobile-open' : ''}`}>
                {children}
            </div>

            {/* 모바일 오버레이 */}
            {isOpen && (
                <div className="mobile-overlay" onClick={onToggle}>
                    <button className="overlay-close-btn" onClick={onToggle}>
                        <FontAwesomeIcon icon="fa-solid fa-times" />
                    </button>
                </div>
            )}

            {/* 햄버거 버튼 (필요한 경우에만 표시) */}
            {showHamburger && (
                <button
                    className={`hamburger-btn ${hamburgerPosition === 'map' ? 'hamburger-btn-map' : ''}`}
                    onClick={onToggle}
                >
                    <FontAwesomeIcon icon={isOpen ? "fa-solid fa-times" : "fa-solid fa-bars"} />
                </button>
            )}
        </>
    )
}

export default SidePanel
