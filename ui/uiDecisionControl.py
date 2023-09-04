import tkinter as tk
import tkinter.ttk as ttk


class uiDecisionControl(ttk.Frame):
    def __init__(self, master, window_height, window_width):
        super(uiDecisionControl, self).__init__(master)
        self._is_running = False

        self.Frame_title = ttk.Frame(self)
        self.Frame_title.pack(fill="x", side="top")

        self.Label_Frame_Name = ttk.Label(self.Frame_title, text="决策控制")
        self.Label_Frame_Name.pack(side="left")

        self.Experiment_Frame = ttk.Labelframe(self, text="实验区")
        self.Experiment_Frame.pack(
            expand="true", fill="both", padx="4", pady="4", side="top"
        )

        self.pygame_frame_width = int(window_width * 0.8)
        self.pygame_frame_height = int(window_height * 0.95)

        self.Pygame_Frame = tk.Frame(
            self.Experiment_Frame,
            width=self.pygame_frame_width,
            height=self.pygame_frame_height,
        )

        self.Pygame_Frame.pack(side="left")

        self.Stat_Frame = ttk.LabelFrame(self.Experiment_Frame, text=" 统计信息 ")
        self.Stat_Frame.pack(fill="both", ipadx="2", padx="4", pady="4", side="top")

        self.stat_view = ttk.Treeview(self.Stat_Frame, height=20)
        _columns = ["轮次", "结果", "用时"]
        self.stat_view.configure(
            columns=_columns, displaycolumns=_columns, show="headings"
        )
        self.stat_view.column(
            _columns[0], anchor="w", stretch="true", width="60", minwidth="50"
        )
        self.stat_view.column(
            _columns[1], anchor="w", stretch="true", width="60", minwidth="50"
        )
        self.stat_view.column(
            _columns[2], anchor="w", stretch="true", width="30", minwidth="40"
        )
        self.stat_view.heading(_columns[0], anchor="w", text=_columns[0])
        self.stat_view.heading(_columns[1], anchor="w", text=_columns[1])
        self.stat_view.heading(_columns[2], anchor="w", text=_columns[2])

        sb = ttk.Scrollbar(self.Stat_Frame, orient="vertical")
        sb.pack(fill="y", pady="4", side="right")
        self.stat_view.config(yscrollcommand=sb.set)
        sb.config(command=self.stat_view.yview)
        self.stat_view.tag_configure("correct_row", foreground="green")
        self.stat_view.tag_configure("wrong_row", foreground="red")
        self.stat_view.pack(expand="true", fill="both", padx="4", pady="4", side="top")

        self.summary_status_text = tk.StringVar(value="等待实验开始")
        self.SummaryStatus = tk.Label(
            self.Experiment_Frame,
            textvariable=self.summary_status_text,
            bd=2,
            relief=tk.SUNKEN,
            anchor=tk.W,
            fg="blue",
        )
        self.SummaryStatus.pack(
            fill="x", ipadx="4", ipady="6", padx="6", pady="6", side="top"
        )

        self.Control_Frame = ttk.LabelFrame(self.Experiment_Frame, text=" 实验设置 ")
        self.Control_Frame.pack(fill="x", ipadx="2", padx="4", pady="4", side="top")

        self.round_text = ttk.Label(self.Control_Frame, text="实验轮次:")
        self.round_text.pack(fill="x", ipadx="2", padx="4", pady="4", side="left")
        self.round_number = tk.StringVar()
        self.rounds_chosen = ttk.Combobox(
            self.Control_Frame,
            width=12,
            textvariable=self.round_number,
            state="readonly",
        )
        self.rounds_chosen["values"] = list(range(1, 51))
        self.rounds_chosen.pack(fill="x", ipadx="2", padx="4", pady="4", side="top")
        self.rounds_chosen.current(0)

        self.ModelFrame = ttk.LabelFrame(self.Experiment_Frame, text=" 模型文件 ")
        self.EntryModelFile = ttk.Entry(self.ModelFrame)
        self.model_file = tk.StringVar(value="")
        self.EntryModelFile.configure(state="readonly", textvariable=self.model_file)
        self.EntryModelFile.pack(
            expand="true", fill="x", padx="4", pady="4", side="top"
        )

        self.ModelFileButton = ttk.Button(
            self.ModelFrame, text=("浏览"), command=self.get_model_file
        )
        self.ModelFileButton.pack(padx="4", pady="4", side="top")

        self.ModelFrame.pack(fill="x", ipadx="2", padx="4", pady="4", side="top")

        self.LoadModelFrame = ttk.LabelFrame(self.Experiment_Frame, text=" 模型状态 ")
        self.ModelInfoText = ttk.Label(self.LoadModelFrame)
        self.load_model_info = tk.StringVar(value="模型未加载")
        self.ModelInfoText.configure(textvariable=self.load_model_info)
        self.ModelInfoText.pack(expand="true", fill="x", padx="4", pady="4", side="top")

        self.LoadModelFileButton = ttk.Button(
            self.LoadModelFrame, text=("加载模型文件"), command=self.model_initialize
        )
        self.LoadModelFileButton.pack(padx="4", pady="4", side="top")
        self.LoadModelFrame.pack(fill="x", ipadx="2", padx="4", pady="4", side="top")

        self.Start_Button = ttk.Button(
            self.Experiment_Frame, text=("开始实验"), command=self.start_exp
        )
        self.Start_Button.pack(fill="x", ipadx="2", padx="4", pady="4", side="bottom")

    def _toggle_buttons(self):
        if self._is_running:
            state = "disabled"
        else:
            state = "normal"
        self.rounds_chosen["state"] = state
        self.Start_Button["state"] = state
        self.ModelFileButton["state"] = state
        self.LoadModelFileButton["state"] = state

    def start_exp(self):
        pass

    def get_model_file(self):
        pass

    def model_initialize(self):
        pass
