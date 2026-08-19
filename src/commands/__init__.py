class CommandManager:

   def __init__(self):
    self.commands = {}

    self.register("help", help_execute)
    self.register("version", version_execute)
    self.register("status", status_execute)
    self.register("clear", clear_execute)