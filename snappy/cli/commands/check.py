import os
from typing import List

from cleo import Command
from snappy.cli.commands.build import BuildCommand
from snappy.cli.commands.init import InitCommand
from snappy.cli.constants import (
    APP_FILE,
    INFORMAL_LOCAL_IMAGE_NAME,
    LIBRARY_NAME,
    REQUIREMENTS_FILE,
    YAML_FILE,
)
from snappy.cli.helpers.common import find_file
from snappy.cli.styles import command_style, file_style


class CheckCommand(Command):
    name = "check"
    help = f"""
    The {command_style(name)} command validates the structure of your project. This evaluation happens relative to the working directory where the command is run.

    The structure requirements are:
    * One {file_style(APP_FILE)} file beneath working directory
    * One {file_style(REQUIREMENTS_FILE)} file in the same directory as your {file_style(APP_FILE)} file
    * One {file_style(YAML_FILE)} file in the same directory as your {file_style(APP_FILE)} file.

    If there is no {file_style(YAML_FILE)} file in your project, you will be prompted to create one with the {command_style(InitCommand.name)} command.
    """

    def handle(self) -> bool:
        app_paths = find_file(os.getcwd(), APP_FILE)
        self.describe_findings(app_paths, APP_FILE)

        single_app = len(app_paths) != 1
        if single_app:
            self.line(
                f"<error>Could not identify application directory. Please ensure there is only one {APP_FILE} file beneath current working directory.</error>"
            )
            return False
        else:
            app_dir = os.path.dirname(app_paths[0])

        requirements_paths = find_file(app_dir, REQUIREMENTS_FILE)
        self.describe_findings(requirements_paths, REQUIREMENTS_FILE)

        yaml_paths = find_file(app_dir, YAML_FILE)
        self.describe_findings(yaml_paths, YAML_FILE)

        paths = [app_paths, requirements_paths, yaml_paths]

        if all(len(path_list) == 1 for path_list in paths):
            self.line("")
            self.line("<info>🎉 All checks pass!</info>")
            self.next_step_prompt()
            return True

        if yaml_paths != 1:
            self.line(
                f"Run {command_style('{LIBRARY_NAME} init')} to configure a new yaml file for your project."
            )

        return False

    def describe_findings(self, paths: List[str], target_file: str) -> None:
        n_paths = len(paths)
        if n_paths == 0:
            self.line(f"<error>🛑 Could not find {target_file} file.</error>")
            self.line("")

        elif n_paths > 1:
            self.line(f"<error>🛑 Found {n_paths} {target_file} files.</error>")
            for path in paths:
                self.line(f"- {path}")
            self.line("")

        else:
            self.line(f"<info>✅ Found {target_file} at path {paths[0]}</info>")

    def next_step_prompt(self) -> None:
        self.line("")
        self.line(
            f"Run {command_style(f'{LIBRARY_NAME} {BuildCommand.name}')} to build your {INFORMAL_LOCAL_IMAGE_NAME}."
        )
