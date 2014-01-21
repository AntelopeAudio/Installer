# -*- coding: utf-8 -*-

import pkg_resources
import subprocess

from installer.commands import RunScriptCommand
from installer_platinum.res import Resources


res = Resources()


class Command(RunScriptCommand):
    dialog_checkboxes = res.install_cb
    dialog_feedback = res.install_feedback
    dialog_message = res.install_message
    dialog_title = res.install_title
    dialog_wait = res.install_wait
    script = pkg_resources.resource_filename(
        'installer_platinum_res',
        'burn/install.bash'
    )

    def on_dialog_success(self, checkboxes):
        if checkboxes.get('run_after_install', False):
            run = pkg_resources.resource_filename(
                'installer_platinum_res',
                'burn/run_after_install.bash'
            )
            subprocess.call(run)
