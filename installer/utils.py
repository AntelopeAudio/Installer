# -*- coding: utf-8 -*-

import functools
import subprocess
import sys


def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in range(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


# if six.PY3:
#     from importlib import import_module
# else:
def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]


def is_root():
    """
    Return True if current user is root
    """
    try:
        return subprocess.check_output(['whoami']).strip() == 'root'
    except subprocess.CalledProcessError:
        return False


def is_sudoer():
    """
    Return True if current user is sudoer
    """
    process = subprocess.Popen(['sudo', '-n', '-v'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    com = process.communicate()
    if any('may not run sudo' in s for s in com):
        return False
    return True


def has_program(program):
    try:
        subprocess.check_output(['which', program])
        return True
    except subprocess.CalledProcessError:
        return False


has_gksudo = functools.partial(has_program, 'gksudo')
has_gksu = functools.partial(has_program, 'gksu')
has_kdesu = functools.partial(has_program, 'kdesu')
