import json
import random
import openai
import logging
from openai import OpenAI
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_caller_profiles(system_prompt, num_profiles=10):
    client = OpenAI()

    logging.info(f"Generating {num_profiles} caller profiles...")
    gpt_prompt = f"""
    Given the following system prompt for a voice agent in a hospital context:
    "{system_prompt}"
    Generate {num_profiles} distinct caller profiles with the following information for each:
    - A unique personality and background description.
    - A specific issue or request that this caller might have.
    - An expected call duration (in seconds) which should be a random value between 20 and 300.
    
    Return ONLY a valid JSON array of objects with no additional text, each object having keys: 'profile_id', 'personality', 'issue', 'call_duration'.
    The response should be parseable by json.loads() in Python.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates testing scenarios. Return only valid JSON with no additional text."},
                {"role": "user", "content": gpt_prompt}
            ],
            temperature=0.7,
            max_tokens=800,
            response_format={"type": "json_object"}  
        )
        result_text = response.choices[0].message.content.strip()
        
        try:
            json_data = json.loads(result_text)
            
            if isinstance(json_data, dict):
                for key in json_data:
                    if isinstance(json_data[key], list):
                        profiles = json_data[key]
                        break
                else:
                    if all(k in json_data for k in ['profile_id', 'personality', 'issue', 'call_duration']):
                        profiles = [json_data]
                    else:
                        raise ValueError("JSON response doesn't contain expected profile data")
            elif isinstance(json_data, list):
                profiles = json_data
            else:
                raise ValueError("JSON response is neither a list nor a dictionary")
                
            for profile in profiles:
                if not all(k in profile for k in ['profile_id', 'personality', 'issue', 'call_duration']):
                    raise ValueError("Some profiles are missing required fields")
                    
            logging.info(f"Successfully generated {len(profiles)} caller profiles using GPT")

        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\[\s*{.*}\s*\]', result_text, re.DOTALL)
            if json_match:
                try:
                    profiles = json.loads(json_match.group(0))
                except:
                    raise ValueError("Could not parse JSON from response")
            else:
                raise ValueError("No JSON array found in response")
                
    except Exception as e:
        logging.error("Error generating caller profiles using GPT: %s", e)
        profiles = []
        for i in range(1, num_profiles + 1):
            profile = {
                "profile_id": f"profile_{i}",
                "personality": f"Caller {i}: friendly and inquisitive",
                "issue": f"Caller {i} has a general inquiry about hospital services.",
                "call_duration": random.randint(20, 300)
            }
            profiles.append(profile)
        logging.info("Fallback profiles generated")
    
    return profiles
    



