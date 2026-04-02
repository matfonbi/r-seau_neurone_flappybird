import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'game'))

from game_engine import FlappyBirdEnv

class Perceptron:
    def __init__(self, n_inputs=5):
        self.weights = np.random.uniform(-1, 1, n_inputs)
        self.bias = np.random.uniform(-1, 1)

    def forward(self, x):
        z = np.dot(self.weights, x) + self.bias
        # Sigmoïde : ramène la sortie entre 0 et 1
        return np.tanh(z)

    def decide(self, x):
        return 1 if self.forward(x) > 0.5 else 0


def run(n_games=10):
    env = FlappyBirdEnv()
    net = Perceptron()
    scores = []

    for i in range(n_games):
        state = env.reset()
        done = False
        while not done:
            action = net.decide(state)
            state, reward, done = env.step(action)
        scores.append(env.score)
        print(f"Partie {i + 1} : score = {env.score}")

    print(f"\nScore moyen sur {n_games} parties : {sum(scores) / len(scores):.1f}")
    return scores[0], net.weights

if __name__ == '__main__':
    best_score = -1
    best_weight = ()
    best_game = 0
    for numero_game in range(100):
        print(f"Game n°{numero_game}")
        score_game, weight = run(1)
        print(f"score_game = {score_game}")
        if score_game > best_score:
            best_score = score_game
            best_weight = weight
            best_game = numero_game
    print(f"Le meilleur score est : {best_score}, avec les poids suivant : {best_weight} pendant la game {best_game}")