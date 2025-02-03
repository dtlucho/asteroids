import pygame
import random

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        angle = random.uniform(20, 50)
        velocity_1 = self.velocity.rotate(angle)
        velocity_2 = self.velocity.rotate(-angle)
        old_radius = self.radius
        asteroid_1 = Asteroid(self.position.x, self.position.y, old_radius - ASTEROID_MIN_RADIUS)
        asteroid_2 = Asteroid(self.position.x, self.position.y, old_radius - ASTEROID_MIN_RADIUS)
        asteroid_1.velocity = velocity_1 * 1.2
        asteroid_2.velocity = velocity_2 * 1.2
    