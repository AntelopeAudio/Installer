# -*- coding: utf-8 -*-

import gettext
import pkg_resources

from installer.res import BaseResources

localedir = pkg_resources.resource_filename('installer_platinum_res', 'locale')
_ = gettext.translation('messages', localedir=localedir, fallback=True).ugettext


class Resources(BaseResources):

    title = _('Zodiac Platinum control panel installer')
    header = _('<span size="20000">Zodiac Platinum control panel installer</span>')
    header_font_desc = "25.0"
    content = _('''\
This installer asks you for your <b>sudo</b> or <b>root</b> password and \
un/installs\nthe Zodiac Platinum control panel on your computer.

This program respects your privacy.  It is free software licensed under
the terms of the GNU General Public License version 3. The source code
for this installer program can be found <a
href="https://github.com/AntelopeAudio/Installer">here</a>.''')

    _wizard_image = 'images/platinum.png'
    install_btn = _('Install')
    uninstall_btn = _('Uninstall')
    close_btn = _('Close')

    install_title = _('Installation')
    install_message = _('''\
Please enter your sudo or root password to install Zodiac Platinum control \
panel.''')
    install_cb = {
        'run_after_install': (_('Run control panel after install'), True)
    }
    install_wait = _('Installing...')
    install_feedback = {
        0: '',
        1: _('Please check your password and try again'),
    }
    install_success_title = _('Success!')
    install_success_message = _('The control panel for your Zodiac Platinum \
is successfully installed')

    uninstall_title = _('Uninstallation')
    uninstall_message = _('''\
Please enter your sudo or root password to uninstall Zodiac Platinum control \
panel.''')
    uninstall_cb = {
        'delete_configuration_files': (_('Delete configuration files'), True)
    }
    uninstall_wait = _('Uninstalling...')
    uninstall_feedback = {
        0: '',
        1: _('Please check your password and try again'),
    }
    uninstall_success_title = _('Success!')
    uninstall_success_message = _('The control panel for your Zodiac Platinum \
is successfully uninstalled')

    footer = _('© Antelope audio 2014')

    @property
    def wizard_image(self):
        fn = self._wizard_image
        return pkg_resources.resource_filename('installer_platinum_res', fn)
