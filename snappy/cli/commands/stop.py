from cleo import Command
from snappy.cli.commands.running import RunningCommand
from snappy.cli.constants import INFORMAL_LOCAL_CONTAINER_NAME, PYTHON_LAMBDA_BASE_IMAGE
from snappy.cli.helpers.aws.lambda_function import get_running_lambdas
from snappy.cli.styles import command_style, keyword_style


class StopCommand(Command):
    name = "stop"
    help = f"""
    The {command_style(name)} command will stop all running containers that are children of the Python 3.7 Lambda base image ({keyword_style(PYTHON_LAMBDA_BASE_IMAGE)}). These are the same containers that are listed by the {command_style(RunningCommand.name)} command.
    """

    def handle(self) -> None:
        running_lambdas = get_running_lambdas()

        if running_lambdas:
            self.line(f"Stopping running {INFORMAL_LOCAL_CONTAINER_NAME}s:")
            for container in running_lambdas:
                container.stop()
                self.line(f" - {container.id}")

        else:
            self.line(f"No running {INFORMAL_LOCAL_CONTAINER_NAME}s found.")
