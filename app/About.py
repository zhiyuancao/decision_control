import tkinter as tk

from constants import APP_ICON, APP_NAME, APP_VERSION
from ui.uiAbout import UiAbout


class About(UiAbout):
    def __init__(self, master, **kw):
        super(About, self).__init__(master, **kw)

        self._center()

        self.app_name.set(APP_NAME)
        self.app_version.set(APP_VERSION)
        self.iconphoto(False, tk.PhotoImage(file=APP_ICON))

        self.ButtonOK.focus_set()
        self.grab_set()

    def _center(self):
        self.update_idletasks()
        width, height = self.winfo_width(), self.winfo_height()
        screen_width, screen_height = (
            self.winfo_screenwidth(),
            self.winfo_screenheight() * 3 // 5,
        )
        left = (screen_width - width) // 2
        top = (screen_height - height) // 2
        self.wm_geometry(f"+{left}+{top}")

    def close_about(self):
        self.destroy()
