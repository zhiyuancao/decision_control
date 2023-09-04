import pickle
import tkinter as tk
import tkinter.messagebox

from PIL import Image, ImageTk

from constants import APP_ICON, APP_NAME, BANNER_IMG


class LoginPage(tk.Tk):
    def __init__(self):
        super(LoginPage, self).__init__()

        self.window_initialize()
        self.interface_initialize()

    def window_initialize(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        if screen_height < 1080 or screen_width < 1920:
            tk.messagebox.showinfo(
                "错误", f"程序无法在小于1920x1080的分辨率下运行，您的屏幕分辨率为{screen_width}x{screen_height}。"
            )
            self.exit_all()
        self.window_width = screen_width // 3
        self.window_height = int(self.window_width * 0.7)
        left = (screen_width - self.window_width) // 2
        top = (screen_height - self.window_height) // 2

        self.wm_minsize(self.window_width, self.window_height)
        self.wm_resizable(True, True)
        self.wm_geometry(f"+{left}+{top}")
        self.title(APP_NAME)
        self.icon = tk.PhotoImage(file=APP_ICON)
        self.iconphoto(False, self.icon)

    def interface_initialize(self):
        # banner
        banner_image = Image.open(BANNER_IMG)
        banner_size = banner_image.size
        banner_size_new = (
            self.window_width,
            self.window_width * banner_size[1] // banner_size[0],
        )

        banner_image = banner_image.resize(banner_size_new, Image.Resampling.BILINEAR)
        self.canvas_baner = tk.Canvas(
            self,
            height=banner_size_new[1],
            width=banner_size_new[0],
        )
        self.banner_image_tk = ImageTk.PhotoImage(banner_image)
        self.canvas_baner.create_image(0, 0, anchor="nw", image=self.banner_image_tk)
        self.canvas_baner.pack()

        # username and password entries
        self.user_Frame = tk.LabelFrame(self, text="请登录")
        user_label = tk.Label(self.user_Frame, text="账号")
        user_label.grid(row=0, column=0, padx=20, pady=10)
        password_label = tk.Label(self.user_Frame, text="密码")
        password_label.grid(row=1, column=0, padx=20, pady=10)

        self.var_username = tk.StringVar()
        # self.var_username.set("admin")
        entry_username = tk.Entry(self.user_Frame, textvariable=self.var_username)
        entry_username.grid(row=0, column=1, padx=5, pady=5, ipadx=50)

        self.var_password = tk.StringVar()
        entry_password = tk.Entry(
            self.user_Frame, textvariable=self.var_password, show="*"
        )
        entry_password.grid(row=1, column=1, padx=5, pady=5, ipadx=50)
        self.user_Frame.pack(pady=20, ipadx=5, ipady=5)

        # login and sign up button
        self.button_Frame = tk.Frame(self)
        button_login = tk.Button(self.button_Frame, text="登录", command=self.user_login)
        button_login.grid(row=0, column=0, padx=20, pady=10, ipadx=30)

        button_sign_up = tk.Button(
            self.button_Frame, text="注册", command=self.user_sign_up
        )
        button_sign_up.grid(row=0, column=1, padx=20, pady=10, ipadx=30)

        # exit button
        button_exit = tk.Button(self.button_Frame, text="退出系统", command=self.exit_all)
        button_exit.grid(row=1, column=0, padx=20, pady=10, columnspan=2, ipadx=30)

        self.button_Frame.pack(pady=(0, 20))

        self.module_name = None

    def user_login(self):
        usr_name = self.var_username.get()
        usr_pwd = self.var_password.get()
        try:
            with open("usrs_info.pickle", "rb") as usr_file:
                usrs_info = pickle.load(usr_file)
        except FileNotFoundError:
            with open("usrs_info.pickle", "wb") as usr_file:
                usrs_info = {"admin": "admin"}
                pickle.dump(usrs_info, usr_file)
        if usr_name in usrs_info:
            if usr_pwd != usrs_info[usr_name]:
                tkinter.messagebox.showerror(title="错误", message="用户名或密码输入错误！")
            else:
                self.login_state = True
                self.user_Frame.pack_forget()
                self.button_Frame.pack_forget()
                self.module_select()
        else:
            tkinter.messagebox.showerror(title="错误", message="用户名或密码输入错误！")

    def user_sign_up(self):
        def check_user_profile():
            np = new_pwd.get()
            npf = new_pwd_confirm.get()
            nn = new_name.get()
            with open("usrs_info.pickle", "rb") as usr_file:
                exist_usr_info = pickle.load(usr_file)
            if np != npf:
                tk.messagebox.showerror("错误", "密码不一致!")
            elif nn in exist_usr_info:
                tk.messagebox.showerror("错误", "已经存在的用户名!")
            else:
                exist_usr_info[nn] = np
                with open("usrs_info.pickle", "wb") as usr_file:
                    pickle.dump(exist_usr_info, usr_file)
                tk.messagebox.showinfo("成功", "注册成功！")
                window_sign_up.destroy()

        window_sign_up = tk.Toplevel(self)
        window_sign_up.geometry("600x300")
        window_sign_up.title("用户注册")
        window_sign_up.iconphoto(False, self.icon)

        sign_up_Frame = tk.Frame(window_sign_up)

        user_label = tk.Label(sign_up_Frame, text="账号")
        user_label.grid(row=0, column=0, padx=20, pady=10)
        password_label = tk.Label(sign_up_Frame, text="密码")
        password_label.grid(row=1, column=0, padx=20, pady=10)
        confirm_label = tk.Label(sign_up_Frame, text="确认密码")
        confirm_label.grid(row=2, column=0, padx=20, pady=10)

        new_name = tk.StringVar()
        entry_username = tk.Entry(sign_up_Frame, textvariable=new_name)
        entry_username.grid(row=0, column=1, padx=(5, 20), pady=5, ipadx=50)
        new_pwd = tk.StringVar()
        entry_password = tk.Entry(sign_up_Frame, textvariable=new_pwd, show="*")
        entry_password.grid(row=1, column=1, padx=(5, 20), pady=5, ipadx=50)
        new_pwd_confirm = tk.StringVar()
        entry_usr_pwd_confirm = tk.Entry(
            sign_up_Frame, textvariable=new_pwd_confirm, show="*"
        )
        entry_usr_pwd_confirm.grid(row=2, column=1, padx=(5, 20), pady=5, ipadx=50)

        button_comfirm_sign_up = tk.Button(
            sign_up_Frame, text="注册", command=check_user_profile
        )
        button_comfirm_sign_up.grid(
            row=3, column=0, pady=(20, 10), ipadx=30, columnspan=2
        )
        sign_up_Frame.pack()

    def module_select(self):
        self.Module_Frame = tk.LabelFrame(self, text="模块选择")

        button_direction = tk.Button(
            self.Module_Frame, text="方向判断", command=self.run_direction_control
        )
        button_direction.grid(row=1, column=0, padx=20, pady=10, ipadx=30)

        button_decision = tk.Button(
            self.Module_Frame, text="决策控制", command=self.run_decision_control
        )
        button_decision.grid(row=1, column=1, padx=20, pady=10, ipadx=30)

        self.Module_Frame.pack(pady=(20, 20))

        # exit button
        button_exit = tk.Button(self, text="退出系统", command=self.exit_all)
        button_exit.pack(side="bottom", padx=20, pady=20, ipadx=30)

    def run_direction_control(self):
        self.module_name = "direction"
        self.destroy()

    def run_decision_control(self):
        self.module_name = "decision"
        self.destroy()

    def exit_all(self):
        self.quit()
        self.destroy()
        exit()

    def run(self):
        self.mainloop()
        return self.module_name
