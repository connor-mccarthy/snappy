import json

import boto3
from snappy.cli.config import IAMClient
from snappy.cli.helpers.yaml_helpers import (
    get_ecr_repository_name,
    get_lambda_function_name,
)
from snappy.types import Boto3ReponseType


def get_account_id() -> str:
    return boto3.client("sts").get_caller_identity()["Account"]


def get_region() -> str:
    return boto3.session.Session().region_name


def create_policy(name: str, description: str) -> Boto3ReponseType:
    region = get_region()
    account_id = get_account_id()
    json_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "CloudWatchLogs",
                "Effect": "Allow",
                "Action": "logs:*",
                "Resource": "*",
            },
            {
                "Sid": "LambdaPermissions",
                "Effect": "Allow",
                "Action": "lambda:*",
                "Resource": f"arn:aws:lambda:{region}:{account_id}:function:{get_lambda_function_name()}",
            },
            {
                "Sid": "EcrPermissions",
                "Effect": "Allow",
                "Action": "ecr:*",
                "Resource": f"arn:aws:ecr:{region}:{account_id}:function:{get_ecr_repository_name()}",
            },
        ],
    }
    return IAMClient.create_policy(
        PolicyName=name,
        PolicyDocument=json.dumps(json_policy),
        Description=description,
    )


def create_lambda_ecr_role(name: str, description: str) -> Boto3ReponseType:
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {"Service": "ec2.amazonaws.com"},
                "Action": "sts:AssumeRole",
            },
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole",
            },
        ],
    }
    return IAMClient.create_role(
        RoleName=name,
        Description=description,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
    )


def attach_policy_to_role(policy_arn: str, role_name: str) -> Boto3ReponseType:
    return IAMClient.attach_role_policy(PolicyArn=policy_arn, RoleName=role_name)
