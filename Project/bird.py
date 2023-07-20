import pygame

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 1
        self.lift = -15
        self.bird_img = pygame.image.load("bird.png") # Replace with your bird image file
        print("Bird image loaded successfully")

    def update(self):
        # Apply gravity
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self, screen):
        print("Drawing Bird")
        screen.blit(self.bird_img, (self.x, self.y))

    def jump(self):
        self.velocity = self.lift

    def get_rect(self):
        # Return the bounding rectangle of the bird image
        return pygame.Rect(self.x, self.y, self.bird_img.get_width(), self.bird_img.get_height())

    def collides(self, pipe):
        # Check for collision between bird and pipe
        bird_rect = self.get_rect()
        return bird_rect.colliderect(pipe.pipe_top) or bird_rect.colliderect(pipe.pipe_bottom)
