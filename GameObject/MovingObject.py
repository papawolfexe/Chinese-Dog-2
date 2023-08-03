import math
import pygame
from .ObjectVars import MoveDirections as MoveDirs


class MovingObject:
    def __init__(
            self,
            game_window: pygame.Surface,
            image_path, pos: tuple[float, float],
            use_scalar: bool,
            size: tuple[float, float] | float,
            default_speed: float,
            center_positioning: bool = False
    ) -> None:

        if use_scalar:
            if type(size) == tuple:
                raise ValueError('Cant use tuple when using scalars for size')

        self.game_window = game_window
        self.image_path = image_path
        self.pos = pos
        self.size = size
        self.default_speed = default_speed
        self.center_positioning = center_positioning

        self.img = pygame.image.load(self.image_path).convert_alpha()

        self.rect = self.img.get_rect()

        if use_scalar:
            self.rect = self.rect.scale_by(self.size)
            self.img = pygame.transform.scale_by(self.img, self.size)
        else:
            self.rect.size = self.size
            self.img = pygame.transform.scale(self.img, self.rect.size)

        if not self.center_positioning:
            self.rect.topleft = self.pos
        else:
            self.rect.center = self.pos

        self.game_window.blit(self.img, self.rect.topleft)

    def draw(self):
        self.game_window.blit(self.img, self.rect.topleft)

    def move(self, direction: MoveDirs, speed: int = None, boundaries=(True, True, True, True)) -> None:
        """
        Move character in specified direction
        :param direction: Movement direction of object
        :param speed: specific speed of movement, uses default class if value not passed
        :param boundaries: Which screen boundaries to collide with, \
        formatted as tuple of bools for up, down, right, left boundaries respectively
        :return:
        """
        if speed is None:
            speed = self.default_speed

        if direction == MoveDirs.up:
            self.rect.move_ip(0, -1 * speed)
            if boundaries[0] and self.rect.top < 0:
                self.rect.top = 0

        elif direction == MoveDirs.down:
            self.rect.move_ip(0, 1 * speed)
            if boundaries[1] and self.rect.bottom > self.game_window.get_height():
                self.rect.bottom = self.game_window.get_height()

        elif direction == MoveDirs.left:
            self.rect.move_ip(-1 * speed, 0)
            if boundaries[2] and self.rect.left < 0:
                self.rect.left = 0

        elif direction == MoveDirs.right:
            self.rect.move_ip(1 * speed, 0)
            if boundaries[3] and self.rect.right > self.game_window.get_width():
                self.rect.right = self.game_window.get_width()

    def move_at_angle(self, angle, speed: float) -> None:
        """
        Move in the direction of the given angle and speed
        :param angle: angle of movement in degrees
        :param speed: speed of movement
        """
        angle = math.radians(angle)

        x = speed * math.cos(angle)
        y = speed * math.sin(angle)

        self.rect = self.rect.move(x, -y)

    def collides_with_mouse(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def check_for_bounce(self, angle: int) -> int:
        if (self.rect.top < 0) or (self.rect.bottom > self.game_window.get_height()):
            return 360 - angle
        elif (self.rect.left < 0) or (self.rect.right > self.game_window.get_width()):
            return 180 - angle
        else:
            return angle
