from cleo import Command
from docker.errors import ImageNotFound
from snappy.cli.commands.stop import StopCommand
from snappy.cli.constants import (INFORMAL_LOCAL_CONTAINER_NAME,
                                  INFORMAL_LOCAL_IMAGE_NAME, LIBRARY_NAME)
from snappy.cli.helpers.docker_helpers import run_default_lambda
from snappy.cli.styles import command_style


class RunCommand(Command):
    name = "run"
    help = f"""
    The {command_style(name)} command is a simple wrapper around Docker's run command, with a few Lambda-specific configurations. {command_style(name)} will run your Lambda container locally.
    """

    def handle(self) -> None:
        n_already_running = self.call_silent("running")

        if n_already_running:
            self.line(
                f"<error>Found {INFORMAL_LOCAL_CONTAINER_NAME}(s) already running locally."
            )
            self.call("running")
            return

        try:
            container = run_default_lambda()
            if self.io.is_verbose():
                self.line(
                    f"<info>📦 Container {container.id} running image {str(container.image.tags)}!</info>"
                )
            else:
                self.line("<info>📦 Container running!</info>")

        except ImageNotFound as e:
            self.line(
                f"<error>{INFORMAL_LOCAL_IMAGE_NAME} not found. Run <info>{LIBRARY_NAME} build</info> to build your {INFORMAL_LOCAL_IMAGE_NAME}.</error>"
            )
            raise e

        self.next_steps_prompt()

    def next_steps_prompt(self) -> None:
        self.line("")
        self.line(
            f"Run {command_style(f'{LIBRARY_NAME} {StopCommand.name}')} to stop your {INFORMAL_LOCAL_CONTAINER_NAME} at any time."
        )
        self.line(
            f"Run {command_style(f'{LIBRARY_NAME} invoke')} with the  {command_style('--local')} switch to test your function locally."
        )
