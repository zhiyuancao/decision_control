import tkinter as tk
import tkinter.ttk as ttk

from constants import APP_NAME, APP_VERSION


class UiAbout(tk.Toplevel):
    def __init__(self, master=None, **kw):
        super(UiAbout, self).__init__(master, **kw)
        self.FrameAbout = ttk.Frame(self)
        self.LabelAppName = ttk.Label(self.FrameAbout)
        self.app_name = tk.StringVar(value=APP_NAME)
        self.LabelAppName.configure(
            font="{Arial} 36 {bold}", text=APP_NAME, textvariable=self.app_name
        )
        self.LabelAppName.pack(padx="60", pady="40", side="top")
        self.LabelAppVersion = ttk.Label(self.FrameAbout)
        self.app_version = tk.StringVar(value=APP_VERSION)
        self.LabelAppVersion.configure(
            font="{Arial} 14 {bold}", text=APP_VERSION, textvariable=self.app_version
        )
        self.LabelAppVersion.pack(side="top")
        self.LabelAuthorInfo = ttk.Label(self.FrameAbout)
        self.author_info = tk.StringVar(value="技术支持：caozhiyuan@mail.bnu.edu.cn")
        self.LabelAuthorInfo.configure(
            font="{Arial} 14 {bold}", text="", textvariable=self.author_info
        )
        self.LabelAuthorInfo.pack(side="top")
        self.ButtonOK = ttk.Button(self.FrameAbout)
        self.ButtonOK.configure(text="OK")
        self.ButtonOK.pack(ipadx="2", pady="30", side="top")
        self.ButtonOK.configure(command=self.close_about)
        self.FrameAbout.configure(height="200", width="200")
        self.FrameAbout.pack(side="top")

    def close_about(self):
        pass
