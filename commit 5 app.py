
import streamlit as st
import streamlit.components.v1 as components
from shared import (
    CONFIG, HISTORY, trigger, user_signup, user_login, register_device,
    get_user_devices, add_caretaker, get_accessible_accounts, _load_users,
    set_user_theme, get_user_profile, verify_security_answer, reset_password,
    SECURITY_QUESTIONS, get_user_medicines, set_user_medicines
)

st.set_page_config(page_title="Assistive Buttons", layout="wide", initial_sidebar_state="collapsed")

def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "email" not in st.session_state:
        st.session_state.email = None
    if "device_id" not in st.session_state:
        import uuid
        st.session_state.device_id = str(uuid.uuid4())[:8]
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "show_medicine_modal" not in st.session_state:
        st.session_state.show_medicine_modal = False
    if "show_help_modal" not in st.session_state:
        st.session_state.show_help_modal = False
    if "help_request_text" not in st.session_state:
        st.session_state.help_request_text = ""

init_session_state()

DEFAULT_MEDICINES_LIST = [
    {"name": "Aspirin", "dosage": "500mg", "icon": ""},
    {"name": "Ibuprofen", "dosage": "200mg", "icon": ""},
    {"name": "Paracetamol", "dosage": "500mg", "icon": ""},
    {"name": "Vitamin C", "dosage": "1000mg", "icon": ""},
    {"name": "Blood Pressure Med", "dosage": "As prescribed", "icon": ""},
    {"name": "Insulin", "dosage": "As prescribed", "icon": ""},
]


 
init_session_state()


theme_css = """
body { background-color: #0f1419; color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
[data-testid="stMainBlockContainer"] { background-color: #0f172a; color: #ffffff; }
[data-testid="stSidebar"] { background-color: #1a1f3a; color: #ffffff; }
.auth-card { background: #1a1f3a; border-radius: 16px; padding: 40px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3); border: 1px solid #2d3d5f; }
input, select, textarea { background-color: #1e2a47 !important; color: #ffffff !important; border-radius: 8px !important; border: 1px solid #2d3d5f !important; padding: 12px 14px !important; }
input:focus, select:focus, textarea:focus { background-color: #3a3a3a !important; border: 2px solid #667eea !important; outline: none !important; }
.stButton > button { border-radius: 8px !important; height: 44px !important; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; color: white !important; border: none !important; }
h1, h2, h3, h4, h5, h6, p, span, label, li { color: #ffffff !important; }
a { color: #667eea !important; }
"""

st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)

def logout():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.email = None
    st.session_state.page = "home"
    st.rerun()

