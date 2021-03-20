from collections import OrderedDict

from cleo import Command
from snappy.cli.commands.attach import AttachCommand
from snappy.cli.config import DockerClientInstance
from snappy.cli.constants import DEFAULT_IMAGE_TAG, LIBRARY_NAME, YAML_FILE
from snappy.cli.helpers.aws.ecr import (
    create_ecr_repository,
    get_repository_uri_from_name,
)
from snappy.cli.helpers.docker_helpers import (
    get_default_lambda_image,
    log_in_docker_to_ecr,
)
from snappy.cli.helpers.yaml_helpers import read_configuration_yaml
from snappy.cli.styles import command_style, file_style


class PushCommand(Command):
    name = "push"
    help = f"""
    The {command_style(name)} command will push your image to the ECR repository specified in the {file_style(YAML_FILE)} file.

    If the specified repository does not exist, you will be able to create it through the CLI.
    """

    def handle(self) -> None:
        repository_name = read_configuration_yaml()["repository_name"]

        if self.io.is_verbose():
            self.line(f"Repository name: {repository_name}")

        uri = get_repository_uri_from_name(repository_name)

        if self.io.is_verbose():
            self.line(f"Repository uri: {uri}")

        if not uri:
            self.line(f"It looks like ECR repository {repository_name} does not exist.")
            if self.confirm("Would you like to create it?", False):
                response = create_ecr_repository(repository_name)

                if self.io.is_verbose():
                    self.line(str(response))

                self.write("🏛️ Creating repository {repository_name}...")
                while not uri:
                    uri = get_repository_uri_from_name(repository_name)

                self.overwrite("<info>All set!</info>")
                self.line("")
            else:
                self.line("Please create this repository yourself before continuing.")
                return

        response = log_in_docker_to_ecr()

        if self.io.is_verbose():
            self.line(f"Docker log in to ECR: {str(response)}")

        if response["Status"] != "Login Succeeded":
            self.line("<error>Docker log in to ECR failed.</error>")
            return

        image = get_default_lambda_image()
        image.tag(uri, DEFAULT_IMAGE_TAG)

        self.add_style("processing", options=["blink"])
        self.line(
            f"<processing>🚀 Pushing your image to {repository_name}...</processing>"
        )
        self.line("This may take a bit...")
        self.line("Hint: Use verbosity flag -v or greater for additional logging.")
        self.line("")

        progress_dict = OrderedDict()
        for line in DockerClientInstance.images.push(
            uri, DEFAULT_IMAGE_TAG, stream=True, decode=True
        ):
            if ("progress" in line) and self.io.is_verbose():
                progress_dict[line["id"]] = line["progress"]
                progress_log = "\n".join(
                    f"{_id}: {progress}" for _id, progress in progress_dict.items()
                )
                self.overwrite(progress_log)

        self.line(f"<info>🎉 {uri}/{DEFAULT_IMAGE_TAG} pushed to ECR.</info>")
        self.next_step_prompt()

    def next_step_prompt(self) -> None:
        self.line("")
        self.line(
            f"Run {command_style(f'{LIBRARY_NAME} {AttachCommand.name}')} to attach your new image to your Lambda function."
        )
