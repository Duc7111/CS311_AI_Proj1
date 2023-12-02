import pygame

# Initialize Pygame
pygame.init()

# Constants
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
BUTTON_MARGIN = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Set up fonts
font = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.enabled = True  # Added an "enabled" attribute

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY if self.enabled else (150, 150, 150), self.rect)  # Gray out disabled buttons
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

def create_buttons():
    buttons = [
        Button(200 - BUTTON_WIDTH // 2, 100, BUTTON_WIDTH, BUTTON_HEIGHT, "Level 1", "level1"),
        Button(200 - BUTTON_WIDTH // 2, 100 + BUTTON_HEIGHT + BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, "Level 2", "level2"),
        Button(200 - BUTTON_WIDTH // 2, 100 + 2 * (BUTTON_HEIGHT + BUTTON_MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT, "Level 3", "level3"),
        Button(200 - BUTTON_WIDTH // 2, 100 + 3 * (BUTTON_HEIGHT + BUTTON_MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT, "Level 4", "level4"),
    ]
    return buttons
