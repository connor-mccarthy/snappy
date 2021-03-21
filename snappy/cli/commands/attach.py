from cleo import Command
from snappy.cli.commands.invoke import InvokeCommand
from snappy.cli.constants import LIBRARY_NAME, YAML_FILE
from snappy.cli.helpers.aws.ecr import (
    get_default_image_name,
    get_repository_uri_from_name,
)
from snappy.cli.helpers.aws.general import get_role_arn_by_name
from snappy.cli.helpers.aws.iam import (
    attach_policy_to_role,
    create_lambda_ecr_role,
    create_policy,
)
from snappy.cli.helpers.aws.lambda_function import (
    create_lambda_function,
    list_functions_by_name,
    update_function_code,
)
from snappy.cli.helpers.yaml_helpers import read_configuration_yaml
from snappy.cli.styles import command_style, file_style


class AttachCommand(Command):
    name = "attach"
    help = f"""
    The {command_style(name)} command attaches your pushed image to the function specified in the {file_style(YAML_FILE)} file.

    If the specified function does not exist, you will be able to create it through the CLI, after which the most recent image in your ECR repository will be attached.
    """

    def handle(self) -> None:
        config_data = read_configuration_yaml()
        lambda_function_name = config_data["lambda_function_name"]
        repository_name = config_data["repository_name"]
        role_name = config_data["role_name"]

        repository_uri = get_repository_uri_from_name(repository_name)

        try:
            role_arn = get_role_arn_by_name(role_name)

        except ValueError as e:
            if "not found" not in str(e):
                raise e

            print(e)

            if not self.confirm(
                "<question>Would you like to create the role?</question>", False
            ):
                return

            description = self.ask(
                "<question>Please add a brief description for the role:</question>", ""
            )

            lambda_ecr_role_response = create_lambda_ecr_role(
                name=role_name, description=description
            )

            if self.io.is_verbose():
                self.line(str(lambda_ecr_role_response))

            role_arn = lambda_ecr_role_response["Role"]["Arn"]
            self.line(f"<info>Made your IAM role: {role_name}.</info>")
            self.line("")

            self.line(
                "Now let's create a policy with the correct permissions to attach to your role."
            )
            policy_name = self.ask(
                "<question>What would you like to name the policy associated with your new role?</question>",
                "",
            )
            description = self.ask(
                "<question>Please add a brief description of your policy:</question>",
                "",
            )

            create_policy_response = create_policy(policy_name, description)

            if self.io.is_verbose():
                self.line(str(create_policy_response))

            policy_arn = create_policy_response["Policy"]["Arn"]
            self.line(f"<info>Made your IAM policy: {policy_name}.</info>")

            attach_policy_to_role_response = attach_policy_to_role(
                policy_arn, role_name
            )

            if self.io.is_verbose():
                self.line(str(attach_policy_to_role_response))

            self.line("<info>Attached policy {policy_name} to role {role_name}.</info>")

            self.line("")

        existing_lambda_functions = list_functions_by_name()

        if self.io.is_verbose():
            self.line("Found the following Lambda functions:")
            for function_name in existing_lambda_functions:
                self.line(f"- {function_name}")

        if lambda_function_name not in existing_lambda_functions:
            self.line("It looks like your Lambda function is not yet created.")

            repository_uri = get_default_image_name()
            if self.confirm("Would you like to create it now?", False):
                create_lambda_response = create_lambda_function(
                    lambda_function_name, repository_uri, role_arn
                )

                if self.io.is_verbose():
                    self.line(str(create_lambda_response))

                self.line(
                    f"<info>Created lambda function {lambda_function_name}!</info>"
                )

        else:
            repository_uri = get_default_image_name()
            update_function_code_response = update_function_code(
                lambda_function_name, repository_uri
            )

            if self.io.is_verbose():
                self.line(str(update_function_code_response))

            self.line("<info>🔁 Updating function code!</info>")
            self.line("It may take a few minutes for the change to take effect.")
            self.next_step_prompt()

    def next_step_prompt(self) -> None:
        self.line("")
        self.line(
            f"Run {command_style(f'{LIBRARY_NAME} {InvokeCommand.name}')} to test your Lambda function."
        )
