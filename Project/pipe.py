import pygame
import random

class Pipe:
    def __init__(self, screen_width, screen_height):
        self.PIPE_WIDTH = 80
        self.PIPE_GAP = 200
        self.x = screen_width
        self.top_height = random.randint(50, screen_height - self.PIPE_GAP - 50)
        self.bottom_height = screen_height - self.top_height - self.PIPE_GAP
        self.pipe_top = pygame.Rect(self.x, 0, self.PIPE_WIDTH, self.top_height)
        self.pipe_bottom = pygame.Rect(self.x, screen_height - self.bottom_height, self.PIPE_WIDTH, self.bottom_height)

    def update(self):
        self.x -= 5

    def draw(self, screen):
        print("Drawing Pipe")
        pygame.draw.rect(screen, (0, 0, 255), self.pipe_top)
        pygame.draw.rect(screen, (0, 0, 255), self.pipe_bottom)