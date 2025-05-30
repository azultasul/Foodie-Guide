def validate_input(data):
    """
    message_list의 유효성을 검사하고 안전한 role만 반환되도록 정제합니다.
    잘못된 항목이 있으면 에러 메시지를 반환하고, 없으면 None을 반환합니다.
    """
    if not data:
        return "Input cannot be empty"

    user_message = data.get("message")
    message_list = data.get("messageList")

    if not user_message or not isinstance(user_message, str):
        return "Message must be a non-empty string"
    
    if not isinstance(message_list, list):
        return "Message list must be a list"
    
    #DoS attack 방지: 메시지 길이 제한
    if len(user_message) > 1000:
        return "Message is too long, maximum length is 1000 characters"
    
    if len(message_list) > 50:
        return "Message list is too long, maximum length is 50 items"
    
    for  i, msg in enumerate(message_list):
        if not isinstance(msg,dict) or 'role' not in msg or 'content' not in msg:
            return f"Message list item {i} must be a dictionary with 'role' and 'content' keys"

        if msg['role'] not in ['user', 'assistant']:
            return f"Invalid role '{msg['role']}' in message list item {i}, must be 'user' or 'assistant'"
        if not isinstance(msg['content'], str):
            return f"{i+1}th message content must be a string"
    return None  # 모든 검증 통과