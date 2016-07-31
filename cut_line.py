from gi.repository import GObject, Gio, Gtk, Gedit, Gdk

import os

class CutLineWindowActivatable(GObject.Object, Gedit.WindowActivatable):

	window = GObject.property(type=Gedit.Window)

	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		self.handler_id = self.window.connect('key-press-event', self.on_key_press)

	def do_deactivate(self):
		self.window.disconnect(self.handler_id)

	def on_key_press(self, term, event):
		modifiers = event.state & Gtk.accelerator_get_default_mod_mask()

		if event.keyval in (Gdk.KEY_X, Gdk.KEY_x):
			if modifiers == Gdk.ModifierType.CONTROL_MASK:
				self.on_cut_line_key_press(self)

		return False

	def on_cut_line_key_press(self, action=None, user_data=None):
		doc = self.window.get_active_document()
		selection_iter = doc.get_selection_bounds()

		if len(selection_iter) == 0:
			view = self.window.get_active_view()
			itstart = doc.get_iter_at_mark(doc.get_insert())
			offset = itstart.get_line_offset()
			itstart.set_line_offset(0)
			itend = doc.get_iter_at_mark(doc.get_insert())
			itend.forward_line()
			doc.begin_user_action()
			doc.select_range(itstart, itend)
			view.cut_clipboard()
			itstart = doc.get_iter_at_mark(doc.get_insert())
			itstart.set_line_offset(offset)
			doc.end_user_action()
			doc.place_cursor(itstart)
