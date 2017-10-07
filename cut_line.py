import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gedit', '3.0')

from gi.repository import GObject, Gdk, Gtk, Gedit


class CutLineWindowActivatable(GObject.Object, Gedit.WindowActivatable):

  window = GObject.property(type=Gedit.Window)

  def __init__(self):
    GObject.Object.__init__(self)

    self._handler_id = None

  def do_activate(self):
    self._handler_id = self.window.connect('key-press-event', self.on_key_press)

  def do_deactivate(self):
    self.window.disconnect(self._handler_id)

  def on_key_press(self, term, event):
    if event.keyval in (Gdk.KEY_X, Gdk.KEY_x):
      modifiers = event.state & Gtk.accelerator_get_default_mod_mask()

      if modifiers == Gdk.ModifierType.CONTROL_MASK:
        self.cut_line()

    return False

  def cut_line(self):
    doc    = self.window.get_active_document()
    bounds = doc.get_selection_bounds()

    if len(bounds) == 0:
      itstart = doc.get_iter_at_mark(doc.get_insert())
      loffset = itstart.get_line_offset()
      itstart.set_line_offset(0)

      itend = doc.get_iter_at_mark(doc.get_insert())
      itend.forward_line()

      doc.begin_user_action()
      doc.select_range(itstart, itend)

      view = self.window.get_active_view()
      view.cut_clipboard()

      itstart = doc.get_iter_at_mark(doc.get_insert())
      itstart.set_line_offset(loffset)

      doc.end_user_action()
      doc.place_cursor(itstart)
