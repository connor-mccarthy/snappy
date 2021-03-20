from cleo import Command
from cleo.helpers import argument, option
from requests.exceptions import ConnectionError
from snappy.cli.commands.build import BuildCommand
from snappy.cli.commands.running import RunningCommand
from snappy.cli.commands.stop import StopCommand
from snappy.cli.constants import (
    DEFAULT_PAYLOAD,
    INFORMAL_LOCAL_CONTAINER_NAME,
    LIBRARY_NAME,
    YAML_FILE,
)
from snappy.cli.helpers.aws.lambda_function import (
    get_running_lambdas,
    make_local_request,
    make_remote_request,
)
from snappy.cli.helpers.yaml_helpers import read_configuration_yaml
from snappy.cli.styles import command_style, file_style


class InvokeCommand(Command):
    arguments = [
        argument(
            "payload",
            "Payload to pass to your Lambda function. Optional. Defaults to empty payload.",
        )
    ]
    options = [
        option(
            "local",
            "l",
            "If set, the command will invoke the locally running Lambda container.",
        ),
        option(
            "body-only",
            "b",
            "If set, the command will only display the body of the response.",
        ),
    ]
    name = "invoke"
    help = f"""
    The {command_style(name)} command is used to test your Lambda function, both when running locally and in production.

    {command_style(name)} defaults to invoking your production Lambda function, specified by the name in your {file_style(YAML_FILE)} function.

    You can also invoke your function when it's running locally:

    {command_style(f"{LIBRARY_NAME} {name} --local")}
    """

    def handle(self) -> None:
        payload = self.argument("payload")
        local = self.option("local")
        body_only = self.option("body-only")
        running_lambdas = get_running_lambdas()

        if local and (len(running_lambdas) > 1):
            self.line(
                f"Cannot test Lambda locally. Found more than one running {INFORMAL_LOCAL_CONTAINER_NAME}."
            )
            self.line(
                f"To resolve, run {command_style(f'{LIBRARY_NAME} {StopCommand.name}')} to stop all running {INFORMAL_LOCAL_CONTAINER_NAME}s, then run {command_style(f'{LIBRARY_NAME} {BuildCommand.name}')} to redeploy the single correct Lambda container."
            )

        data = payload or DEFAULT_PAYLOAD

        if local:
            try:
                response = make_local_request(data)
            except ConnectionError as e:
                self.line(
                    f"<error>There was an issue connecting to your container. Run {command_style(f'{LIBRARY_NAME} {RunningCommand.name}')} to confirm that it's running.</error>"
                )
                raise e
        else:
            name = read_configuration_yaml()["lambda_function_name"]
            response = make_remote_request(data, name)

        print_response = str(response["body"]) if body_only else str(response)
        self.add_style("response", fg="magenta")
        self.line(f"<response>{print_response}</response>")
