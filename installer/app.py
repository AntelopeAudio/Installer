#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from threading import Thread
import types

import os
import gtk
import gobject

from installer import dialogs
from installer import res
from installer import commands

gobject.threads_init()


def install(modname, data):
    inst = commands.load_command_class(modname, 'install')
    return inst.execute(**data)


def uninstall(modname, data):
    inst = commands.load_command_class(modname, 'uninstall')
    return inst.execute(**data)


class Installer(object):

    padding = 5

    def __init__(self, resmodule):
        self.resmodule = resmodule
        self.res = res.get_resources(resmodule)

        # Setup UI
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect('delete_event', self._delete_event)
        self.window.connect('destroy', self._destroy)
        self.window.set_title(self.res.title)
        self.window.set_border_width(2)

        tophbox = gtk.HBox()
        tophbox.show()

        # Image
        wizard = gtk.Image()
        wizard.set_from_file(self.res.wizard_image)
        wizard.show()
        tophbox.pack_start(wizard)

        # Title, description
        vbox = gtk.VBox()
        vbox.show()
        tophbox.pack_start(vbox, padding=10)

        header = self._make_label(self.res.header, font_desc=self.res.header_fd)
        header.set_justify(gtk.JUSTIFY_CENTER)
        vbox.pack_start(header)

        desc = self._make_label(self.res.content,
                                font_desc=self.res.content_fd)
        vbox.pack_start(desc)

        # Buttons
        btnhbox = gtk.HBox()
        btnhbox.show()
        vbox.pack_start(btnhbox)

        buttons = [
            (self.res.install_btn, self._install),
            (self.res.uninstall_btn, self._uninstall),
            (self.res.close_btn, self._quit),
        ]
        for label, action in buttons:
            btn = gtk.Button(label)
            btn.show()
            btn.connect('clicked', action)
            btnhbox.pack_start(btn, padding=5)

        # Footer notice
        if self.res.footer:
            footer = self._make_label(self.res.footer)
            vbox.pack_start(footer)

        self.window.add(tophbox)
        self.window.show()

    def _make_label(self, text, **kwargs):
        attr = ' '.join(
            '{}="{}"'.format(*item) for item in kwargs.items()
        )
        fmt = '<span {attr}>{text}</span>'
        markup = fmt.format(attr=attr, text=text)
        label = gtk.Label()
        label.set_markup(markup)
        label.show()
        return label

    # Events
    def _delete_event(self, widget, event, data=None):
        return gtk.FALSE

    def _destroy(self, widget, data=None):
        gtk.mainquit()

    # Commands
    def _success_and_quit(self, cmd):
        dialogs.show_dialog(
            self.window,
            getattr(self.res, '{}_success_title'.format(cmd)),
            getattr(self.res, '{}_success_message'.format(cmd))
        )
        self._quit()

    def _install(self, widget, data=None):
        ret = commands.execute_command(self.resmodule, 'install', self.window)
        print('ret={}'.format(ret))
        if ret == 0:
            self._success_and_quit('install')

    def _uninstall(self, widget, data=None):
        ret = commands.execute_command(self.resmodule, 'uninstall', self.window)
        print('ret={}'.format(ret))
        if ret == 0:
            self._success_and_quit('install')

    def _quit(self, widget=None, data=None):
        self.window.destroy()


def main():
    res = os.environ['INSTALLER_RESOURCE_MODULE']
    Installer(res)
    gtk.mainloop()


if __name__ == '__main__':
    main()
