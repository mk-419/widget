#!/usr/bin/env python3
# Standard Lib
from datetime import datetime, tzinfo

# Third-Party Lib
import gi, cairo
from widjet import Widjet

gi.require_version("Gtk", "3.0")

from gi.repository import GLib, Gtk

class Main(Widjet):
    def __init__(self):
        super().__init__(500, 600)

        self.h = {}
        self.m = {}
        self.s = {}

        self.get_time()

        self.draw_jst = Gtk.DrawingArea()
        self.draw_jst.connect("draw", self.draw, "JST")
        self.draw_utc = Gtk.DrawingArea()
        self.draw_utc.connect("draw", self.draw, "UTC")
        
        GLib.timeout_add_seconds(1, self.update)

        vbox = Gtk.VBox()
        vbox.add(self.draw_jst)
        vbox.add(self.draw_utc)

        self.add(vbox)
    
    def draw(self, widget, ctx, tz):
        def box(ctx):
            ctx.move_to(0.1, 0.15)
            ctx.line_to(0.3, 0.15)
            ctx.line_to(0.35, 0.20)
            ctx.line_to(0.9, 0.20)
            ctx.line_to(0.9, 0.55)
            ctx.line_to(0.2, 0.55)
            ctx.line_to(0.13, 0.48)
            ctx.line_to(0.13, 0.28)
            ctx.line_to(0.1, 0.25)
            ctx.line_to(0.1, 0.15)

            ctx.close_path()

        def clock(ctx, column, target):
            ctx.set_font_size(font_size)
            ctx.set_source_rgb(1, 1, 0.785)
            x = font_size * (column + 1) + space * column

            ctx.select_font_face("Roboto Condensed")
            ctx.move_to(x, 0.41)
            ctx.show_text(target[0])

            ctx.set_font_size(font_size / 3)
            ctx.set_source_rgb(1, 0.8, 0.2)

            ctx.move_to(x + font_size * 5/ 4, 0.41 - font_size / 2)
            ctx.show_text(target[1])
            ctx.move_to(x  + font_size * 5/ 4, 0.41)
            ctx.select_font_face("Noto Serif CJK JP", cairo.FontSlant.NORMAL, cairo.FontWeight.BOLD)
            ctx.show_text(target[2])
            ctx.select_font_face("Roboto Condensed")
        
        font_size = 0.15
        space = 0.1

        ctx.scale(500, 500)
        ctx.set_line_width(0.01)
        
        ctx.select_font_face("Noto Serif CJK JP", cairo.FontSlant.NORMAL, cairo.FontWeight.BOLD)
        ctx.set_font_size(font_size /3)

        ctx.set_source_rgb(1, 0.8, 0.2)
        ctx.move_to(0.15, 0.09)

        ctx.show_text("日本標準時" if tz == "JST" else "世界標準時")
        ctx.stroke()
            
        ctx.set_source_rgb(1, 0.6, 0.2)
        ctx.move_to(0.1, 0.04)
        ctx.line_to(0.1, 0.12)
        ctx.move_to(0.45, 0.04)
        ctx.line_to(0.45, 0.12)

        ctx.stroke()

        box(ctx)
        ctx.set_source_rgba(0, 0, 0, 0.3)
        ctx.fill_preserve()
        ctx.set_source_rgb(1, 0.6, 0.2)
        ctx.stroke()

        ctx.select_font_face("Roboto Condensed")
        ctx.set_source_rgb(1, 0.8, 0.2)
        ctx.set_font_size(font_size / 3)
        ctx.move_to(0.13, 0.21)
        ctx.show_text("Live")

        h = str(self.h[tz]).zfill(2)
        m = str(self.m[tz]).zfill(2)
        s = str(self.s[tz]).zfill(2)

        clock(ctx, 0,  [f"{h}", "h", "時"])
        clock(ctx, 1, [f"{m}", "m", "分"])
        clock(ctx, 2, [f"{s}", "s", "秒"])

        ctx.stroke()
    
    def update(self):
        self.get_time()
        self.draw_jst.queue_draw()
        self.draw_utc.queue_draw()
        return True
    
    def get_time(self):
        now_jst = datetime.now()
        now_utc = datetime.utcnow()
        self.h["JST"] = now_jst.hour
        self.h["UTC"] = now_utc.hour
        self.m["JST"] = now_jst.minute
        self.m["UTC"] = now_utc.minute
        self.s["JST"] = now_jst.second
        self.s["UTC"] = now_utc.second

if __name__ == '__main__':
    win = Main()
    win.show_all()
    Gtk.main()
