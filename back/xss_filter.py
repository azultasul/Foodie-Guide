import re
import html

def contains_xss(value: str) -> bool:
    """입력값에 잠재적 XSS 공격 코드가 포함되어 있는지 검사."""
    xss_pattern = re.compile(r'(<script|<\/script|<img|<iframe|<object|on\w+\s*=)', re.IGNORECASE)
    return bool(xss_pattern.search(value))

def sanitize_input(value: str) -> str:
    """입력값에서 HTML 특수문자를 이스케이프 처리."""
    return html.escape(value)