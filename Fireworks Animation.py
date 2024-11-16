import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Fireworks")

# Colors
BLACK = (0, 0, 0)
COLORS = [(255, 50, 50), (255, 140, 0), (255, 255, 50), (50, 255, 50), (50, 200, 255), (50, 50, 255), (238, 130, 238)]

# Particle settings
GRAVITY = 0.05

class Particle:
    def __init__(self, x, y, color, speed, angle, size):
        self.x = x
        self.y = y
        self.color = color
        self.radius = size
        self.speed = speed
        self.angle = angle
        self.alpha = 255  # Transparency of the particle
        self.trail = []  # For creating trail effect

    def update(self):
        # Add current position to trail with fading effect
        if self.alpha > 50:  # Only add to trail while particle is still visible
            self.trail.append((self.x, self.y, self.alpha))

        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed + GRAVITY
        self.speed *= 0.97  # Gradual slowdown
        self.alpha -= 3     # Fade out the particle
        self.alpha = max(self.alpha, 0)

        # Limit trail length
        if len(self.trail) > 10:
            self.trail.pop(0)

    def draw(self):
        # Draw the trail with gradually reducing brightness
        for (trail_x, trail_y, trail_alpha) in self.trail:
            color_with_alpha = (*self.color, trail_alpha)
            pygame.draw.circle(screen, color_with_alpha, (int(trail_x), int(trail_y)), self.radius // 2)

        # Draw the main particle
        color_with_alpha = (*self.color, self.alpha)
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, color_with_alpha, (self.radius, self.radius), self.radius)
        screen.blit(surface, (self.x - self.radius, self.y - self.radius))


class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = HEIGHT  # Start from the bottom of the screen
        self.colors = random.choices(COLORS, k=3)  # Use multiple colors for a single firework
        self.particles = []
        self.exploded = False
        self.timer = random.randint(50, 80)  # Random delay for explosion

    def launch(self):
        if self.y > self.timer:
            self.y -= 5  # Move up
            pygame.draw.circle(screen, random.choice(self.colors), (self.x, int(self.y)), 4)
        else:
            self.explode()

    def explode(self):
        if not self.exploded:
            for _ in range(100):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 6)
                size = random.randint(3, 6)
                color = random.choice(self.colors)
                self.particles.append(Particle(self.x, self.y, color, speed, angle, size))
            self.exploded = True

    def update_and_draw(self):
        if not self.exploded:
            self.launch()
        else:
            for particle in self.particles[:]:
                particle.update()
                if particle.alpha > 0:
                    particle.draw()
                else:
                    self.particles.remove(particle)

    def is_finished(self):
        return self.exploded and len(self.particles) == 0


# Main loop
clock = pygame.time.Clock()
fireworks = []

running = True
while running:
    screen.fill(BLACK)

    # Create new fireworks at random intervals
    if random.randint(1, 50) == 1:
        x = random.randint(100, WIDTH - 100)
        y = random.randint(HEIGHT // 2, HEIGHT - 100)
        fireworks.append(Firework(x, y))

    # Update and draw fireworks
    for firework in fireworks[:]:
        firework.update_and_draw()
        if firework.is_finished():
            fireworks.remove(firework)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
