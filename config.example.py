import os

VAPI_BASE_URL = "https://api.vapi.ai"
VAPI_API_KEY = os.getenv("VAPI_API_KEY", "your_vapi_key_here")

TWILIO_PHONE_NUMBER_ID = os.getenv("TWILIO_PHONE_NUMBER_ID", "your_twilio_phone_number_id_here")

REAL_AGENT_PHONE_NUMBER = os.getenv("REAL_AGENT_PHONE_NUMBER", "your_phone_number_here")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_key_here") 