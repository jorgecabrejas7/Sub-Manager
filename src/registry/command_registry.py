class CommandRegistry:
    commands = {}

    @classmethod
    def register_command(cls, name, command_class):
        cls.commands[name] = command_class

    @classmethod
    def get_commands(cls):
        return cls.commands