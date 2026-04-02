import sys
import os
import neat
import pickle
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'game'))

'''from main import *'''
from game_engine import FlappyBirdEnv
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

GENOME_PATH = os.path.join(os.path.dirname(__file__), 'best_genome.pkl')
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'neat_config.txt')


def load_genome_and_config():
    with open(GENOME_PATH, 'rb') as f:
        genome = pickle.load(f)
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        CONFIG_PATH
    )
    return genome, config


def play(genome, config):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird - IA')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('monospace', 20)

    net = neat.nn.FeedForwardNetwork.create(genome, config)
    env = FlappyBirdEnv(render=True, screen=screen)
    #env = FlappyBirdEnv()
    '''bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    draw_background(bg_surface)
    draw_ground(bg_surface)
    bird, pipes, score, pipe_speed, gap, spawn_interval, ms_since_pipe = reset_game()
    STATE_START = "start"
    STATE_PLAY = "play"
    STATE_DEAD = "dead"
    state = STATE_START'''

    running = True
    while running:
        state = env.reset()
        done = False
        frames = 0
        

        while not done and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            output = net.activate(state)
            action = 1 if output[0] > 0.5 else 0
            state, reward, done = env.step(action)
            frames += 1

            overlay_lines = [
                f'Score : {env.score}',
                f'Frames : {frames}',
                f'Sortie reseau : {output[0]:.3f}',
            ]
            for i, line in enumerate(overlay_lines):
                surf = font.render(line, True, (255, 255, 255))
                screen.blit(surf, (10, 10 + i * 24))
            
            '''if state == STATE_PLAY:
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
                draw_game_over(screen, font_big, font_small, score, high_score)'''


            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    genome, config = load_genome_and_config()
    play(genome, config)