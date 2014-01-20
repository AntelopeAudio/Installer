# -*- coding: utf-8 -*-

from installer.utils import import_module


def load_command_class(modname, cmdname):
    """
    Given a command name and an application name, returns the Command
    class instance. All errors raised by the import process
    (ImportError, AttributeError) are allowed to propagate.
    """
    module = import_module('%s.commands.%s' % (modname, cmdname))
    return module.Command()


def execute_command(modname, cmdname, *args, **kwargs):
    inst = load_command_class(modname, cmdname)
    ret = inst.execute(*args, **kwargs)
    return ret


class BaseCommand(object):
    def execute(self, *args, **kwargs):
        pass
