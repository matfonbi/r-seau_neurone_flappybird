import sys
import os
import neat
import pickle
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'game'))

from main import draw_background, draw_ground
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
    #bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    #draw_background(bg_surface)
    #draw_ground(bg_surface)

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

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    genome, config = load_genome_and_config()
    play(genome, config)