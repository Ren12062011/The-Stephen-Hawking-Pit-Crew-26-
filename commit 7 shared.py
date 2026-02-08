
import pyttsx3
def speak_text(text, language="en"):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    
import subprocess
import platform


VOICES = {
    "en": "Samantha",  
    "hi": "Lekha",     
    "es": "Mónica",    
    "fr": "Thomas",    
    "de": "Anna",      
    "it": "Alice",     
}

def speak_text(text, language="en"):
   
    if not text or not text.strip():
        return
    
    try:
       
        voice_name = VOICES.get(language, "Samantha")
        
     
        if platform.system() == "Darwin":  
            subprocess.run(
                ["say", "-v", voice_name, text],
                check=True
            )
        else:
            print(f"TTS not supported on this platform. Text: {text}")
    
    except Exception as e:
        print(f"TTS Error: {str(e)}")

import json
import os
import hashlib
import secrets
from typing import Optional

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def _hash_password(password: str, salt: Optional[str] = None):
    if salt is None:
        salt = secrets.token_hex(8)
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${digest}"

def _verify_password(stored: str, password: str) -> bool:
    try:
        salt, digest = stored.split("$", 1)
        return hashlib.sha256((salt + password).encode("utf-8")).hexdigest() == digest
    except Exception:
        return False

def get_user_by_email(email: str) -> Optional[dict]:
    users = _load_users()
    return users.get(email.lower())

def user_signup(email: str, password: str, primary_account: bool = True, name: str = "", phone: str = "", security_question: str = "", security_answer: str = "") -> dict:

    users = _load_users()
    key = email.lower()
    
    if key in users:
        return {"success": False, "message": "Email already registered"}
    
    pwd_hash = _hash_password(password)
    account_type = "primary" if primary_account else "caretaker"
    
    users[key] = {
        "full_name": name,
        "phone": phone,
        "email": email,
        "security_question": security_question,
        "security_answer_hash": hashlib.sha256(security_answer.strip().lower().encode("utf-8")).hexdigest(),
        "password_hash": pwd_hash,
        "account_type": account_type,
        "created_at": None,
        "caretakers": [],
        "medicines": [],
        "theme": "light",
    }
    _save_users(users)
    return {
        "success": True,
        "message": "Account created successfully"
    }

def user_login(email: str, password: str) -> dict:
    user = get_user_by_email(email)
    if not user:
        return {"success": False, "message": "No account found for this email"}
    if not _verify_password(user.get("password_hash", ""), password):
        return {"success": False, "message": "Incorrect password"}
    return {
        "success": True,
        "message": "Login successful",
        "user_id": email.lower(),
        "user": user
    }

def verify_security_answer(email: str, answer: str) -> bool:
    user = get_user_by_email(email)
    if not user:
        return False
    expected = user.get("security_answer_hash", "")
    return hashlib.sha256(answer.strip().lower().encode("utf-8")).hexdigest() == expected

def reset_password(email: str, new_password: str):
    users = _load_users()
    key = email.lower()
    user = users.get(key)
    if not user:
        raise ValueError("No account found")
    user["password_hash"] = _hash_password(new_password)
    users[key] = user
    _save_users(users)
    return True



SECURITY_QUESTIONS = [
    "What is your pet's name?",
    "What city were you born in?",
    "What is your mother's maiden name?",
    "What was your first car?",
    "What is your favorite book?",
    "What school did you attend?",
    "What was your childhood nickname?",
    "What is your favorite color?",
]


CONFIG = {
    "BTN1": {
        "label": "Help",
        "texts": {
            "en": "I need help",
            "hi": "मुझे मदद चाहिए",
            "es": "Necesito ayuda",
            "fr": "J'ai besoin d'aide",
            "de": "Ich brauche Hilfe",
            "it": "Ho bisogno di aiuto",
        }
    },
    "BTN2": {
        "label": "Medicines",
        "texts": {
            "en": "Time for medicine",
            "hi": "दवा का समय",
            "es": "Hora de la medicina",
            "fr": "Heure du médicament",
            "de": "Zeit für Medizin",
            "it": "Ora della medicina",
        }
    },
    "BTN3": {
        "label": "Water",
        "texts": {
            "en": "I want water",
            "hi": "मुझे पानी चाहिए",
            "es": "Quiero agua",
            "fr": "Je veux de l'eau",
            "de": "Ich möchte Wasser",
            "it": "Voglio acqua",
        }
    },
    "BTN4": {
        "label": "Rest",
        "texts": {
            "en": "I want to rest",
            "hi": "मुझे आराम चाहिए",
            "es": "Quiero descansar",
            "fr": "Je veux me reposer",
            "de": "Ich möchte mich ausruhen",
            "it": "Voglio riposare",
        }
    },
    "BTN5": {
        "label": "Call Someone",
        "texts": {
            "en": "Please call someone",
            "hi": "कृपया किसी को बुलाएं",
            "es": "Por favor llama a alguien",
            "fr": "S'il vous plaît appellez quelqu'un",
            "de": "Bitte rufen Sie jemanden an",
            "it": "Per favore chiama qualcuno",
        }
    },
    "BTN6": {
        "label": "Emergency",
        "texts": {
            "en": "Emergency",
            "hi": "आपातकालीन",
            "es": "Emergencia",
            "fr": "Urgence",
            "de": "Notfall",
            "it": "Emergenza",
        }
    },
}


