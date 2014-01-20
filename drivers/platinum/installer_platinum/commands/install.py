# -*- coding: utf-8 -*-

import pkg_resources
import subprocess

from installer.commands import BaseCommand


class Command(BaseCommand):
    def execute(self, *args, **kwargs):
        # Run commands/burn/install.sh
        runner = pkg_resources.resource_filename(
            'installer_platinum_res',
            'burn/runner.sh'
        )
        install = pkg_resources.resource_filename(
            'installer_platinum_res',
            'burn/install.bash'
        )
        password = kwargs['password']
        ret = subprocess.call(['bash', runner, install, password])
        if ret == 0:
            print('[python] Success!')
            cb = kwargs.get('checkboxes', {})
            if cb.get('run_after_install', False):
                run = pkg_resources.resource_filename(
                    'installer_platinum_res',
                    'burn/run_after_install.bash'
                )
                subprocess.call(run)
            return 0
        else:
            print('[PYTHON] Failure!')
            return 1
