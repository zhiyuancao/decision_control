import pygame

from constants import (
    ARROW_IMG,
    BALLOON_CORRECT_IMG,
    BALLOON_IMG,
    BALLOON_WRONG_IMG,
    FOOTBALL_IMG,
    GoalRes,
)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, frame_width, frame_height, arrow_size):
        super().__init__()
        self.arrow_image = pygame.image.load(ARROW_IMG)
        self.arrow_image = pygame.transform.scale(self.arrow_image, arrow_size)

        self.rect = self.arrow_image.get_rect()
        self.left = (int(frame_width / 3), int(frame_height / 100 * 55))
        self.right = (int(frame_width / 3 * 2), int(frame_height / 100 * 55))
        self.top = (int(frame_width / 100 * 52), int(frame_height / 10 * 3))
        self.bottom = (int(frame_width / 100 * 52), int(frame_height / 10 * 7))

        self.left_image = pygame.transform.rotate(self.arrow_image, 180)
        self.up_image = pygame.transform.rotate(self.arrow_image, 90)
        self.down_image = pygame.transform.rotate(self.arrow_image, -90)

    def draw(self, surface, direction):
        if direction == "left":
            self.rect.center = self.left
            self.image = self.left_image
        if direction == "up":
            self.rect.center = self.top
            self.image = self.up_image
        if direction == "down":
            self.rect.center = self.bottom
            self.image = self.down_image
        if direction == "right":
            self.image = self.arrow_image
            self.rect.center = self.right

        surface.blit(self.image, self.rect)


class Goal(pygame.sprite.Sprite):
    def __init__(self, goalType, pos, goal_size):
        super().__init__()

        self.goal_white = pygame.image.load(GoalRes[goalType.WHITE])
        self.goal_green = pygame.image.load(GoalRes[goalType.GREEN])
        self.goal_red = pygame.image.load(GoalRes[goalType.RED])
        self.goal_white = pygame.transform.scale(self.goal_white, goal_size)
        self.goal_green = pygame.transform.scale(self.goal_green, goal_size)
        self.goal_red = pygame.transform.scale(self.goal_red, goal_size)
        self.rect_white = self.goal_white.get_rect()
        self.rect_green = self.goal_green.get_rect()
        self.rect_red = self.goal_red.get_rect()
        self.rect_white.center = pos
        self.rect_green.center = pos
        self.rect_red.center = pos

    def draw_white(self, surface):
        surface.blit(self.goal_white, self.rect_white)

    def draw_green(self, surface):
        surface.blit(self.goal_green, self.rect_green)

    def draw_red(self, surface):
        surface.blit(self.goal_red, self.rect_red)


class Football(pygame.sprite.Sprite):
    def __init__(self, pos, football_size, frame_width, frame_height, goal_size):
        super().__init__()
        self.football_image = pygame.image.load(FOOTBALL_IMG)
        self.football_image = pygame.transform.scale(self.football_image, football_size)
        self.rect = self.football_image.get_rect()
        self.image = self.football_image

        self.right_speed = [frame_width // 300, 0]
        self.left_speed = [-frame_width // 300, 0]
        self.up_speed = [0, -frame_height // 300]
        self.down_speed = [0, frame_height // 300]

        self.frame_width = frame_width
        self.frame_height = frame_height

        self.goal_width, self.goal_height = goal_size

        self.angle = 0
        self.horizontal_angle = frame_width // 250
        self.vertical_angle = frame_height // 200
        self.pos = pos
        self._done_moving = False

    def move(self, direction):
        if (
            (self.rect.left > self.goal_width // 2)
            and (self.rect.right < self.frame_width - self.goal_width // 2)
            and (self.rect.top > self.goal_height // 2)
            and (self.rect.bottom < self.frame_height - self.goal_height // 2)
        ):
            self._done_moving = False
            if direction == "up":
                speed = self.up_speed
                self.angle += self.vertical_angle
            elif direction == "down":
                speed = self.down_speed
                self.angle -= self.vertical_angle
            elif direction == "left":
                speed = self.left_speed
                self.angle += self.horizontal_angle
            elif direction == "right":
                speed = self.right_speed
                self.angle -= self.horizontal_angle

            self.image = pygame.transform.rotate(self.football_image, self.angle)

            self.moved_rect = self.image.get_rect(center=self.rect.center).move(
                speed[0], speed[1]
            )
            self.rect = self.image.get_rect(center=self.moved_rect.center)

        else:
            self._done_moving = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def reset(self, surface):
        self.rect.center = self.pos[0], self.pos[1]
        surface.blit(self.image, self.rect)


class Balloon(pygame.sprite.Sprite):
    def __init__(self, pos, balloon_size, frame_width, frame_height):
        super().__init__()
        self.balloon_image = pygame.image.load(BALLOON_IMG)
        self.balloon_image = pygame.transform.scale(self.balloon_image, balloon_size)
        self.balloon_correct_image = pygame.image.load(BALLOON_CORRECT_IMG)
        self.balloon_wrong_image = pygame.image.load(BALLOON_WRONG_IMG)
        self.rect = self.balloon_image.get_rect()
        self.image = self.balloon_image

        self.frame_width = frame_width
        self.frame_height = frame_height

        self.expansion_rate_go = self.frame_width // 230
        self.expansion_rate_stop = self.frame_width // 700

        self.goal_width, self.goal_height = balloon_size

        self.pos = pos

        self.horizontal_angle = frame_width // 250
        self.vertical_angle = frame_height // 200
        self._done_moving = False
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def move(self, direction):
        ballon_w, ballon_h = self.image.get_size()

        if direction == "go":
            ballon_w_new, ballon_h_new = (
                ballon_w + self.expansion_rate_go,
                ballon_h + self.expansion_rate_go,
            )
            if (ballon_w_new < self.frame_width * 0.85) and (
                ballon_h_new < self.frame_height * 0.85
            ):
                self._done_moving = False
                self.image = pygame.transform.scale(
                    self.balloon_image, (ballon_w_new, ballon_h_new)
                )
                self.rect = self.image.get_rect(center=self.pos)
            else:
                self._done_moving = True
        elif direction == "stop":
            ballon_w_new, ballon_h_new = (
                ballon_w - self.expansion_rate_stop,
                ballon_h - self.expansion_rate_stop,
            )
            if (ballon_w_new > self.frame_width * 0.25) and (
                ballon_h_new > self.frame_height * 0.25
            ):
                self._done_moving = False
                self.image = pygame.transform.scale(
                    self.balloon_image, (ballon_w_new, ballon_h_new)
                )
                self.rect = self.image.get_rect(center=self.pos)
            else:
                self._done_moving = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def draw_correct(self, surface):
        self.correct_image = pygame.transform.scale(
            self.balloon_correct_image, self.image.get_size()
        )
        surface.blit(self.correct_image, self.rect)

    def draw_wrong(self, surface):
        self.wrong_image = pygame.transform.scale(
            self.balloon_wrong_image, self.image.get_size()
        )
        surface.blit(self.wrong_image, self.rect)

    def reset(self, surface):
        self.image = self.balloon_image
        self.rect = self.balloon_image.get_rect()
        self.rect.center = self.pos
        surface.blit(self.image, self.rect)
