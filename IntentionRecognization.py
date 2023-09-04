import os
import platform
import tkinter as tk

from app.FrameMenu import FrameMenu
from app.Login import LoginPage
from app.MainFrame import MainFrame
from constants import APP_ICON, APP_NAME


class IntentionRecognization(tk.Tk):
    def __init__(self, module_name):
        super(IntentionRecognization, self).__init__(module_name)

        self._center()

        self.FrameMenu = FrameMenu(self)
        self.configure(menu=self.FrameMenu)

        self.MainFrame = MainFrame(
            master=self,
            window_height=self.window_height,
            window_width=self.window_width,
            module_name=module_name,
        )
        self.MainFrame.pack(expand=True, fill="both")

        self.status_bar_text = tk.StringVar(value="等待指令")
        self.statusbar = tk.Label(
            self, textvariable=self.status_bar_text, bd=1, relief=tk.SUNKEN, anchor=tk.W
        )
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.title(APP_NAME)
        self.iconphoto(False, tk.PhotoImage(file=APP_ICON))

        self.interrupt = False

    def _center(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.window_width = int(screen_width * 0.9)
        self.window_height = int(screen_height * 0.8)
        left = (screen_width - self.window_height) // 2
        self.wm_minsize(self.window_width, self.window_height)
        self.wm_resizable(True, True)
        self.wm_geometry(f"+{left}+{10}")

    def run(self):
        self.mainloop()

    def exit(self):
        self.interrupt = True
        self.quit()
        self.destroy()
        exit()


if __name__ == "__main__":
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
    if platform.system() == "Windows" and int(platform.version().split(".")[0]) >= 10:
        import ctypes

        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    login_page = LoginPage()
    module_name = login_page.run()

    if module_name:
        IntentionRecognization(module_name).run()