HISTORY = []

DEVICES_FILE = os.path.join(os.path.dirname(__file__), "devices.json")
EVENTS_FILE = os.path.join(os.path.dirname(__file__), "events.json")


def _load_devices():
    """Load devices from file."""
    if not os.path.exists(DEVICES_FILE):
        return {}
    try:
        with open(DEVICES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_devices(devices: dict):
    """Save devices to file."""
    with open(DEVICES_FILE, "w", encoding="utf-8") as f:
        json.dump(devices, f, indent=2)


def _load_events():
    """Load events from file."""
    if not os.path.exists(EVENTS_FILE):
        return []
    try:
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_events(events: list):
    """Save events to file."""
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)


def register_device(user_id: str, device_id: str, device_name: str) -> dict:
    """Register a new device for a user."""
    devices = _load_devices()
    if user_id not in devices:
        devices[user_id] = {}
    
    devices[user_id][device_id] = {
        "device_id": device_id,
        "device_name": device_name,
        "registered_at": None,
    }
    _save_devices(devices)
    return devices[user_id][device_id]


def get_user_devices(user_id: str) -> dict:
    """Get all devices registered for a user."""
    devices = _load_devices()
    return devices.get(user_id, {})


def trigger(button: str, language: str = "en", source: str = "UI", custom_text: str = None, 
            device_id: str = "unknown", user_id: str = "default") -> dict:
    """Trigger an event and generate audio."""
    text = custom_text or CONFIG.get(button, {}).get("texts", {}).get(language, "Button pressed")
    
    
    audio_bytes = None
    try:
        import io
        import threading
        from gtts import gTTS
        
        def get_audio():
            nonlocal audio_bytes
            try:
                tts = gTTS(text=text, lang=language[:2], slow=False)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                audio_bytes = audio_buffer.read()
            except Exception as e:
                print(f"gTTS error: {e}")
                audio_bytes = None
        
        # Run gTTS in a thread with timeout
        thread = threading.Thread(target=get_audio)
        thread.daemon = True
        thread.start()
        thread.join(timeout=5)  # 5 second timeout
        
        if thread.is_alive():
            print("Audio generation timed out, continuing without audio")
            audio_bytes = None
    except Exception as e:
        print(f"Audio generation error: {e}")
        audio_bytes = None
        # Fallback: Try to use local TTS
        try:
            speak_text(text, language)
        except:
            pass
    
  
    import datetime
    event = {
        "button": button,
        "language": language,
        "text": text,
        "source": source,
        "device_id": device_id,
        "user_id": user_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "audio": None, 
    }
    
  
    HISTORY.append(event)
    events = _load_events()
    events.append(event)
    _save_events(events)
    
    return {
        "button": button,
        "text": text,
        "language": language,
        "audio": audio_bytes,
        "timestamp": event["timestamp"],
    }


def add_caretaker(primary_email: str, caretaker_email: str) -> bool:
    """Add a caretaker relationship between a primary user and a caretaker."""
    users = _load_users()
    primary_key = primary_email.lower()
    caretaker_key = caretaker_email.lower()
    
    if primary_key not in users or caretaker_key not in users:
        raise ValueError("One or both users not found")
    
    if "caretakers" not in users[primary_key]:
        users[primary_key]["caretakers"] = []
    
    if caretaker_key not in users[primary_key]["caretakers"]:
        users[primary_key]["caretakers"].append(caretaker_key)
    
    _save_users(users)
    return True


def get_accessible_accounts(email: str) -> list:
    """Get list of accounts that this user can access (for caretakers)."""
    users = _load_users()
    user_key = email.lower()
    accessible = []
    
    
    for user_email, user_data in users.items():
        if "caretakers" in user_data and user_key in user_data["caretakers"]:
            accessible.append({
                "email": user_data.get("email"),
                "full_name": user_data.get("full_name"),
            })
    
    return accessible


def get_user_profile(email: str) -> Optional[dict]:
    """Get user profile information."""
    user = get_user_by_email(email)
    if not user:
        return None
    
   
    return {
        "full_name": user.get("full_name"),
        "email": user.get("email"),
        "phone": user.get("phone"),
        "account_type": user.get("account_type"),
    }


def set_user_theme(email: str, theme: str) -> bool:
    """Set user theme preference."""
    users = _load_users()
    user_key = email.lower()
    
    if user_key not in users:
        raise ValueError("User not found")
    
    users[user_key]["theme"] = theme
    _save_users(users)
    return True


def get_user_medicines(email: str) -> list:
    """Get list of medicines for a user."""
    user = get_user_by_email(email)
    if not user:
        return []
    
    return user.get("medicines", [])


def set_user_medicines(email: str, medicines: list) -> bool:
    """Set medicines for a user."""
    users = _load_users()
    user_key = email.lower()
    
    if user_key not in users:
        raise ValueError("User not found")
    
    users[user_key]["medicines"] = medicines
    _save_users(users)
    return True

