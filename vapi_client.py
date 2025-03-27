import requests
import logging
from config import (VAPI_BASE_URL, VAPI_API_KEY, TWILIO_PHONE_NUMBER_ID, REAL_AGENT_PHONE_NUMBER)

vapi_headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json"
}

def initiate_outbound_call(caller_profile):
    system_prompt = (
        f"You are a patient calling a voice agent. "
        f"Your personality: {caller_profile['personality']}. "
        f"Your main issue: {caller_profile['issue']}. "
        "Please speak naturally and politely."
    )
    
    payload = {
        "assistant": {
            "name": f"PatientBot-{caller_profile['profile_id']}",
            "model": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    }
                ]
            },
            "firstMessageMode": "assistant-waits-for-user",
            "maxDurationSeconds": caller_profile["call_duration"]
        },
        "phoneNumberId": TWILIO_PHONE_NUMBER_ID,
        "customer": {
            "number": REAL_AGENT_PHONE_NUMBER
        }
    }

    try:   
        response = requests.post(f"{VAPI_BASE_URL}/call", headers = vapi_headers, json = payload)
        if response.status_code == 201:
            data = response.json()
            call_id = data.get("id")
            logging.info("Call initiated for %s, call_id: %s", caller_profile["profile_id"], call_id)
            return call_id
        else:
            logging.error(
                "Failed to initiate call for %s. Status: %s, Response: %s", 
                caller_profile["profile_id"], 
                response.status_code, 
                response.text
            )
            return None
    except Exception as e:
        logging.error("Exception during call initiation for %s: %s", caller_profile["profile_id"], e)
        return None


def retrieve_call_log(call_id):
    try:
        response = requests.get(f"{VAPI_BASE_URL}/call/{call_id}", headers = vapi_headers)
        if response.status_code == 200:
            logging.info("Call log retrieved for call_id: %s", call_id)
            return response.json()
        else:
            logging.error(
                "Failed to retrieve log for call_id: %s. Status: %s, Response: %s", 
                call_id, 
                response.status_code, 
                response.text
            )
            return None
    except Exception as e:
        logging.error("Exception retrieving log for call_id: %s: %s", call_id, e)
        return None



