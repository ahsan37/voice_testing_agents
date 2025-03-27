import time
import logging
from vapi_client import initiate_outbound_call, retrieve_call_log


def call_worker(caller_profile, results):
    logging.info("Worker started for %s", caller_profile["profile_id"])
    call_id = initiate_outbound_call(caller_profile)

    if call_id:
        duration = caller_profile["call_duration"]
        logging.info("Simulating call for %s for %d seconds", caller_profile["profile_id"], duration)
        time.sleep(duration) 

        call_log = retrieve_call_log(call_id)
        results.append({
            "profile_id": caller_profile["profile_id"],
            "call_id": call_id,
            "call_log": call_log
        })
        logging.info("Worker completed for %s", caller_profile["profile_id"])
    else:
        logging.error("Call initiation failed for %s; skipping retrieval", caller_profile["profile_id"])






