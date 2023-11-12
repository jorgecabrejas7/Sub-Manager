from registry.command_registry import CommandRegistry

def register_command(name):
    def decorator(command_class):
        CommandRegistry.register_command(name, command_class)
        return command_class
    return decorator
