import socket
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk

from app.DecisionControl import DecisionControl
from app.DirectionControl import DirectionControl
from constants import EEG_RECEPTION_DURATION, HOST, PORT


class MainFrame(ttk.Frame):
    def __init__(self, window_height, window_width, master, module_name):
        super(MainFrame, self).__init__(master)
        s = ttk.Style()
        s.configure("Treeview", rowheight=window_width // 75)

        self.FrameOperateButtons = ttk.Labelframe(self)

        self.Stop_Button = ttk.Button(
            self.FrameOperateButtons, text=("退出系统"), command=self.master.exit
        )
        self.Stop_Button.pack(fill="x", ipadx="2", padx="4", pady="4", side="bottom")

        self.FrameOperateButtons.configure(height="200", text="模块", width="200")
        self.FrameOperateButtons.pack(fill="y", padx="4", pady="4", side="left")
        if module_name == "direction":
            self.module_selected = DirectionControl(
                master=self, window_height=window_height, window_width=window_width
            )
        elif module_name == "decision":
            self.module_selected = DecisionControl(
                master=self, window_height=window_height, window_width=window_width
            )
        self.module_selected.pack(side="top", expand=True, fill="both")

        self.DeviceFrame = ttk.LabelFrame(self.FrameOperateButtons, text=" 设备配置 ")
        self.DeviceFrame.pack(fill="x", ipadx="2", padx="4", pady="4", side="top")

        self.device_status_text = tk.StringVar(value="设备未连接")
        self.DeviceStatus = tk.Label(
            self.DeviceFrame,
            textvariable=self.device_status_text,
            bd=2,
            relief=tk.SUNKEN,
            fg="red",
        )
        self.DeviceStatus.pack(
            fill="x", ipadx="2", ipady="2", padx="2", pady="2", side="top"
        )

        self.ConnectDeviceButton = ttk.Button(
            self.DeviceFrame, text=("连接设备"), command=self.connect_device
        )
        self.ConnectDeviceButton.pack(
            fill="x", ipadx="2", padx="4", pady="4", side="top"
        )

        self.DisconnectDeviceButton = ttk.Button(
            self.DeviceFrame, text=("断开连接"), command=self.disconnect_device
        )
        self.DisconnectDeviceButton["state"] = "disabled"
        self.DisconnectDeviceButton.pack(
            fill="x", ipadx="2", padx="4", pady="4", side="top"
        )

        self.device_connected = False
        self.start_receive_data = False
        self.eeg_raw_data = ""
        self.start_receive_time = None

    def receive_data(self):
        while not self.master.interrupt and self.device_connected:
            buffer = self.connection.recv(29 * 1000)
            if self.start_receive_data:
                self.eeg_raw_data += buffer.hex()
                if (
                    time.time() * 1000 - self.start_receive_time
                    > EEG_RECEPTION_DURATION
                ):
                    self.start_receive_data = False

    def connect_device(self):
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sk.bind((HOST, PORT))
            self.sk.listen(5)
            self.connection, _ = self.sk.accept()
            self.device_connected = True
            self.T = threading.Thread(target=self.receive_data)
            self.T.start()
            tk.messagebox.showinfo("成功", "设备连接成功！")
            self.master.status_bar_text.set("设备已连接")
            self.DeviceStatus.configure(fg="green")
            self.device_status_text.set("设备已连接")
            self.ConnectDeviceButton["state"] = "disabled"
            self.DisconnectDeviceButton["state"] = "normal"

        except Exception as e:
            self.sk.close()
            tk.messagebox.showinfo("错误", "设备连接错误。错误信息：" + str(e))

    def disconnect_device(self):
        try:
            self.device_connected = False
            self.sk.close()
            self.T.join()
            tk.messagebox.showinfo("信息", "设备已断开！")
            self.ConnectDeviceButton["state"] = "normal"
            self.DisconnectDeviceButton["state"] = "disabled"
            self.DeviceStatus.configure(fg="red")
            self.device_status_text.set("设备未连接")

        except AttributeError:
            tk.messagebox.showinfo("错误", "设备未连接！")
