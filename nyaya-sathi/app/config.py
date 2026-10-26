"""
Nyaya Sathi Configuration Module
Handles environment variables, API configurations, and system defaults.
"""
import os
import json

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Server Configuration
HOST = os.environ.get("NYAYA_HOST", "127.0.0.1")
PORT = int(os.environ.get("NYAYA_PORT", 8080))

# Sarvam AI Credentials & Configuration
# Inspects environment variable SARVAM_API_KEY
SARVAM_API_KEY = os.environ.get("SARVAM_API_KEY", "")
SARVAM_BASE_URL = "https://api.sarvam.ai"

SARVAM_MODELS = {
    "stt": os.environ.get("SARVAM_STT_MODEL", "saaras:v4"),
    "tts": os.environ.get("SARVAM_TTS_MODEL", "bulbul:v1"),
    "translate": os.environ.get("SARVAM_TRANSLATE_MODEL", "sarvam-translate:v1"),
    "tts_speaker": os.environ.get("SARVAM_TTS_SPEAKER", "meera")
}

# Supported Languages (BCP-47 codes)
SUPPORTED_LANGUAGES = {
    "mr-IN": {
        "code": "mr-IN",
        "name": "Marathi",
        "native": "मराठी",
        "default_voice": "hi-IN" # fallback voice tag
    },
    "hi-IN": {
        "code": "hi-IN",
        "name": "Hindi",
        "native": "हिन्दी",
        "default_voice": "hi-IN"
    },
    "en-IN": {
        "code": "en-IN",
        "name": "English",
        "native": "English (India)",
        "default_voice": "en-IN"
    }
}

DEFAULT_LANGUAGE = "hi-IN"

# Verification and Safety Settings
PRIVACY_WARNING = (
    "सुरक्षा सूचना / Privacy Warning: कृपया आधार क्रमांक, बँक खाते, पासवर्ड किंवा वैयक्तिक गुप्त माहिती टाकू नका. "
    "Do not enter Aadhaar numbers, OTPs, bank credentials, or passwords."
)

LEGAL_DISCLAIMER = (
    "न्याय साथी हे एक एआय-आधारित कायदेशीर माहिती सहाय्यक आहे. हे वकील, न्यायालय किंवा सरकारी प्राधिकरण नाही. "
    "हे अधिकृत कायदेशीर सल्ला नाही. गंभीर किंवा तातडीच्या बाबींसाठी कृपया जिल्हा विधी सेवा प्राधिकरण (DLSA) किंवा पात्र वकिलांचा सल्ला घ्या. "
    "Nyaya Sathi is an AI legal-information assistant. It is not a lawyer, court, or government department. "
    "Information provided is for educational navigation and does not constitute formal legal counsel."
)
