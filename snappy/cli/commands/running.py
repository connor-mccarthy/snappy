from cleo import Command
from snappy.cli.constants import (
    INFORMAL_LOCAL_IMAGE_NAME,
    LIBRARY_NAME,
    PYTHON_LAMBDA_BASE_IMAGE,
)
from snappy.cli.helpers.aws.lambda_function import get_running_lambdas
from snappy.cli.styles import command_style, keyword_style


class RunningCommand(Command):
    name = "running"
    help = f"""
    The {command_style(name)} command will list all running containers that are children of the Python 3.7 Lambda base image ({keyword_style(PYTHON_LAMBDA_BASE_IMAGE)}). This is helpful for easy debugging and inspecting what ports are in use.
    """

    def handle(self) -> int:
        running_lambdas = get_running_lambdas()

        if running_lambdas:
            self.line(f"{len(running_lambdas)} running container:")

            for container in running_lambdas:
                self.line(f"- {container.id}")

            self.line("\n")
            self.line(
                f"Run {command_style('{LIBRARY_NAME} stop')} to stop all local {INFORMAL_LOCAL_IMAGE_NAME}s."
            )

        else:
            self.line(f"Found no running {INFORMAL_LOCAL_IMAGE_NAME}s.")

        return len(running_lambdas)
