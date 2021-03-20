import json
from typing import Callable, Dict

from snappy.cli.constants import HEALTCHECK_RESPONSE
from snappy.types import JSONType


def set_handler(function: Callable) -> None:
    handler = event_processing_wrapper(function)
    g = function.__globals__  # type: ignore
    g["handler"] = handler


def event_processing_wrapper(function: Callable) -> Callable:
    def decorator(event: JSONType, context: Dict) -> JSONType:
        print("Received event:", event)
        event = process_event(event)
        if is_healthcheck(event):
            wake_up_response = HEALTCHECK_RESPONSE
            return api_gateway_format(wake_up_response)
        response = function(**event)
        return api_gateway_format(response)

    return decorator


def process_event(event: JSONType) -> Dict:
    if not isinstance(event, dict):
        raise ValueError(
            "Event is not a dictionary. Additional logic is needed in lambda_handler._process_event function."
        )

    if "body" in event:
        event = event["body"]

    return json.loads(event) if isinstance(event, str) else event  # type: ignore


def api_gateway_format(response: JSONType) -> JSONType:
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": response,
    }


def is_healthcheck(event: JSONType) -> bool:
    if isinstance(event, dict):
        return "healtcheck" in event
    elif isinstance(event, str):
        return event == "healtcheck"