def show_auth_page():
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align: center; margin-bottom: 8px;">Assistive Buttons</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #a0aec0; font-size: 14px; margin-bottom: 32px;">Empowering the disabled and elderly with simple, accessible communication</p>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Forgot Password"])
        
        with tab1:
            st.markdown('<h3 style="margin-bottom: 24px;">Login to your account</h3>', unsafe_allow_html=True)
            login_email = st.text_input("Email", placeholder="your@email.com", key="login_email")
            login_password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")
            
            if st.button("Login", use_container_width=True):
                if login_email and login_password:
                    result = user_login(login_email, login_password)
                    if result["success"]:
                        st.session_state.logged_in = True
                        st.session_state.user_id = result["user_id"]
                        st.session_state.email = login_email
                        st.session_state.page = "home"
                        st.success("Login successful!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"{result['message']}")
                else:
                    st.error("Please enter email and password")
        
        with tab2:
            st.markdown('<h3 style="margin-bottom: 24px;">Create a new account</h3>', unsafe_allow_html=True)
            signup_name = st.text_input("Full name", placeholder="John Doe", key="signup_name")
            signup_phone = st.text_input("Phone (optional)", placeholder="+1 (555) 123-4567", key="signup_phone")
            signup_email = st.text_input("Email", placeholder="your@email.com", key="signup_email")
            signup_security_q = st.selectbox("Security Question", SECURITY_QUESTIONS, key="signup_security_q")
            signup_security_a = st.text_input("Your answer", placeholder="Your answer", key="signup_security_a")
            signup_password = st.text_input("Password", type="password", placeholder="••••••••", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="confirm_password")
            account_type = st.radio("Account Type", ["Primary (Disabled/Elderly)", "Caretaker/Family Member"], key="account_type", label_visibility="collapsed")
            
            if st.button("Sign Up", use_container_width=True):
                if not signup_email or not signup_password or not signup_security_a:
                    st.error("Please fill in all required fields")
                elif signup_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    is_primary = account_type == "Primary (Disabled/Elderly)"
                    result = user_signup(signup_email, signup_password, primary_account=is_primary, name=signup_name, phone=signup_phone, security_question=signup_security_q, security_answer=signup_security_a)
                    if result["success"]:
                        st.success(f"{result['message']}! You can now login.")
                    else:
                        st.error(f"{result['message']}")
        
        with tab3:
            st.markdown('<h3 style="margin-bottom: 24px;">Reset your password</h3>', unsafe_allow_html=True)
            reset_email = st.text_input("Email address", placeholder="your@email.com", key="reset_email")
            if st.button("Find Account", use_container_width=True, key="find_account_btn"):
                users_db = _load_users()
                found_user = None
                for uid, user in users_db.items():
                    if user["email"] == reset_email:
                        found_user = (uid, user)
                        break
                if found_user:
                    st.info(f"Security Question: {found_user[1].get('security_question', '')}")
                else:
                    st.error("Email not found")
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_main_app():
    page = st.session_state.get("page", "home")
    
    with st.sidebar:
        st.markdown(f'**Account:** {st.session_state.email}')
        st.markdown(f'**Device ID:** `{st.session_state.device_id}`')
        st.markdown("---\n**Navigation**")
        
        for label, page_key in [("Home", "home"), ("About", "about")]:
            if st.button(label, use_container_width=True, key=f"nav_{page_key}"):
                st.session_state.page = page_key
                st.rerun()
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True, key="logout_btn"):
            logout()

    if page == "home":
        components.html("""<script>setTimeout(()=>{ window.location.reload(); }, 2000);</script>""", height=0)
        
        st.markdown('<h1 style="text-align: center;">Assistive Buttons</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #a0aec0;">Simple, accessible communication for everyone</p>', unsafe_allow_html=True)
        
        col_lang = st.columns([1])[0]
        with col_lang:
            lang = st.selectbox("Language", options=["en", "hi", "it", "de", "fr", "es"], 
                format_func=lambda x: {"en":"English","hi":"Hindi","it":"Italian","de":"German","fr":"French","es":"Spanish"}[x],
                key="home_lang", label_visibility="collapsed")
        
        if st.session_state.show_help_modal:
            st.markdown('<h2 style="text-align: center;">What Help Do You Need?</h2>', unsafe_allow_html=True)
            help_text = st.text_area("Describe your help request", value=st.session_state.help_request_text, 
                placeholder="E.g., 'I need help getting out of bed'", key="help_text_input", height=100)
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("Send Help Request", use_container_width=True, key="help_submit_btn"):
                    if help_text.strip():
                        evt = trigger("BTN1", lang, source="UI", custom_text=f"Help needed: {help_text}",
                            device_id=st.session_state.device_id, user_id=st.session_state.user_id)
                        st.session_state.show_help_modal = False
                        st.session_state.help_request_text = ""
                        st.success("Help request sent!")
                        st.rerun()
                    else:
                        st.error("Please describe what help you need")
            with c2:
                if st.button("Cancel", use_container_width=True, key="help_cancel_btn"):
                    st.session_state.show_help_modal = False
                    st.rerun()
        
        if st.session_state.show_medicine_modal:
            user_medicines = get_user_medicines(st.session_state.user_id)
            medicines_to_display = user_medicines if user_medicines else DEFAULT_MEDICINES_LIST
            
            st.markdown('<h2 style="text-align: center;">Select Medicine</h2>', unsafe_allow_html=True)
            cols = st.columns(3)
            selected = False
            for idx, medicine in enumerate(medicines_to_display):
                with cols[idx % 3]:
                    if st.button(f"{medicine['icon']}\n{medicine['name']}\n{medicine['dosage']}", 
                        key=f"med_{idx}", use_container_width=True):
                        medicine_text = f"Give me {medicine['name']} ({medicine['dosage']})"
                        evt = trigger("BTN2", lang, source="UI", custom_text=medicine_text,
                            device_id=st.session_state.device_id, user_id=st.session_state.user_id)
                        st.session_state.show_medicine_modal = False
                        selected = True
            
            if selected:
                st.success("Medicine request recorded!")
                st.rerun()
            
            c1, c2, c3 = st.columns([1, 1, 1])
            with c2:
                if st.button("Close", use_container_width=True):
                    st.session_state.show_medicine_modal = False
                    st.rerun()
        
        st.markdown('<h2 style="text-align: center; margin-top: 30px;">Quick Action Buttons</h2>', unsafe_allow_html=True)
        
        button_configs = {
            "BTN1": {"icon": "", "color": "#ef4444"},
            "BTN2": {"icon": "", "color": "#10b981"},
            "BTN3": {"icon": "", "color": "#3b82f6"},
            "BTN4": {"icon": "", "color": "#8b5cf6"},
            "BTN5": {"icon": "", "color": "#f59e0b"},
            "BTN6": {"icon": "", "color": "#ec4899"},
        }
        
        col1, col2 = st.columns(2, gap="large")
        grid_cols = [col1, col2]
        
        for i, btn_key in enumerate(["BTN1", "BTN2", "BTN3", "BTN4", "BTN5", "BTN6"]):
            with grid_cols[i % 2]:
                btn_label = CONFIG[btn_key]["label"]
                btn_icon = button_configs[btn_key]["icon"]
                btn_color = button_configs[btn_key]["color"]
                
                st.markdown(f"""<div style="background: linear-gradient(135deg, {btn_color}20 0%, {btn_color}40 100%);
                    border: 2px solid {btn_color}; border-radius: 16px; padding: 32px 20px; margin: 16px 0;
                    text-align: center; box-shadow: 0 0 20px rgba(100,100,100,0.3); cursor: pointer;">
                    <div style="font-size: 56px; margin-bottom: 12px;">{btn_icon}</div>
                    <div style="font-size: 20px; font-weight: 700;">{btn_label}</div></div>""", unsafe_allow_html=True)
                
                if st.button(f"> {btn_label}", use_container_width=True, key=f"btn_play_{btn_key}"):
                    if btn_key == "BTN1":
                        st.session_state.show_help_modal = True
                        st.rerun()
                    elif btn_key == "BTN2":
                        st.session_state.show_medicine_modal = True
                        st.rerun()
                    else:
                        lang = st.session_state.get("home_lang", "en")
                        custom_text = CONFIG[btn_key]["texts"].get(lang, CONFIG[btn_key]["texts"]["en"])

                        with st.spinner("Speaking..."):
                            evt = trigger(
                                btn_key,
                                lang,
                                source="UI",
                                custom_text=custom_text,
                                device_id=st.session_state.device_id,
                                user_id=st.session_state.user_id
                            )

                            audio_bytes = evt.get("audio")
                            if audio_bytes:
                                st.audio(audio_bytes, format="audio/mp3")

                            spoken_text = evt.get("text", "Unknown")
                            st.success(f"Spoken: **{spoken_text}**")
        
        st.markdown('---')
        with st.expander("Customize Buttons", expanded=False):
            edit_tabs = st.tabs(["Labels", "Languages", "Test Audio", "Medicines"])
            
            with edit_tabs[0]:
                st.markdown('**Update button labels:**')
                for btn_key in ["BTN1", "BTN2", "BTN3", "BTN4", "BTN5", "BTN6"]:
                    CONFIG[btn_key]["label"] = st.text_input(f"{btn_key} Label", CONFIG[btn_key]["label"], key=f"label_edit_{btn_key}")
            
            with edit_tabs[1]:
                st.markdown('**Update text for languages:**')
                for btn_key in ["BTN1", "BTN2", "BTN3", "BTN4", "BTN5", "BTN6"]:
                    st.markdown(f"**{btn_key}: {CONFIG[btn_key]['label']}**")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        CONFIG[btn_key]["texts"]["en"] = st.text_input(f"{btn_key} EN", CONFIG[btn_key]["texts"]["en"], key=f"en_edit_{btn_key}")
                    with c2:
                        CONFIG[btn_key]["texts"]["hi"] = st.text_input(f"{btn_key} HI", CONFIG[btn_key]["texts"]["hi"], key=f"hi_edit_{btn_key}")
                    with c3:
                        CONFIG[btn_key]["texts"]["it"] = st.text_input(f"{btn_key} IT", CONFIG[btn_key]["texts"]["it"], key=f"it_edit_{btn_key}")
            
            with edit_tabs[2]:
                test_lang = st.selectbox("Select Language", ["en", "hi", "it", "de", "fr", "es"], key="test_tts_lang")
                test_text = st.text_area("Text to speak", placeholder="Enter text to hear it read aloud...")
                if st.button("Play Test", use_container_width=True):
                    if test_text:
                        from shared import speak_text
                        speak_text(test_text, test_lang)
                        st.success("Audio played!")
                    else:
                        st.error("Please enter text")
            
            with edit_tabs[3]:
                st.markdown('**Your medicines:**')
                user_medicines = get_user_medicines(st.session_state.user_id)
                if not user_medicines:
                    user_medicines = DEFAULT_MEDICINES_LIST.copy()
                
                updated_medicines = []
                for idx, med in enumerate(user_medicines):
                    c1, c2, c3 = st.columns([2, 2, 2])
                    with c1:
                        name = st.text_input(f"Medicine {idx+1} Name", med.get("name", ""), key=f"med_name_{idx}")
                    with c2:
                        dosage = st.text_input(f"Dosage", med.get("dosage", ""), key=f"med_dosage_{idx}")
                    with c3:
                        icon = st.text_input(f"Icon", med.get("icon", ""), key=f"med_icon_{idx}")
                    if name:
                        updated_medicines.append({"name": name, "dosage": dosage, "icon": icon})
                
                if st.button("Save Medicines", use_container_width=True):
                    if updated_medicines:
                        set_user_medicines(st.session_state.user_id, updated_medicines)
                        st.success("Medicines saved!")
                        st.rerun()
                    else:
                        st.error("Please add at least one medicine")
    
    elif page == "about":
        st.markdown('<h2>About Assistive Buttons</h2>', unsafe_allow_html=True)
        st.markdown("""
        **Assistive Buttons** is a simple, accessible communication tool designed for the disabled and elderly.
        
        ### Features:
        - 6 Quick action buttons for common needs
        - Multi-language support (English, Hindi, Italian, German, French, Spanish)
        - Customizable button labels and messages
        - Medicine tracking and requests
        - Help request system
        - Text-to-speech functionality
        
        ### How to use:
        1. Select your language
        2. Press any button to trigger its action
        3. Listen to the spoken message
        4. Customize buttons in settings if needed
        """)

if not st.session_state.logged_in:
    show_auth_page()
else:
    show_main_app()

    