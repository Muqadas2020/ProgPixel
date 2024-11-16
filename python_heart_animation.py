import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Heart Animation")

# Colors
BACKGROUND_COLOR = (30, 30, 30)
HEART_COLOR = (255, 0, 127)

# Heart settings
heart_size = 15  # Initial size of the heart
animation_speed = 0.02  # Speed of the "pulsing" effect

# Function to draw a heart shape
def draw_heart(x, y, size):
    points = []
    for angle in range(360):
        angle_rad = math.radians(angle)
        x_offset = size * (16 * math.sin(angle_rad) ** 3)
        y_offset = size * (13 * math.cos(angle_rad) - 5 * math.cos(2 * angle_rad) -
                           2 * math.cos(3 * angle_rad) - math.cos(4 * angle_rad))
        points.append((x + x_offset, y - y_offset))
    pygame.draw.polygon(screen, HEART_COLOR, points)

# Main animation loop
clock = pygame.time.Clock()
scale = 1  # Pulsing scale factor

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Background
    screen.fill(BACKGROUND_COLOR)

    # Calculate the current scale factor for the pulsating effect
    scale = 1 + 0.2 * math.sin(pygame.time.get_ticks() * animation_speed)

    # Draw the heart with the current scale
    draw_heart(WIDTH // 2, HEIGHT // 2, heart_size * scale)

    # Update the screen and set the frame rate
    pygame.display.flip()
    clock.tick(60)
