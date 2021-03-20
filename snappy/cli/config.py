import os

import boto3
import docker

DockerClientInstance = docker.from_env()
if os.environ.get("CI", False):
    region_name = "us-east-2"
    ECRClient = boto3.client("ecr", region_name=region_name)
    LambdaClient = boto3.client("lambda", region_name=region_name)
    IAMClient = boto3.client("iam", region_name=region_name)
else:
    ECRClient = boto3.client(
        "ecr",
    )
    LambdaClient = boto3.client("lambda")
    IAMClient = boto3.client("iam")
