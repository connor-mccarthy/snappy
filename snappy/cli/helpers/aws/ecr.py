import base64
from typing import Dict, List, Optional

from snappy.cli.config import ECRClient
from snappy.cli.constants import DEFAULT_IMAGE_TAG
from snappy.cli.helpers.aws.iam import get_region
from snappy.cli.helpers.yaml_helpers import read_configuration_yaml
from snappy.types import Boto3ReponseType


def create_ecr_repository(name: str) -> Boto3ReponseType:
    return ECRClient.create_repository(
        repositoryName=name,
        imageTagMutability="MUTABLE",  # TODO make this immutable and add semver incrementation logic
        imageScanningConfiguration={"scanOnPush": True},
        encryptionConfiguration={
            "encryptionType": "AES256",
        },
    )


def get_default_image_name() -> str:
    registry_id = ECRClient.describe_registry()["registryId"]
    repository_name = read_configuration_yaml()["repository_name"]
    region = get_region()
    return f"{registry_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{DEFAULT_IMAGE_TAG}"


def list_repositories(registry_id: Optional[str] = None) -> List[Boto3ReponseType]:
    if registry_id:
        response = ECRClient.describe_repositories(registryId=registry_id)
    else:
        response = ECRClient.describe_repositories()
    return response["repositories"]


def list_repository_names(registry_id: Optional[str] = None) -> List[str]:
    repositories = list_repositories(registry_id)
    return [repository["repositoryName"] for repository in repositories]


def get_ecr_login() -> Dict[str, str]:
    token = ECRClient.get_authorization_token()
    username, password = (
        base64.b64decode(token["authorizationData"][0]["authorizationToken"])
        .decode()
        .split(":")
    )
    registry = token["authorizationData"][0]["proxyEndpoint"]
    return dict(username=username, password=password, registry=registry)


def get_repository_uri_from_name(name: str) -> str:
    repositories = list_repositories()
    for repository in repositories:
        if repository["repositoryName"] == name:
            return repository["repositoryUri"]
