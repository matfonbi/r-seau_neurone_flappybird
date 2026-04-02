import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import pygame
except ImportError:
    print("Erreur : pygame n'est pas installé. Lancez : pip install pygame")
    sys.exit(1)

import math
import random
from config import *
from game_engine import Bird, Pipe, get_difficulty


def draw_background(surface):
    for y in range(SCREEN_HEIGHT - GROUND_HEIGHT):
        t = y / (SCREEN_HEIGHT - GROUND_HEIGHT)
        r = int(COLOR_SKY_TOP[0] + (COLOR_SKY_BOTTOM[0] - COLOR_SKY_TOP[0]) * t)
        g = int(COLOR_SKY_TOP[1] + (COLOR_SKY_BOTTOM[1] - COLOR_SKY_TOP[1]) * t)
        b = int(COLOR_SKY_TOP[2] + (COLOR_SKY_BOTTOM[2] - COLOR_SKY_TOP[2]) * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))


def draw_ground(surface):
    ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
    pygame.draw.rect(surface, COLOR_GROUND, (0, ground_y, SCREEN_WIDTH, GROUND_HEIGHT))
    pygame.draw.rect(surface, COLOR_GROUND_TOP, (0, ground_y, SCREEN_WIDTH, 6))


def draw_pipe(surface, pipe):
    tx, ty, tw, th = pipe.get_top_rect()
    bx, by, bw, bh = pipe.get_bottom_rect()

    # Corps
    pygame.draw.rect(surface, COLOR_PIPE, (tx, ty, tw, th))
    pygame.draw.rect(surface, COLOR_PIPE, (bx, by, bw, bh))

    # Rebords (chapeau du tuyau)
    cap_w = tw + 10
    cap_h = 18
    cap_x = tx - 5
    pygame.draw.rect(surface, COLOR_PIPE, (cap_x, th - cap_h, cap_w, cap_h))
    pygame.draw.rect(surface, COLOR_PIPE, (cap_x, by, cap_w, cap_h))

    # Ombrage
    pygame.draw.rect(surface, COLOR_PIPE_DARK, (tx, ty, 8, th))
    pygame.draw.rect(surface, COLOR_PIPE_DARK, (bx, by, 8, bh))
    pygame.draw.rect(surface, COLOR_PIPE_DARK, (cap_x, th - cap_h, 8, cap_h))
    pygame.draw.rect(surface, COLOR_PIPE_DARK, (cap_x, by, 8, cap_h))


def draw_bird(surface, bird):
    cx = int(bird.x)
    cy = int(bird.y)
    r = BIRD_RADIUS

    # Corps principal
    pygame.draw.circle(surface, COLOR_BIRD, (cx, cy), r)

    # Ventre légèrement plus clair
    pygame.draw.circle(surface, (255, 235, 100), (cx + 3, cy + 4), r - 6)

    # Oeil
    eye_x = cx + int(r * 0.45)
    eye_y = cy - int(r * 0.25)
    pygame.draw.circle(surface, COLOR_WHITE, (eye_x, eye_y), 5)
    pygame.draw.circle(surface, COLOR_BIRD_EYE, (eye_x + 1, eye_y), 3)

    # Bec
    bec_x = cx + r - 2
    bec_y = cy + 2
    pts = [(bec_x, bec_y - 3), (bec_x + 9, bec_y), (bec_x, bec_y + 3)]
    pygame.draw.polygon(surface, (255, 140, 0), pts)


