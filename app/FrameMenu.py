import tkinter as tk
import tkinter.ttk as ttk

from app.About import About


class FrameMenu(tk.Menu):
    def __init__(self, master=None, **kw):
        super(FrameMenu, self).__init__(master, **kw)
        self._style = ttk.Style(self.master)
        self.theme = tk.StringVar(value=self._style.theme_use())

        self.MenuFile = tk.Menu(self, tearoff=False)
        self.MenuFile.add_command(label="退出", command=self.master.exit)
        self.add_cascade(label="文件", menu=self.MenuFile)

        self.MenuTheme = tk.Menu(self, tearoff=False)
        for theme in self._style.theme_names():
            self.MenuTheme.add_radiobutton(
                label=theme, command=self._set_theme, value=theme, variable=self.theme
            )
        self.add_cascade(label="主题", menu=self.MenuTheme)

        self.MenuHelp = tk.Menu(self, tearoff=False)
        self.MenuHelp.add_command(label="关于", command=self.about)
        self.add_cascade(label="帮助", menu=self.MenuHelp)

    def about(self):
        about_frame = About(None)
        self.wait_window(about_frame)

    def _set_theme(self):
        self._style.theme_use(self.theme.get())
