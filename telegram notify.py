import requests
import json
from typing import Optional, Dict, Any
from datetime import datetime


TELEGRAM_BOT_TOKEN = "8417493285:AAFQ6b8oR0qQlMI2vhxzGDLAATysrZAfC4Y"
TELEGRAM_CHAT_ID = "8106146605"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"




def send_telegram_notification(
    message: str,
    title: str = "Assistive Buttons Alert",
    include_timestamp: bool = True,
    buttons_info: Optional[Dict[str, Any]] = None
) -> bool:
        try:
       
        formatted_message = f"<b>{title}</b>\n\n"
        formatted_message += f"{message}\n"
       
        if buttons_info:
            formatted_message += "\n<b>Details:</b>\n"
            if buttons_info.get("button"):
                formatted_message += f"Button: {buttons_info['button']}\n"
            if buttons_info.get("text"):
                formatted_message += f"Action: {buttons_info['text']}\n"
            if buttons_info.get("language"):
                formatted_message += f"Language: {buttons_info['language']}\n"
            if buttons_info.get("user_id") and buttons_info["user_id"] != "default":
                formatted_message += f"User: {buttons_info['user_id']}\n"
            if buttons_info.get("device_id") and buttons_info["device_id"] != "unknown":
                formatted_message += f"Device: {buttons_info['device_id']}\n"
            if buttons_info.get("device_name"):
                formatted_message += f"Device Name: {buttons_info['device_name']}\n"
            if buttons_info.get("source"):
                formatted_message += f"Source: {buttons_info['source']}\n"
       
        if include_timestamp:
            formatted_message += f"\n<i>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
       
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": formatted_message,
            "parse_mode": "HTML"
        }
       
        response = requests.post(TELEGRAM_API_URL, json=payload, timeout=5)
       
        if response.status_code == 200:
            return True
        else:
            print(f"Telegram notification failed: {response.status_code}")
            return False
           
    except Exception as e:
        print(f"Error sending Telegram notification: {str(e)}")
        return False




def notify_button_press(
    button: str,
    text: str,
    language: str,
    user_id: str = "unknown",
    device_id: str = "unknown",
    device_name: str = None,
    source: str = "DEVICE"
) -> bool:
    
    message = f"🔔 Button pressed on your Assistive Device\n\n"
   
    button_labels = {
        "BTN1": "🆘 Help",
        "BTN2": "💊 Medicine",
        "BTN3": "💧 Water",
        "BTN4": "🛏️ Rest",
        "BTN5": "📞 Call Someone",
        "BTN6": "🚨 Emergency"
    }
   
    button_label = button_labels.get(button, button)
    message += f"Action: {button_label}\n"
    message += f"Message: {text}\n"
   
    buttons_info = {
        "button": button_label,
        "text": text,
        "language": language,
        "user_id": user_id,
        "device_id": device_id,
        "device_name": device_name,
        "source": source
    }
   
    return send_telegram_notification(
        message=message,
        title="📱 Button Press Alert",
        buttons_info=buttons_info
    )




def notify_security_reset(email: str) -> bool:
    message = f"🔐 Password reset initiated for account: {email}"
    return send_telegram_notification(
        message=message,
        title="🔒 Security Alert",
        include_timestamp=True
    )




def notify_account_signup(email: str, account_type: str) -> bool:
    account_label = "👴 Primary (Disabled/Elderly)" if account_type == "primary" else "👨‍⚕️ Caretaker"
    message = f"✅ New account created\n\nEmail: {email}\nType: {account_label}"
    return send_telegram_notification(
        message=message,
        title="👤 New User Registration",
        include_timestamp=True
    )




def notify_help_request(user_id: str, help_text: str, device_id: str = None) -> bool:
    message = f"🚨 <b>HELP REQUEST</b>\n\n"
    message += f"Message: {help_text}\n"
    message += f"User: {user_id}\n"
    if device_id:
        message += f"Device: {device_id}\n"
   
    return send_telegram_notification(
        message=message,
        title="🆘 URGENT - Help Request",
        include_timestamp=True
    )




def notify_emergency(user_id: str, device_id: str = None) -> bool:
    message = f"🚨 <b>EMERGENCY ALERT</b>\n\n"
    message += f"User: {user_id}\n"
    if device_id:
        message += f"Device: {device_id}\n"
    message += "\n⚠️ IMMEDIATE ACTION REQUIRED"
   
    return send_telegram_notification(
        message=message,
        title="🚨 CRITICAL - EMERGENCY",
        include_timestamp=True
    )
