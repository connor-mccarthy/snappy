import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterator

from docker.models.containers import Container
from docker.models.images import Image
from snappy.cli.config import DockerClientInstance
from snappy.cli.constants import DOCKERFILE, LAMBDA_PORTS
from snappy.cli.helpers.aws.ecr import get_default_image_name, get_ecr_login
from snappy.cli.helpers.common import get_app_dir


def build_image() -> str:
    build_kwargs = dict(
        path=get_app_dir(),
        dockerfile=DOCKERFILE,
        tag=get_default_image_name(),
    )
    image = DockerClientInstance.images.build(**build_kwargs)
    return image[0].id


def run_container(image_id: str) -> Container:
    run_kwargs = dict(image=image_id, detach=True, ports=LAMBDA_PORTS)
    container = DockerClientInstance.containers.run(
        **run_kwargs
    )  # sourcery: keep named return variable
    return container


def run_default_lambda() -> Container:
    image = get_default_lambda_image()
    return DockerClientInstance.containers.run(
        image, ports=LAMBDA_PORTS, remove=True, detach=True
    )


def get_default_lambda_image() -> Image:
    return DockerClientInstance.images.get(name=get_default_image_name())


@contextmanager
def flush_existing_docker_config(registry: str) -> Iterator:
    """handles the known bug
    where existing stale creds cause login
    to fail.
    https://github.com/docker/docker-py/issues/2256
    """
    config = Path(Path.home() / ".docker" / "config.json")
    if os.path.isfile(str(config)):
        original = config.read_text()
        as_json = json.loads(original)
        if "auths" in as_json:
            as_json["auths"].pop(registry, None)
            config.write_text(json.dumps(as_json))
        try:
            yield
        finally:
            config.write_text(original)
    else:
        try:
            yield
        finally:
            pass


def log_in_docker_to_ecr() -> Dict[str, str]:
    ecr_login = get_ecr_login()
    with flush_existing_docker_config(registry=ecr_login["registry"]):
        response = DockerClientInstance.login(**ecr_login)
    return response
