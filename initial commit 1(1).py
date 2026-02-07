import streamlit as st
from shared import speak_text

st.set_page_config(
    page_title="Assistive Buttons",
    page_icon="🔘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

theme_css = """
<style>
    * { margin: 0; padding: 0; }
    body { background-color: #1a1a1a; color: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stApp { background-color: #1a1a1a; }
    
    /* Hide sidebar */
    [data-testid="stSidebar"] { display: none; }
    
    /* Main content */
    .main { background-color: #1a1a1a; }
    .stButton > button { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        font-weight: 600;
        padding: 20px;
        border-radius: 12px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
    
    /* Text input */
    .stTextInput input { 
        background-color: #333333;
        color: white;
        border: 1px solid #444444;
        border-radius: 8px;
        padding: 10px;
    }
    .stTextInput input::placeholder { color: #999999; }
    
    /* Selectbox */
    .stSelectbox { color: white; }
    [data-testid="stSelectbox"] { background-color: #333333; }
    
    /* Text content */
    h1, h2, h3, h4, h5, h6 { color: #ffffff; }
    p, span, label { color: #ffffff; }
    
    /* Success/error messages */
    .stSuccess { background-color: #22c55e; color: white; }
    .stError { background-color: #ef4444; color: white; }
    .stWarning { background-color: #f59e0b; color: white; }
</style>
"""
st.markdown(theme_css, unsafe_allow_html=True)

BUTTONS = {
    "BTN1": {
        "emoji": "🆘",
        "label": "Help",
        "text_en": "I need help",
        "text_hi": "मुझे मदद चाहिए",
        "text_es": "Necesito ayuda",
        "text_fr": "J'ai besoin d'aide",
        "text_de": "Ich brauche Hilfe",
        "text_it": "Ho bisogno di aiuto",
    },
    "BTN2": {
        "emoji": "💊",
        "label": "Medicines",
        "text_en": "Time for medicine",
        "text_hi": "दवा का समय",
        "text_es": "Hora de la medicina",
        "text_fr": "Heure du médicament",
        "text_de": "Zeit für Medizin",
        "text_it": "Ora della medicina",
    },
    "BTN3": {
        "emoji": "💧",
        "label": "Water",
        "text_en": "I want water",
        "text_hi": "मुझे पानी चाहिए",
        "text_es": "Quiero agua",
        "text_fr": "Je veux de l'eau",
        "text_de": "Ich möchte Wasser",
        "text_it": "Voglio acqua",
    },
    "BTN4": {
        "emoji": "😴",
        "label": "Rest",
        "text_en": "I want to rest",
        "text_hi": "मुझे आराम चाहिए",
        "text_es": "Quiero descansar",
        "text_fr": "Je veux me reposer",
        "text_de": "Ich möchte ruhen",
        "text_it": "Voglio riposare",
    },
    "BTN5": {
        "emoji": "📞",
        "label": "Come Here",
        "text_en": "Please come here",
        "text_hi": "कृपया यहाँ आएं",
        "text_es": "Por favor ven aquí",
        "text_fr": "S'il vous plaît venez ici",
        "text_de": "Bitte komm hier her",
        "text_it": "Per favore vieni qui",
    },
    "BTN6": {
        "emoji": "🚨",
        "label": "Emergency",
        "text_en": "Emergency help needed",
        "text_hi": "आपातकालीन मदद चाहिए",
        "text_es": "Se necesita ayuda de emergencia",
        "text_fr": "Aide d'urgence nécessaire",
        "text_de": "Notfallhilfe erforderlich",
        "text_it": "Aiuto di emergenza necessario",
    },
}

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "en"

st.markdown(
    '<h1 style="text-align: center; margin-bottom: 8px; color: #ffffff;">🔘 Assistive Buttons</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<p style="text-align: center; color: #cccccc; font-size: 14px; margin-bottom: 32px;">Press a button to hear the message</p>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    lang_map = {
        "en": "🇬🇧 English",
        "hi": "🇮🇳 Hindi",
        "es": "🇪🇸 Spanish",
        "fr": "🇫🇷 French",
        "de": "🇩🇪 German",
        "it": "🇮🇹 Italian",
    }
    selected_lang = st.selectbox(
        "Select Language",
        list(lang_map.keys()),
        format_func=lambda x: lang_map[x],
        key="language_selector",
        label_visibility="collapsed"
    )
    st.session_state.selected_language = selected_lang

st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)

st.markdown('<h2 style="color: #ffffff; text-align: center; margin-bottom: 24px;">Quick Actions</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")
columns = [col1, col2]

btn_keys = ["BTN1", "BTN2", "BTN3", "BTN4", "BTN5", "BTN6"]

for i, btn_key in enumerate(btn_keys):
    with columns[i % 2]:
        btn_config = BUTTONS[btn_key]
        emoji = btn_config["emoji"]
        label = btn_config["label"]
        lang_key = f"text_{st.session_state.selected_language}"
        text = btn_config.get(lang_key, btn_config["text_en"])

        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 40px 20px;
            text-align: center;
            margin: 16px 0;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            border: 2px solid rgba(255, 255, 255, 0.1);
        ">
            <div style="font-size: 64px; margin-bottom: 16px;">{emoji}</div>
            <div style="font-size: 24px; font-weight: 700; color: white; margin-bottom: 12px;">{label}</div>
            <div style="font-size: 14px; color: #e0e0e0; line-height: 1.5; min-height: 60px; display: flex; align-items: center; justify-content: center;">"{text}"</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Say {label}", use_container_width=True, key=f"btn_{btn_key}"):
            with st.spinner(f"Speaking: {label}..."):
                speak_text(text, st.session_state.selected_language)
            st.success(f"✅ {label} spoken!")

st.divider()
st.markdown('<h2 style="color: #ffffff; text-align: center; margin: 32px 0 24px 0;">📝 Custom Message</h2>', unsafe_allow_html=True)

custom_text = st.text_input(
    "Enter custom text to speak",
    placeholder="Type something and press the button below...",
    label_visibility="collapsed"
)

if custom_text:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Say Custom Message", use_container_width=True):
            with st.spinner("Speaking..."):
                speak_text(custom_text, st.session_state.selected_language)
            st.success("✅ Message spoken!")
