import os

APP_NAME = "单人意图识别系统"
APP_VERSION = "0.1-BETA"

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
APP_ICON = os.path.join(BASE_DIR, "imgs/icon.png")
BANNER_IMG = os.path.join(BASE_DIR, "imgs/banner.jpg")
GRASS_IMG = os.path.join(BASE_DIR, "imgs/grass.png")
ARROW_IMG = os.path.join(BASE_DIR, "imgs/arrow.png")
FOOTBALL_IMG = os.path.join(BASE_DIR, "imgs/football.png")
SKY_IMG = os.path.join(BASE_DIR, "imgs/sky.png")
BALLOON_IMG = os.path.join(BASE_DIR, "imgs/balloon.png")
BALLOON_CORRECT_IMG = os.path.join(BASE_DIR, "imgs/balloon_correct.png")
BALLOON_WRONG_IMG = os.path.join(BASE_DIR, "imgs/balloon_wrong.png")
STIMULI_GO_IMG = os.path.join(BASE_DIR, "imgs/stimuli_go.png")
STIMULI_STOP_IMG = os.path.join(BASE_DIR, "imgs/stimuli_stop.png")


DIRECTION_CONTROL_CATEGORY = ["left", "right", "up", "down"]
DECISION_CONTROL_CATEGORY = ["go", "stop"]
FILE_TYPES_MODEL = [("PyTorch模型参数文件", "*.pkl")]

FRAME_UPDATE_INTERVAL = 10
STIMULATE_DISPLAY_TIME = 1000
RESULT_DISPLAY_TIME = 1000
EEG_RECEPTION_DURATION = 2600
EEG_INPUT_DURATION = 2000
SAMPLING_FREQ = 2000

BAND_FILTER = True
LOW_FREQ = 0.5
HIGH_FREQ = 100

HOST = "127.0.0.1"
PORT = 9687


class GoalType:
    class TOP:
        WHITE = 0
        GREEN = 1
        RED = 2

    class BOTTOM:
        WHITE = 3
        GREEN = 4
        RED = 5

    class LEFT:
        WHITE = 6
        GREEN = 7
        RED = 8

    class RIGHT:
        WHITE = 9
        GREEN = 10
        RED = 11


GoalRes = {
    GoalType.TOP.WHITE: os.path.join(BASE_DIR, "imgs/goal_top_white.png"),
    GoalType.TOP.GREEN: os.path.join(BASE_DIR, "imgs/goal_top_green.png"),
    GoalType.TOP.RED: os.path.join(BASE_DIR, "imgs/goal_top_red.png"),
    GoalType.BOTTOM.WHITE: os.path.join(BASE_DIR, "imgs/goal_bottom_white.png"),
    GoalType.BOTTOM.GREEN: os.path.join(BASE_DIR, "imgs/goal_bottom_green.png"),
    GoalType.BOTTOM.RED: os.path.join(BASE_DIR, "imgs/goal_bottom_red.png"),
    GoalType.LEFT.WHITE: os.path.join(BASE_DIR, "imgs/goal_left_white.png"),
    GoalType.LEFT.GREEN: os.path.join(BASE_DIR, "imgs/goal_left_green.png"),
    GoalType.LEFT.RED: os.path.join(BASE_DIR, "imgs/goal_left_red.png"),
    GoalType.RIGHT.WHITE: os.path.join(BASE_DIR, "imgs/goal_right_white.png"),
    GoalType.RIGHT.GREEN: os.path.join(BASE_DIR, "imgs/goal_right_green.png"),
    GoalType.RIGHT.RED: os.path.join(BASE_DIR, "imgs/goal_right_red.png"),
}
