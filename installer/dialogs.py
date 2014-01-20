# -*- coding: utf-8 -*-

from pkg_resources import resource_filename
from functools import wraps

import gtk


def show_dialog(parent, title, message):
    dialog = gtk.MessageDialog(
        parent,
        gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_MODAL,
        gtk.MESSAGE_INFO,
        gtk.BUTTONS_OK,
        message
    )
    resp = dialog.run()
    dialog.destroy()
    return resp


class Loader(gtk.VBox):
    def __init__(self, *args, **kwargs):
        super(Loader, self).__init__(*args, **kwargs)
        self.label = gtk.Label()
        self.label.show()
        self.pack_start(self.label)

        image = resource_filename('installer_res', 'images/loader.gif')
        loader = gtk.Image()
        loader.set_from_file(image)
        loader.show()
        self.pack_start(loader)

    def set_markup(self, *args, **kwargs):
        self.label.set_markup(*args, **kwargs)


def make_password_entry():
    entry = gtk.Entry()
    entry.set_visibility(False)
    entry.set_invisible_char('*')
    return entry


# Original idea: http://is.gd/LiksfD
class PasswordDialog(gtk.MessageDialog):

    # Callbacks
    _cancel_cb = None
    _ok_cb = None

    def __init__(self,
                 parent=None,
                 flags=(gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_MODAL),
                 type=gtk.MESSAGE_QUESTION,
                 buttons=0, # gtk.BUTTONS_OK_CANCEL,
                 message_format='Please enter your password',
                 title='Password',
                 checkboxes=None):
        super(PasswordDialog, self).__init__(
            parent, flags, type, buttons, message_format
        )

        self.sensitive = []

        # Set title
        if title is not None:
            self.set_title(title)
            self.set_markup('<b>{}</b>'.format(title))

        # Set message
        if message_format is not None:
            self.format_secondary_markup(message_format)

        area = self.get_content_area()

        self.cbs = {}
        for key, (label, active) in checkboxes.items():
            self.cbs[key] = gtk.CheckButton(label)
            self.cbs[key].set_active(active)
            self.cbs[key].show()
            area.pack_start(self.cbs[key])


        # Add password text entry widget
        self.entry = make_password_entry()
        self.entry.connect('key-press-event', self._on_key)
        self.sensitive.append(self.entry)
        self.entry.show()
        area.pack_start(self.entry)

        # Add loader widget
        self.loader = Loader()
        area.pack_start(self.loader)

        # Add feedback widget
        self.feedback = gtk.Label()
        area.pack_start(self.feedback)

        # Add OK and cancel buttons
        ok = gtk.Button(stock=gtk.STOCK_OK)
        ok.connect('clicked', self._on_ok)
        self.sensitive.append(ok)

        cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        cancel.connect('clicked', self._on_cancel)
        self.sensitive.append(cancel)

        # Pack buttons and show
        hbox = gtk.HBox()
        hbox.add(ok)
        hbox.add(cancel)
        hbox.show_all()
        area.pack_end(hbox)

    def _cb_decorator(self, cb):
        @wraps(cb)
        def wrapper(*args, **kwargs):
            code = cb(*args, **kwargs)
            return code
        return wrapper

    @property
    def cancel_cb(self):
        return self._cancel_cb

    @cancel_cb.setter
    def cancel_cb(self, cb):
        self._cancel_cb = self._cb_decorator(cb)

    @property
    def ok_cb(self):
        return self._ok_cb

    @ok_cb.setter
    def ok_cb(self, cb):
        self._ok_cb = self._cb_decorator(cb)

    def _on_ok(self, _=None):
        if self._ok_cb is not None:
            return self._ok_cb()
        else:
            self.response(gtk.RESPONSE_OK)

    def _on_cancel(self, _=None):
        if self._cancel_cb is not None:
            return self._cancel_cb()
        else:
            self.response(gtk.RESPONSE_CANCEL)

    def show_feedback(self, text, style='default'):
        """The `style` argument may be one of the following strings: default,
        info, success, warning, error.

        """
        self.hide_all()
        color = lambda s: 'color="{}"'.format(s)
        markup = '<span {}>{}</span>'.format(
            color('blue') if style == 'info' else
            color('green') if style == 'success' else
            color('orange') if style == 'warning' else
            color('red') if style == 'error' else
            '',
            text
        )
        self.feedback.set_markup(markup)
        self.feedback.show()

    def hide_feedback(self):
        self.feedback.set_markup('<span>Nothing to look here. ;)</span>')
        self.feedback.hide()

    def show_loader(self, text):
        self.hide_all()
        [w.set_sensitive(False) for w in self.sensitive]
        self.loader.set_markup(text)
        self.loader.show_all()

    def hide_loader(self):
        [w.set_sensitive(True) for w in self.sensitive]
        self.loader.hide_all()

    def hide_all(self):
        self.hide_feedback()
        self.hide_loader()

    def get_password(self):
        return self.entry.get_text()

    def get_checkboxes(self):
        return {k: v.get_active() for (k, v) in self.cbs.items()}

    def _on_key(self, widget, event):
        name = gtk.gdk.keyval_name(event.keyval)
        if name.lower() in ('kp_enter', 'return'):
            self._on_ok()
