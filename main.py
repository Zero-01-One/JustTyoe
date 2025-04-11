import pygame
import random
import sys
import time
import os

pygame.init()


WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Just Type")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font_path = "Sahel-Black.ttf"
font = pygame.font.Font(font_path, 74)
score = 0
target_key = chr(random.randint(97, 122))

music_path = "epic-battle-153400.mp3"
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


#in ghesmat ra az gpt komak gereftam bedalil inke khodam nemidanestam

def draw_gradient(surface, color1, color2):
    for y in range(HEIGHT):
        r = color1[0] + (color2[0] - color1[0]) * y // HEIGHT
        g = color1[1] + (color2[1] - color1[1]) * y // HEIGHT
        b = color1[2] + (color2[2] - color1[2]) * y // HEIGHT
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

def save_scores(mode, player1, score1, player2=None, score2=None):
    with open("scores.txt", "a") as file:
        if mode == "single":
            file.write(f"Single Player - {player1}: {score1}\n")
        elif mode == "two":
            file.write(f"Two Players - {player1}: {score1}, {player2}: {score2}\n")

def end_screen(player1, score1, player2=None, score2=None):
    while True:
        screen.fill(WHITE)
        draw_text("Game Over!", font, BLACK, screen, 20, 20)
        draw_text(f"{player1}: {score1}", font, BLACK, screen, 20, 200)
        if player2:
            draw_text(f"{player2}: {score2}", font, BLACK, screen, 20, 300)
        draw_text("Press Q to Quit", font, BLACK, screen, 20, 500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def main_menu():
    
    while True:
        draw_gradient(screen, (255, 200, 200), (200, 200, 255))
        draw_text('Just Type', font, BLACK, screen, 20, 20)
        draw_text('Press 1 for Single Player', font, BLACK, screen, 20, 200)
        draw_text('Press 2 for Two Players', font, BLACK, screen, 20, 300)
        draw_text('Press L for Leaderboard', font, BLACK, screen, 20, 400)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player1 = input("Enter your name: ")
                    single_player(player1)
                elif event.key == pygame.K_2:
                    player1 = input("Enter Player 1 name: ")
                    player2 = input("Enter Player 2 name: ")
                    two_players(player1, player2)
                elif event.key == pygame.K_l:
                    show_leaderboard()

        pygame.display.update()

def single_player(player1):
    global score, target_key

    x, y = random.randint(0, WIDTH - 100), random.randint(100, HEIGHT - 100)
    velocity_x, velocity_y = 3, 3

    start_time = time.time()
    score = 0
    reaction_start_time = time.time()
    effect_color = None
    effect_text = None
    effect_timer = 0

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > 60:
            save_scores("single", player1, score)
            end_screen(player1, score)

        draw_gradient(screen, (255, 200, 200), (200, 200, 255))
        draw_text(f'Score: {score}', font, BLACK, screen, 20, 20)

        x += velocity_x
        y += velocity_y

        if x <= 0 or x >= WIDTH - 300:
            velocity_x = -velocity_x
        if y <= 100 or y >= HEIGHT - 100:
            velocity_y = -velocity_y

        draw_text(f'Type: {target_key}', font, BLACK, screen, x, y)


        if effect_color and time.time() - effect_timer < 1:
            draw_text(effect_text, font, effect_color, screen, 20, 100)
        else:
            effect_color = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                reaction_time = time.time() - reaction_start_time
                if event.unicode == target_key:
                    if reaction_time <= 1:
                        score += 3
                        effect_color = (0, 255, 0)  
                        effect_text = "+3"
                    elif reaction_time <= 2:
                        score += 2
                        effect_color = (255, 255, 0)  
                        effect_text = "+2"
                    elif reaction_time <= 3:
                        score += 1
                        effect_color = (255, 0, 0)  
                        effect_text = "+1"
                    else:
                        score += 0
                        effect_color = None
                    effect_timer = time.time()
                else:
                    score -= 5
                    effect_color = None
                target_key = chr(random.randint(97, 122))
                reaction_start_time = time.time()

        pygame.display.update()
        pygame.time.delay(30)

def two_players(player1, player2):
    score1, score2 = 0, 0
    x1, y1 = random.randint(0, WIDTH - 200), random.randint(100, HEIGHT - 100)
    x2, y2 = random.randint(0, WIDTH - 200), random.randint(100, HEIGHT - 100)
    velocity_x1, velocity_y1 = 3, 3
    velocity_x2, velocity_y2 = -3, -3

    target_key1 = chr(random.randint(97, 109))
    target_key2 = chr(random.randint(110, 122))

    start_time = time.time()
    reaction_start_time1 = time.time()
    reaction_start_time2 = time.time()
    effect_color1 = None
    effect_text1 = None
    effect_timer1 = 0
    effect_color2 = None
    effect_text2 = None
    effect_timer2 = 0

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > 60:
            save_scores("two", player1, score1, player2, score2)
            end_screen(player1, score1, player2, score2)

        screen.fill(WHITE)
        draw_gradient(screen, (200, 255, 200), (200, 200, 255))

        draw_text(f'{player1} Score: {score1}', font, BLACK, screen, 20, 20)
        draw_text(f'{player2} Score: {score2}', font, BLACK, screen, 20, 180)

        x1 += velocity_x1
        y1 += velocity_y1
        x2 += velocity_x2
        y2 += velocity_y2

        if x1 <= 0 or x1 >= WIDTH - 300:
            velocity_x1 = -velocity_x1
        if y1 <= 100 or y1 >= HEIGHT - 100:
            velocity_y1 = -velocity_y1

        if x2 <= 0 or x2 >= WIDTH - 300:
            velocity_x2 = -velocity_x2
        if y2 <= 100 or y2 >= HEIGHT - 100:
            velocity_y2 = -velocity_y2

        draw_text(f'P1: {target_key1}', font, BLACK, screen, x1, y1)
        draw_text(f'P2: {target_key2}', font, BLACK, screen, x2, y2)


        if effect_color1 and time.time() - effect_timer1 < 1:
            draw_text(effect_text1, font, effect_color1, screen, 20, 100)
        else:
            effect_color1 = None

        if effect_color2 and time.time() - effect_timer2 < 1:
            draw_text(effect_text2, font, effect_color2, screen, 20, 260)
        else:
            effect_color2 = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                reaction_time1 = time.time() - reaction_start_time1
                reaction_time2 = time.time() - reaction_start_time2
                if event.unicode == target_key1:
                    if reaction_time1 <= 1:
                        score1 += 3
                        effect_color1 = (0, 255, 0)  
                        effect_text1 = "+3"
                    elif reaction_time1 <= 2:
                        score1 += 2
                        effect_color1 = (255, 255, 0)  
                        effect_text1 = "+2"
                    elif reaction_time1 <= 3:
                        score1 += 1
                        effect_color1 = (255, 0, 0)  
                        effect_text1 = "+1"
                    else:
                        score1 += 0
                        effect_color1 = None
                    effect_timer1 = time.time()
                    target_key1 = chr(random.randint(97, 109))
                    reaction_start_time1 = time.time()
                elif event.unicode == target_key2:
                    if reaction_time2 <= 1:
                        score2 += 3
                        effect_color2 = (0, 255, 0)  
                        effect_text2 = "+3"
                    elif reaction_time2 <= 2:
                        score2 += 2
                        effect_color2 = (255, 255, 0)
                        effect_text2 = "+2"
                    elif reaction_time2 <= 3:
                        score2 += 1
                        effect_color2 = (255, 0, 0)
                        effect_text2 = "+1"
                    else:
                        score2 += 0
                        effect_color2 = None
                    effect_timer2 = time.time()
                    target_key2 = chr(random.randint(110, 122))
                    reaction_start_time2 = time.time()

        pygame.display.update()
        pygame.time.delay(30)


        
def load_scores():
    if not os.path.exists("scores.txt"):
        return []
    with open("scores.txt", "r") as file:
        scores = []
        for line in file:
            parts = line.split(":")
            if len(parts) == 2:
                name = parts[0].strip()
                score = int(parts[1].strip())
                scores.append((name, score))
        scores.sort(key=sort_by_score, reverse=True)
        return scores[:5]

def sort_by_score(score_entry):
    return score_entry[1]

def show_leaderboard():
    while True:
        screen.fill(WHITE)
        draw_text("Leaderboard", font, BLACK, screen, 20, 20)
        top_scores = load_scores()
        y_offset = 100
        for i, (name, score) in enumerate(top_scores):
            draw_text(f"{i + 1}. {name}: {score}", font, BLACK, screen, 20, y_offset)
            y_offset += 100

        draw_text("Press Q to go back", font, BLACK, screen, 20, y_offset + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return

        pygame.display.update()

def save_scores(mode, player1, score1, player2=None, score2=None):

    scores = load_scores()
    with open("scores.txt", "a") as file:
        if mode == "single":
            file.write(f"{player1}: {score1}\n")
            scores.append((player1, score1))
        elif mode == "two":
            file.write(f"{player1}: {score1}\n")
            file.write(f"{player2}: {score2}\n")
            scores.append((player1, score1))
            scores.append((player2, score2))
    scores.sort(key=sort_by_score, reverse=True)
    with open("scores.txt", "w") as file:
        for name, score in scores[:5]:
            file.write(f"{name}: {score}\n")



if __name__ == "__main__":
    main_menu()

















