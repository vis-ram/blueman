from gi.repository import Gtk
from gi.repository import Pango
from gi.repository import GObject


class MessageArea(Gtk.InfoBar):
    _inst_ = None

    def __new__(cls):
        if not MessageArea._inst_:
            MessageArea._inst_ = super(MessageArea, cls).__new__(cls)

        return MessageArea._inst_

    def __init__(self):
        GObject.GObject.__init__(self)

        self.text = ""

        self.set_app_paintable(True)

        self.setting_style = False

        self.icon = Gtk.Image()
        self.icon.props.xpad = 4
        self.label = Gtk.Label()
        self.label.props.xalign = 0
        self.label.set_ellipsize(Pango.EllipsizeMode.END)
        self.label.set_single_line_mode(True)
        self.label.set_selectable(True)

        self.b_more = self.add_button(_("More"), 0)
        im = Gtk.Image()
        im.set_from_icon_name("dialog-information", Gtk.IconSize.MENU)
        im.show()
        self.b_more.set_image(im)
        self.b_more.props.relief = Gtk.ReliefStyle.NONE

        self.set_show_close_button(True)

        self.get_content_area().add(self.icon)
        self.get_content_area().add(self.label)

        self.icon.show()
        self.label.show()

        self.connect("response", self.on_response)

    def on_response(self, info_bar, response_id):
        if response_id == 0:
            self.on_more()
        elif response_id == Gtk.ResponseType.CLOSE:
            self.on_close()

    def on_more(self):
        d = Gtk.MessageDialog(parent=None, flags=0, type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.CLOSE)

        d.props.text = self.text

        d.run()
        d.destroy()

    def on_close(self):
        self.props.visible = False

    @staticmethod
    def close():
        MessageArea._inst_.on_close()

    @staticmethod
    def show_message(*args):
        MessageArea._inst_._show_message(*args)

    def _show_message(self, text, icon="dialog-warning"):
        self.text = text

        self.label.set_tooltip_text(text)
        self.icon.set_from_icon_name(icon, Gtk.IconSize.MENU)

        if icon == "dialog-warning":
            self.set_message_type(Gtk.MessageType.ERROR)
        else:
            self.set_message_type(Gtk.MessageType.INFO)

        if not self.props.visible:
            self.show()

        lines = text.split("\n")
        if len(lines) > 1:
            self.label.props.label = lines[0] + "..."
            self.b_more.props.visible = True
        else:
            self.label.props.label = text
            self.b_more.props.visible = False
