# -*- coding: utf-8 -*-

import pkg_resources

from installer.commands import RunScriptCommand
from installer_platinum.res import Resources


res = Resources()


class Command(RunScriptCommand):
    dialog_checkboxes = res.uninstall_cb
    dialog_feedback = res.uninstall_feedback
    dialog_message = res.uninstall_message
    dialog_title = res.uninstall_title
    dialog_wait = res.uninstall_wait
    script = pkg_resources.resource_filename(
        'installer_platinum_res',
        'burn/uninstall.bash'
    )

    def on_dialog_success(self, checkboxes):
        # TODO y: Remove ~/.antelope or should it be done automatically
        # in uninstall.bash?
        pass
