import math

import pygame

from simpleros import Node
from simpleros.msg.geometry_msg import Twist

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (69, 86, 255)


class Spaceship:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.theta = -math.pi / 2  # Pointing up
        self.lin_vel = 0.0
        self.ang_vel = 0.0

        self.original_image = pygame.image.load(
            "examples/spaceship.png"
        ).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 42))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, dt):
        # Update orientation
        self.theta += self.ang_vel * dt
        # Update position
        self.x += self.lin_vel * math.cos(self.theta) * dt
        self.y += self.lin_vel * math.sin(self.theta) * dt

        # Screen wrapping logic
        if self.x > SCREEN_WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = SCREEN_WIDTH
        if self.y > SCREEN_HEIGHT:
            self.y = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT

    def draw(self, screen):
        # Rotate the original image to avoid quality degradation over time.
        angle_deg = -math.degrees(self.theta) - 90
        self.image = pygame.transform.rotate(self.original_image, angle_deg)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Draw the image (blit)
        screen.blit(self.image, self.rect)


class SpaceshipSimNode:
    def __init__(self, node: Node):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("SpaceshipSim")
        self.clock = pygame.time.Clock()
        self.spaceship = Spaceship()

        self.node = node
        self.node.create_subscriber("cmd_vel", Twist, self.cmd_vel_callback)

    def cmd_vel_callback(self, msg: Twist):
        self.spaceship.lin_vel = msg.linear.x * 100  # Scale for better visuals
        self.spaceship.ang_vel = msg.angular.z

    def run(self):
        try:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False

                dt = self.clock.tick(60) / 1000.0  # seconds
                self.spaceship.update(dt)
                self.screen.fill(BACKGROUND_COLOR)
                self.spaceship.draw(self.screen)
                pygame.display.flip()

        except KeyboardInterrupt:
            pygame.quit()


def main():
    with Node("spaceshipsim_node") as node:
        sim = SpaceshipSimNode(node)
        sim.run()


if __name__ == "__main__":
    main()
