import pygame
import sys
from bird import Bird
from pipe import Pipe

pygame.init()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
FPS = 60
GROUND_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Create clock object to control frame rate
clock = pygame.time.Clock()

# Create bird and pipes objects
bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
pipes = []

def main():
    global bird, pipes

    pygame.time.wait(1000)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Bird update and draw
        bird.update()
        bird.draw(screen)

        # Pipe generation and update
        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe(SCREEN_WIDTH, SCREEN_HEIGHT))
        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x > -pipe.PIPE_WIDTH]

        # Draw ground
        pygame.draw.rect(screen, (0, 255, 0), (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

        # Check for collisions with pipes or ground
        for pipe in pipes:
            if bird.collides(pipe):
                # Game Over
                pygame.quit()
                sys.exit()

        if bird.y > SCREEN_HEIGHT - GROUND_HEIGHT:
            # Bird hit the ground
            pygame.quit()
            sys.exit()

        # Update display
        pygame.display.flip()

        # Control frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    print("Starting Flappy Bird Game")
    main()
    print("Game Loop Exited")
    # Add a delay before exiting the program
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()
