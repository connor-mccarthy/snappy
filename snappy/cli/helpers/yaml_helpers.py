import dataclasses
import os
from typing import Any, Dict

import yaml
from snappy.cli.constants import YAML_FILE
from snappy.cli.helpers.common import get_app_dir

YamlData = Dict[str, Any]


def get_yaml_path() -> str:
    app_dir = get_app_dir()
    return os.path.join(app_dir, YAML_FILE)


def write_configuration_yaml(data: YamlData) -> None:
    filepath = get_yaml_path()
    with open(filepath, "w") as f:
        yaml.dump(data, f)
    return yaml.dump(data)


def read_configuration_yaml() -> YamlData:
    filepath = get_yaml_path()
    with open(filepath, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            raise e


def get_lambda_function_name() -> str:
    return read_configuration_yaml()["lambda_function_name"]


def get_ecr_repository_name() -> str:
    return read_configuration_yaml()["repository_name"]


def get_role_name() -> str:
    return read_configuration_yaml()["role_name"]


def delete_existing_yaml_files() -> None:
    filepath = get_yaml_path()
    if os.path.isfile(filepath):
        os.remove(filepath)


@dataclasses.dataclass
class YamlConfig:
    lambda_function_name: str
    role_name: str
    repository_name: str

    def to_dict(self) -> YamlData:
        return dataclasses.asdict(self)
