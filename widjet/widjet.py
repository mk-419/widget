# Third-Party Lib
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")

from gi.repository import Gdk, Gtk

class Widjet(Gtk.Window):
    def __init__(
        self,
        width: int =100,
        height: int =100
    ):
        # Create window
        super().__init__()

        # Make transparent
        self.set_app_paintable(True)
        self.set_visual(self.get_screen().get_rgba_visual())

        # Set size
        self.set_default_size(width, height)

        # Fix to desktop
        self.set_keep_below(True)
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)

        # Move upper right
        monitor = self.get_display().get_primary_monitor()
        x = monitor.get_geometry().width * monitor.get_scale_factor()
        self.move(x - width, 0)

        # Define
        self.drag =  False
        self.free = True

        # Get event
        self.connect("button-press-event", self.on_clicked)
        self.connect("motion-notify-event", self.on_moved)
        self.connect("button-release-event", self.on_released)

        # Create menu
        self.menu = Gtk.Menu()

        # Create menu item
        end = Gtk.MenuItem().new_with_label("終了")
        end.connect("activate", Gtk.main_quit)
        fix = Gtk.CheckMenuItem().new_with_label("固定")
        fix.connect("toggled", self.on_toggled)

        # Add menu item
        self.menu.add(end)
        self.menu.add(fix)
    
    def on_clicked(self, widget, event):
        # Get  left click
        if event.button == 1 and self.free:
            self.drag = True
            self.x_click = event.x
            self.y_click = event.y
        # Get  right click
        elif event.button == 3:
            self.menu.show_all()
            self.menu.popup_at_pointer()

    def on_released(self, widget, event):
        self.drag =  False
    
    def on_moved(self, widget, event):
        if self.drag:
            self.move(int(event.x_root - self.x_click), int(event.y_root - self.y_click))
    
    def on_toggled(self, widget):
        self.free = not widget.get_active()