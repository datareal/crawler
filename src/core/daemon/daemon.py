import time

import src.modules.aws as aws

def handler(event: dict, content) -> dict:
    target: str = event.get('target') 
    reason: str = event.get('reason')
    payload: dict = event.get('payload')

    if reason == 'REQUEST_FORBBIDEN':
        time.sleep(30) # Sleep 30 seconds before continuing

    aws.invoke(target, payload)

    return {
        "status_code": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Target": target,
            "Reason": reason,
            "Payload": payload
        })
    }