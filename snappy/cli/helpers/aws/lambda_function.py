from typing import List

import requests
from docker.models.containers import Container
from snappy.cli.config import DockerClientInstance, LambdaClient
from snappy.cli.constants import HEADERS, LOCAL_ENDPOINT, PYTHON_LAMBDA_BASE_IMAGE
from snappy.cli.helpers.aws.general import decode_streaming_body_payload
from snappy.types import Boto3ReponseType, JSONType


def get_running_lambdas() -> List[Container]:
    return DockerClientInstance.containers.list(
        filters={"ancestor": PYTHON_LAMBDA_BASE_IMAGE}
    )


def update_function_code(name: str, uri: str) -> Boto3ReponseType:
    return LambdaClient.update_function_code(
        FunctionName=name,
        ImageUri=uri,
    )


def create_lambda_function(name: str, uri: str, role_arn: str) -> Boto3ReponseType:
    return LambdaClient.create_function(
        FunctionName=name,
        Role=role_arn,
        Code={
            "ImageUri": uri,
        },
        PackageType="Image",
    )


def list_functions_by_name() -> List[str]:
    response = LambdaClient.list_functions()
    return [function["FunctionName"] for function in response["Functions"]]


def make_local_request(payload: str) -> JSONType:
    raw_response = requests.request(
        "GET", LOCAL_ENDPOINT, headers=HEADERS, data=payload
    )
    return raw_response.json()


def make_remote_request(payload: str, name: str) -> JSONType:
    response = LambdaClient.invoke(
        InvocationType="RequestResponse",
        FunctionName=name,
        Payload=bytes(payload, encoding="utf8"),
        LogType="Tail",
    )
    return decode_streaming_body_payload(response["Payload"])


def get_function_arn_by_name(name: str) -> str:
    response = LambdaClient.get_function(FunctionName=name)
    return response["Configuration"]["FunctionArg"]
