import os
import random
import time
import tkinter as tk
from tkinter.filedialog import askopenfilename

import numpy as np
import pygame
import torch

from app.Component import Arrow, Football, Goal
from constants import (
    BAND_FILTER,
    DIRECTION_CONTROL_CATEGORY,
    EEG_INPUT_DURATION,
    FILE_TYPES_MODEL,
    FRAME_UPDATE_INTERVAL,
    GRASS_IMG,
    HIGH_FREQ,
    LOW_FREQ,
    RESULT_DISPLAY_TIME,
    SAMPLING_FREQ,
    STIMULATE_DISPLAY_TIME,
    GoalType,
)
from data.Model import SINCEEGNet
from ui.uiDirectionControl import uiDirectionControl
from utils import band_filter, eeg_data_convert


class DirectionControl(uiDirectionControl):
    def __init__(self, master, window_height, window_width):
        super(DirectionControl, self).__init__(master, window_height, window_width)
        self.master = master
        self.category = np.array(DIRECTION_CONTROL_CATEGORY)

        # embed pygame window
        os.environ["SDL_WINDOWID"] = str(self.Pygame_Frame.winfo_id())
        os.environ["SDL_VIDEODRIVER"] = "windib"

        self.update_idletasks()

        pygame.init()
        self.pygame_surface = pygame.display.set_mode(
            (self.pygame_frame_width, self.pygame_frame_height)
        )

        self.grass = pygame.image.load(GRASS_IMG)
        self.grass = pygame.transform.scale(
            self.grass, (self.pygame_frame_width, self.pygame_frame_height)
        )

        goal_height = self.pygame_frame_height // 4
        goal_width = int(goal_height * 1.5)
        goal_size = (goal_width, goal_height)

        goal_left_center = (goal_width // 2, self.pygame_frame_height // 2)
        goal_right_center = (
            self.pygame_frame_width - goal_width // 2,
            self.pygame_frame_height // 2,
        )
        goal_top_center = (self.pygame_frame_width // 2, goal_height // 2)
        goal_bottom_center = (
            self.pygame_frame_width // 2,
            self.pygame_frame_height - goal_height // 2,
        )

        self.goal_left = Goal(GoalType.LEFT, goal_left_center, goal_size)
        self.goal_right = Goal(GoalType.RIGHT, goal_right_center, goal_size)
        self.goal_top = Goal(GoalType.TOP, goal_top_center, goal_size)
        self.goal_bottom = Goal(GoalType.BOTTOM, goal_bottom_center, goal_size)

        arrow_height = self.pygame_frame_height // 8
        arrow_width = int(arrow_height * 1.5)
        arrow_size = (arrow_width, arrow_height)

        self.arrow = Arrow(
            frame_width=self.pygame_frame_width,
            frame_height=self.pygame_frame_height,
            arrow_size=arrow_size,
        )

        football_size = (self.pygame_frame_height // 10, self.pygame_frame_height // 10)
        football_start_pos = (
            self.pygame_frame_width // 2,
            self.pygame_frame_height // 100 * 55,
        )
        self.football = Football(
            football_start_pos,
            football_size,
            frame_width=self.pygame_frame_width,
            frame_height=self.pygame_frame_height,
            goal_size=goal_size,
        )
        self.football.reset(self.pygame_surface)

        self.football_move = True
        self.trail_index = 0
        self.correct_trial = 0
        self.model_load_success = False
        self.master.start_receive_data = False
        self.master.device_connected = False
        self.interface_initialize()

    def model_initialize(self):
        try:
            self.model = SINCEEGNet(num_class=4)
            load_info = self.model.load_state_dict(self.state_dict)
            self.model = self.model.eval()
            self.model(
                torch.rand(1, 8, int(EEG_INPUT_DURATION * SAMPLING_FREQ // 1000))
            )  # for fast inference

            self.load_model_info.set(str(load_info))
            self.model_load_success = True
        except Exception as e:
            self.model_load_success = False
            self.load_model_info.set(str(e))

    def draw_background(self):
        self.pygame_surface.blit(self.grass, [0, 0])
        self.goal_left.draw_white(self.pygame_surface)
        self.goal_right.draw_white(self.pygame_surface)
        self.goal_top.draw_white(self.pygame_surface)
        self.goal_bottom.draw_white(self.pygame_surface)

    def interface_initialize(self):
        self.draw_background()

        if not self._is_running:
            self.Pygame_Frame.after(FRAME_UPDATE_INTERVAL, self.interface_initialize)
        pygame.display.update()

    def start_exp(self):
        if self.check_model():
            self.trail_index = 0
            self.correct_trial = 0
            self.stat_view.delete(*self.stat_view.get_children())
            self.trial_rounds = int(self.rounds_chosen.get())
            # self.label_sequence = [
            #     random.choice(DIRECTION_CONTROL_CATEGORY)
            #     for _ in range(self.trial_rounds)
            # ]
            self.label_sequence = []
            category_copy = DIRECTION_CONTROL_CATEGORY.copy()
            label_repeat = self.trial_rounds // len(DIRECTION_CONTROL_CATEGORY)
            for _ in range(label_repeat):
                random.shuffle(category_copy)
                self.label_sequence = self.label_sequence + category_copy
            if len(self.label_sequence) < self.trial_rounds:
                [
                    self.label_sequence.append(
                        random.choice(DIRECTION_CONTROL_CATEGORY)
                    )
                    for _ in range(self.trial_rounds - len(self.label_sequence))
                ]
        self.do_single_trail()

    def do_single_trail(self):
        if self.trail_index < self.trial_rounds:
            self.summary_status_text.set(
                f"正在进行第{self.trail_index+1}/{self.trial_rounds}轮实验。"
            )
            self._is_running = True
            self.trial_start_time = time.time() * 1000
            self.master.master.status_bar_text.set("正在呈现刺激")
            self.gt_direction = self.label_sequence[self.trail_index]
            self.stimulate()
        else:
            self._is_running = False
            self.summary_status_text.set(
                f"实验结束，正确率为{self.correct_trial / self.trial_rounds * 100:.1f}%。"
            )
            self.interface_initialize()

        self._toggle_buttons()

    def stimulate(self):
        self.arrow.draw(self.pygame_surface, direction=self.gt_direction)
        self.football.draw(self.pygame_surface)
        pygame.display.update()

        if time.time() * 1000 - self.trial_start_time < STIMULATE_DISPLAY_TIME:
            self.Pygame_Frame.after(FRAME_UPDATE_INTERVAL, self.stimulate)
        else:
            self.draw_background()
            self.master.eeg_raw_data = ""
            self.master.start_receive_time = time.time() * 1000
            self.master.start_receive_data = True
            while True:
                if not self.master.start_receive_data:
                    self.model_inference()
                    break

    def model_inference(self):
        self.football_move = True

        eeg_data_len = int(EEG_INPUT_DURATION // 1000 * SAMPLING_FREQ)
        input_data = eeg_data_convert(self.master.eeg_raw_data, eeg_data_len)
        input_data = input_data[None, ...]
        if BAND_FILTER:
            input_data = band_filter(input_data, low_freq=LOW_FREQ, high_freq=HIGH_FREQ)

        logit = self.model(torch.FloatTensor(input_data.copy()))
        predict_label = logit.argmax().numpy()

        self.pred_direction = self.category[predict_label]
        self.master.master.status_bar_text.set("解码完毕")

        self.predict_end_time = time.time() * 1000

        self.update_stat()
        self.display_football_animation()

    def update_stat(self):
        time_past = self.predict_end_time - self.master.start_receive_time
        if self.pred_direction == self.gt_direction:
            result_text = "正确"
            self.correct_trial += 1
            self.stat_view.insert(
                parent="",
                index=self.trail_index + 1,
                iid=self.trail_index + 1,
                text="",
                values=(
                    f"第{self.trail_index+1}/{self.trial_rounds}轮",
                    f"{result_text}",
                    f"{time_past/1000:.2f}s",
                ),
                tags="correct_row",
            )
        else:
            result_text = "错误"
            self.stat_view.insert(
                parent="",
                index=self.trail_index + 1,
                iid=self.trail_index + 1,
                text="",
                values=(
                    f"第{self.trail_index+1}/{self.trial_rounds}轮",
                    f"{result_text}",
                    f"{time_past/1000:.2f}s",
                ),
                tags="wrong_row",
            )

    def display_result(self):
        if time.time() * 1000 - self.football_end_time < RESULT_DISPLAY_TIME:
            self.draw_background()
            if self.gt_direction == self.pred_direction:
                if self.gt_direction == "up":
                    self.goal_top.draw_green(self.pygame_surface)
                if self.gt_direction == "down":
                    self.goal_bottom.draw_green(self.pygame_surface)
                if self.gt_direction == "left":
                    self.goal_left.draw_green(self.pygame_surface)
                if self.gt_direction == "right":
                    self.goal_right.draw_green(self.pygame_surface)
            else:
                if self.pred_direction == "up":
                    self.goal_top.draw_red(self.pygame_surface)
                if self.pred_direction == "down":
                    self.goal_bottom.draw_red(self.pygame_surface)
                if self.pred_direction == "left":
                    self.goal_left.draw_red(self.pygame_surface)
                if self.pred_direction == "right":
                    self.goal_right.draw_red(self.pygame_surface)
            pygame.display.update()
            self.Pygame_Frame.after(FRAME_UPDATE_INTERVAL, self.display_result)
        else:
            # next trial
            self.trial_start_time = time.time() * 1000
            self.draw_background()
            self.football.reset(self.pygame_surface)
            self.trail_index += 1
            self.do_single_trail()

    def display_football_animation(self):
        self.draw_background()
        self.arrow.draw(self.pygame_surface, direction=self.gt_direction)

        if not self.football._done_moving:
            self.football.move(direction=self.pred_direction)
            self.football.draw(self.pygame_surface)
            pygame.display.update()
            self.Pygame_Frame.after(
                FRAME_UPDATE_INTERVAL, self.display_football_animation
            )
        else:
            self.football._done_moving = False
            self.football_end_time = time.time() * 1000
            self.display_result()

    def get_model_file(self):
        model_file = askopenfilename(title="选择模型文件", filetypes=FILE_TYPES_MODEL)
        if model_file:
            self.model_file.set(model_file)
            self.state_dict = torch.load(model_file, map_location=torch.device("cpu"))

    def check_model(self):
        if not self.model_load_success:
            tk.messagebox.showinfo("错误", "模型参数未正确加载！")
            return False
        if not self.master.device_connected:
            tk.messagebox.showinfo("错误", "采集设备未正确连接！")
            return False

        return True
