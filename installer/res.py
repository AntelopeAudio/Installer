# -*- coding: utf-8 -*-

import pkg_resources

from installer.utils import import_module


class BaseResources(object):

    modname = ''

    # Main
    title = ''
    header = ''
    header_fd = ''
    content = ''
    content_fd = ''
    _wizard_image = ''
    install_btn = 'Install'
    uninstall_btn = 'Uninstall'
    close_btn = 'Close'

    # Install
    install_title = ''
    install_message = ''
    install_cb = {}
    install_wait = ''
    install_feedback = {}
    install_success_title = ''
    install_success_message = ''

    # Uninstall
    uninstall_title = ''
    uninstall_message = ''
    uninstall_cb = {}
    uninstall_wait = ''
    uninstall_feedback = {}
    uninstall_success_title = ''
    uninstall_success_message = ''

    # Footer
    footer = ''

    @property
    def wizard_image(self):
        fn = self._wizard_image
        return pkg_resources.resource_filename(self.modname, fn)


def get_resources(modname):
    module = import_module('%s.res' % modname)
    return module.Resources()
