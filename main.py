import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Just Type")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 74)

# Game variables
score = 0
target_key = chr(random.randint(97, 122))  # Random lowercase letter

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text('Just Type', font, BLACK, screen, 20, 20)
        draw_text('Press 1 for Single Player', font, BLACK, screen, 20, 100)
        draw_text('Press 2 for Two Players', font, BLACK, screen, 20, 200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    single_player()
                elif event.key == pygame.K_2:
                    # Implement two player mode
                    pass

        pygame.display.update()

def single_player():
    global score, target_key
    while True:
        screen.fill(WHITE)
        draw_text(f'Score: {score}', font, BLACK, screen, 20, 20)
        
        # Random color and position for the target key
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        x = random.randint(0, WIDTH - 100)
        y = random.randint(0, HEIGHT - 100)
        draw_text(f'Type: {target_key}', font, random_color, screen, x, y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode == target_key:
                    score += 1
                else:
                    score -= 5
                target_key = chr(random.randint(97, 122))  # New random letter
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
