import sys
import os
import statistics 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'game'))

from game_engine import FlappyBirdEnv

def naive_action(state):
    bird_above_gap_top = state[3]
    vertical_velocity = state[1]
    if bird_above_gap_top < 0.5 or vertical_velocity < -0.2:
        return 0
    return 1

def stat(score):
    print(f"Valeur Max :{max(score)}\nValeur Min : {min(score)}\nEcart type {statistics.pstdev(score)}")

def run(n_games=100):
    env = FlappyBirdEnv()
    scores = []

    for i in range(n_games):
        state = env.reset()
        done = False
        while not done:
            action = naive_action(state)
            state, reward, done = env.step(action)
        scores.append(env.score)
        print(f"Partie {i + 1} : score = {env.score}")

    print(f"\nScore moyen sur {n_games} parties : {sum(scores) / len(scores):.1f}")
    stat(scores)

if __name__ == '__main__':
    run()

