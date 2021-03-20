#!/usr/bin/env python

from cleo import Application
from snappy.cli.commands.attach import AttachCommand
from snappy.cli.commands.build import BuildCommand
from snappy.cli.commands.check import CheckCommand
from snappy.cli.commands.deploy import DeployCommand
from snappy.cli.commands.init import InitCommand
from snappy.cli.commands.invoke import InvokeCommand
from snappy.cli.commands.push import PushCommand
from snappy.cli.commands.run import RunCommand
from snappy.cli.commands.running import RunningCommand
from snappy.cli.commands.stop import StopCommand

commands = [
    InitCommand,
    CheckCommand,
    BuildCommand,
    RunCommand,
    RunningCommand,
    StopCommand,
    InvokeCommand,
    PushCommand,
    AttachCommand,
    DeployCommand,
]

application = Application("snappy", "0.1.0")
for CommandObj in commands:
    application.add(CommandObj())


def main() -> int:
    return application.run()


if __name__ == "__main__":
    main()
