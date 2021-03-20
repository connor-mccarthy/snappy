from cleo import Command
from snappy.cli.commands.attach import AttachCommand
from snappy.cli.commands.build import BuildCommand
from snappy.cli.commands.check import CheckCommand
from snappy.cli.commands.init import InitCommand
from snappy.cli.commands.push import PushCommand
from snappy.cli.styles import command_style


class DeployCommand(Command):
    name = "deploy"
    help = f"""
    The {command_style(name)} command is a meta command that runs {command_style(BuildCommand.name)}, {command_style(PushCommand.name)}, and {command_style(AttachCommand.name)} sequentially.

    The most simple possible workflow to deploy a Lambda function, barring any bugs, would be to run the {command_style(CheckCommand.name)}, {command_style(InitCommand.name)}, and {command_style(name)} commands sequentially.
    """

    def handle(self) -> None:
        self.call("build")
        self.call("push")
        self.call("attach")
