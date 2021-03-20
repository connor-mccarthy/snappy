import os

from cleo import Command
from snappy.cli.commands.build import BuildCommand
from snappy.cli.constants import (
    APP_FILE,
    ECR_NAME_REQUIREMENTS,
    INFORMAL_LOCAL_IMAGE_NAME,
    LAMBDA_NAME_REQUIREMENTS,
    LIBRARY_NAME,
    YAML_FILE,
)
from snappy.cli.helpers.common import find_file
from snappy.cli.helpers.yaml_helpers import (
    YamlConfig,
    delete_existing_yaml_files,
    get_yaml_path,
    read_configuration_yaml,
    write_configuration_yaml,
)
from snappy.cli.styles import command_style, file_style


class InitCommand(Command):
    name = "init"
    help = f"""
    The {command_style(name)} command helps you create a {file_style(YAML_FILE)} file in the same directory as your {file_style(APP_FILE)} file. It will interactively ask you to fill in the three fields snappy needs to configure your Lambda:
    * lambda_function_name
    * arn_name
    * repository_name

    If two {file_style(APP_FILE)} files are found beneath the working directory where this is run, it will throw an error.
    """

    def handle(self) -> None:
        app_paths = find_file(os.getcwd(), APP_FILE)

        single_app = len(app_paths) != 1
        if single_app:
            self.line(
                f"<error>Could not identify application directory. Please ensure there is only one {APP_FILE} file beneath current working directory.</error>"
            )
            return
        else:
            app_dir = os.path.dirname(app_paths[0])

        yaml_exists = find_file(app_dir, YAML_FILE)
        if yaml_exists and not self.confirm(
            f"<question>Would you like overwrite existing '{YAML_FILE}' file(s) with a new one?</question>",
            True,
        ):
            return

        delete_existing_yaml_files()
        self.create_yaml()
        self.line("")
        self.line(f"✨ Wrote configuration file to {get_yaml_path()}!")

        self.next_step_prompt()

    def create_yaml(self) -> None:
        self.line("")
        lambda_function_name = self.ask(
            f"<question>What is the name of the Lambda function you would like to deploy?\nIf one does not exist yet, what would you like to name it?</question>\n({LAMBDA_NAME_REQUIREMENTS}):"
        )
        self.line("")
        role_name = self.ask(
            "<question>What is the name of the ARN role which you would like to attach to this Lambda function?</question>\nIf one does not exist, what would you like to name it?"
        )
        self.line("")
        repository_name = self.ask(
            f"<question>From which ECR repository would you like to deploy your Lambda?\nIf one does not exist yet, what would you like to name it?</question>\n({ECR_NAME_REQUIREMENTS}):"
        )

        data = YamlConfig(
            lambda_function_name=lambda_function_name,
            role_name=role_name,
            repository_name=repository_name,
        ).to_dict()

        write_configuration_yaml(data)

        if self.io.is_verbose():
            self.line(str(read_configuration_yaml()))

    def next_step_prompt(self) -> None:
        self.line("")
        self.line(
            f"Run {command_style(f'{LIBRARY_NAME} {BuildCommand.name}')} to build your {INFORMAL_LOCAL_IMAGE_NAME}."
        )