def draw_score(surface, font_big, font_small, score, high_score):
    # Score principal
    score_surf = font_big.render(str(score), True, COLOR_WHITE)
    shadow_surf = font_big.render(str(score), True, COLOR_DARK_GREY)
    sx = SCREEN_WIDTH // 2 - score_surf.get_width() // 2
    surface.blit(shadow_surf, (sx + 2, 22))
    surface.blit(score_surf, (sx, 20))

    # Meilleur score
    hs_text = font_small.render(f"Meilleur : {high_score}", True, COLOR_WHITE)
    surface.blit(hs_text, (SCREEN_WIDTH // 2 - hs_text.get_width() // 2, 70))


def draw_game_over(surface, font_big, font_small, score, high_score):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    surface.blit(overlay, (0, 0))

    go_surf = font_big.render("GAME OVER", True, (255, 80, 80))
    surface.blit(go_surf, (SCREEN_WIDTH // 2 - go_surf.get_width() // 2, 220))

    sc_surf = font_small.render(f"Score : {score}", True, COLOR_WHITE)
    surface.blit(sc_surf, (SCREEN_WIDTH // 2 - sc_surf.get_width() // 2, 300))

    hs_surf = font_small.render(f"Meilleur : {high_score}", True, (255, 215, 0))
    surface.blit(hs_surf, (SCREEN_WIDTH // 2 - hs_surf.get_width() // 2, 340))

    restart_surf = font_small.render("ESPACE pour rejouer", True, COLOR_WHITE)
    surface.blit(restart_surf, (SCREEN_WIDTH // 2 - restart_surf.get_width() // 2, 400))


def draw_start_screen(surface, font_big, font_small):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    surface.blit(overlay, (0, 0))

    title = font_big.render("FLAPPY BIRD", True, (255, 215, 0))
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))

    prompt = font_small.render("Appuyez sur ESPACE pour commencer", True, COLOR_WHITE)
    surface.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 320))


def reset_game():
    bird = Bird()
    pipes = []
    score = 0
    pipe_speed, gap, spawn_interval = get_difficulty(0)
    ms_since_pipe = 0.0

    # Premier tuyau
    margin = 110
    gap_y = random.randint(margin, SCREEN_HEIGHT - GROUND_HEIGHT - margin)
    pipes.append(Pipe(SCREEN_WIDTH + 10, gap_y, gap))

    return bird, pipes, score, pipe_speed, gap, spawn_interval, ms_since_pipe


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("Arial", 52, bold=True)
    font_small = pygame.font.SysFont("Arial", 28)

    # Pré-rendu du fond (coûteux à faire chaque frame)
    bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    draw_background(bg_surface)
    draw_ground(bg_surface)

    bird, pipes, score, pipe_speed, gap, spawn_interval, ms_since_pipe = reset_game()
    high_score = 0

    STATE_START = "start"
    STATE_PLAY = "play"
    STATE_DEAD = "dead"
    state = STATE_START

    ms_per_frame = 1000.0 / FPS

    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE:
                    if state == STATE_START:
                        state = STATE_PLAY
                    elif state == STATE_PLAY:
                        bird.jump()
                    elif state == STATE_DEAD:
                        bird, pipes, score, pipe_speed, gap, spawn_interval, ms_since_pipe = reset_game()
                        state = STATE_PLAY

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == STATE_PLAY:
                    bird.jump()

        if state == STATE_PLAY:
            bird.update()

            ms_since_pipe += ms_per_frame
            if ms_since_pipe >= spawn_interval:
                ms_since_pipe = 0.0
                margin = 110
                gap_y = random.randint(margin, SCREEN_HEIGHT - GROUND_HEIGHT - margin)
                pipes.append(Pipe(SCREEN_WIDTH + 10, gap_y, gap))

            for pipe in pipes:
                pipe.update(pipe_speed)
                if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                    pipe.passed = True
                    score += 1
                    if score > high_score:
                        high_score = score
                    pipe_speed, gap, spawn_interval = get_difficulty(score)

            pipes = [p for p in pipes if not p.is_off_screen()]

            dead = bird.is_out_of_bounds()
            if not dead:
                for pipe in pipes:
                    if pipe.collides_with(bird):
                        dead = True
                        break

            if dead:
                if score > high_score:
                    high_score = score
                state = STATE_DEAD

        # --- Rendu ---
        screen.blit(bg_surface, (0, 0))

        for pipe in pipes:
            draw_pipe(screen, pipe)

        draw_bird(screen, bird)

        if state == STATE_PLAY or state == STATE_DEAD:
            draw_score(screen, font_big, font_small, score, high_score)

        if state == STATE_START:
            draw_start_screen(screen, font_big, font_small)
        elif state == STATE_DEAD:
            draw_game_over(screen, font_big, font_small, score, high_score)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
