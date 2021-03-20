from cleo import Command
from docker.errors import BuildError
from snappy.cli.commands.run import RunCommand
from snappy.cli.constants import (
    DEFAULT_IMAGE_TAG,
    INFORMAL_LOCAL_CONTAINER_NAME,
    LIBRARY_NAME,
    YAML_FILE,
)
from snappy.cli.helpers.docker_helpers import build_image
from snappy.cli.styles import command_style, file_style, keyword_style


class BuildCommand(Command):
    name = "build"
    help = f"""
    The {command_style(name)} command is a simple wrapper around Docker's build command, with a few Lambda-specific configurations. {command_style(name)} will build your Lambda container, naming it according to the ECR repository specified the {file_style(YAML_FILE)} file and tagging it as {keyword_style((DEFAULT_IMAGE_TAG))}.
    """

    def handle(self) -> None:
        checks_pass = self.call_silent("check")

        if not checks_pass:
            self.call("check")
            return

        try:
            self.add_style("processing", options=["blink"])
            self.write("<processing>🔨 Building your image...</processing>")
            build_image()  # TODO: add progress bar logging
            self.overwrite("<info>🎉 Image built!</info>")

        except BuildError as e:
            self.line("<error>❗ Something went wrong with building your image.</error>")

            for line in e.build_log:
                if self.io.is_verbose():
                    self.line(line)
                elif "stream" in line:
                    self.line(line["stream"].strip())

            raise e

    def next_step_prompt(self) -> None:
        self.line("")
        self.line(
            f"Run {command_style(f'{LIBRARY_NAME} {RunCommand.name}')} to run your {INFORMAL_LOCAL_CONTAINER_NAME}."
        )
