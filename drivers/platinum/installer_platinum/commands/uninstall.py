# -*- coding: utf-8 -*-

import pkg_resources
import subprocess

from installer.commands import BaseCommand


class Command(BaseCommand):
    def execute(self, *args, **kwargs):
        # Run commands/burn/uninstall.sh
        runner = pkg_resources.resource_filename(
            'installer_platinum_res',
            'burn/runner.sh'
        )
        uninstall = pkg_resources.resource_filename(
            'installer_platinum_res',
            'burn/uninstall.sh'
        )
        password = kwargs['password']
        ret = subprocess.call(['bash', runner, uninstall, password])
        if ret == 0:
            print('[python] Success!')
            # TODO y: delete_configuration_files
            # cb = kwargs.get('checkboxes', {})
            return 0
        else:
            print('[PYTHON] Failure!')
            return 1
