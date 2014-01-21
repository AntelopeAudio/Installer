# -*- coding: utf-8 -*-

import os.path
import pkg_resources
import subprocess
import sys
import threading
import types

from installer import dialogs, utils


DIALOG_SUCCESS = 100


def load_command_class(modname, cmdname):
    """
    Given a command name and an application name, returns the Command
    class instance. All errors raised by the import process
    (ImportError, AttributeError) are allowed to propagate.
    """
    module = utils.import_module('%s.commands.%s' % (modname, cmdname))
    return module.Command()


def execute_command(modname, cmdname, *args, **kwargs):
    inst = load_command_class(modname, cmdname)
    ret = inst.execute(*args, **kwargs)
    return ret


class BaseCommand(object):
    def execute(self, *args, **kwargs):
        pass


class RunScriptCommand(BaseCommand):
    script = None
    run_as_root = True

    dialog_checkboxes = {}
    dialog_feedback = {}
    dialog_message = ''
    dialog_title = ''
    dialog_wait = ''

    def get_script(self):
        return os.path.abspath(self.script)

    def execute(self, window):
        if not self.run_as_root or utils.is_root():
            return subprocess.call([self.get_script()])

        if utils.is_sudoer() and utils.has_gksudo():
            # Run gksudo
            return subprocess.call([
                'gksudo',
                self.get_script()
            ])

        if utils.has_gksu():
            # Run gksu
            return subprocess.call([
                'gksu',
                self.get_script()
            ])

        if utils.has_kdesu():
            # Run kdesu
            return subprocess.call([
                'kdesu',
                self.get_script()
            ])

        return self.run_pwdialog(window)

    def _worker(self, dialog):
        code = self.run_script(self.get_script(), dialog.get_password())
        if code == 0:
            dialog.response(DIALOG_SUCCESS)
        else:
            fb = self.dialog_feedback[code]
            if isinstance(fb, types.StringTypes):
                text, style = fb, 'error'
            else:
                text, style = fb
            dialog.show_feedback(text, style=style)

    def run_pwdialog(self, window):
        pwdialog = dialogs.PasswordDialog(
            window,
            message_format=self.dialog_message,
            title=self.dialog_title,
            checkboxes=self.dialog_checkboxes
        )

        def on_ok():
            pwdialog.show_loader(self.dialog_wait)
            t = threading.Thread(target=self._worker, args=[pwdialog])
            t.start()

        pwdialog.ok_cb = on_ok
        resp = pwdialog.run()
        pwdialog.destroy()
        if resp == DIALOG_SUCCESS:
            self.on_dialog_success(pwdialog.get_checkboxes())
            return 0
        return 1

    def on_dialog_success(self, checkboxes):
        pass

    def run_script(self, script, password):
        """
        Run given script as root.  Password is optional since current user
        may be root
        """
        runner = pkg_resources.resource_filename(
            'installer_res',
            'scripts/runner.sh'
        )
        return subprocess.call([runner, script, password])
