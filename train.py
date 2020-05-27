import os
import glob
import argparse
import pickle
from tqdm import tqdm
import IPython
from shutil import copyfile
import gym
import textworld.gym
from textworld import EnvInfos
from time import time
import pandas as pd
import numpy as np
import sys
import yaml
from utils import make_path

# from dalab.grid_search.grid_search import GridSearcher
from utils import get_points
from custom_agent import CustomAgent


class Environment:
    """
    Wrapper for the TextWorld Environment.
    """
    def __init__(self, games_dir, max_nb_steps=100, batch_size=1):
        self.games = self.get_games(games_dir)
        self.max_nb_steps = max_nb_steps
        self.batch_size = batch_size
        self.env = self.setup_env()

    def step(self, commands):
        return self.env.step(commands)

    def reset(self):
        return self.env.reset()

    def render(self):
        return self.env.render()

    def manual_game(self):
        try:
            done = False
            self.env.reset()
            nb_moves = 0
            while not done:
                self.env.render()
                command = input("Input ")
                nb_moves += 1
                obs, scores, dones, infos = self.env.step([command])

            self.env.render()  # Final message.
        except KeyboardInterrupt:
            pass  # Quit the game.

        print("Played {} steps, scoring {} points.".format(nb_moves, scores[0]))

    def setup_env(self):
        requested_infos = self.select_additional_infos()
        env_id = textworld.gym.register_games(self.games, requested_infos,
                                              max_episode_steps=self.max_nb_steps,
                                              name="training")
        env_id = textworld.gym.make_batch(env_id, batch_size=self.batch_size, parallel=True)
        return gym.make(env_id)

    def get_games(self, games_dir):
        games = []
        for game in [games_dir]:
            if os.path.isdir(game):
                games += glob.glob(os.path.join(game, "*.ulx"))
            else:
                games.append(game)
        games = [os.path.join(os.getcwd(), game) for game in games]
        print("{} games found for training.".format(len(games)))
        return games

    def select_additional_infos(self) -> EnvInfos:
        request_infos = EnvInfos()
        request_infos.description = True
        request_infos.inventory = True
        request_infos.entities = True
        request_infos.verbs = True
        request_infos.extras = ["recipe", "walkthrough"]
        request_infos.admissible_commands = True

        return request_infos


class Trainer:
    def __init__(self, game_dir):
        self.agent = CustomAgent(verbose=True)
        self.env = Environment(game_dir)

    def train(self):
        self.start_time = time()

        games_id = {'/home/swasti/Documents/sem6/NLP/Modifications/FirstTextWorldProblems/./train_games/tw-cooking-recipe2+take2+cut+open-BnYEixa9iJKmFZxO.ulx': 0, '/home/swasti/Documents/sem6/NLP/Modifications/FirstTextWorldProblems/./train_games/tw-cooking-recipe1+take1-11Oeig8bSVdGSp78.ulx': 1}

        for epoch_no in range(1, self.agent.nb_epochs + 1):
            print('Epoch {}'.format(epoch_no))
            accuracy = 0.0
            for game_no in range(len(self.env.games)):
                obs, infos = self.env.reset()
                idx = games_id[self.env.games[game_no]]
                self.agent.train(idx)

                scores = [0] * len(obs)
                dones = [False] * len(obs)
                steps = [0] * len(obs)
                while not all(dones):
                    # Increase step counts.
                    steps = [step + int(not done) for step, done in zip(steps, dones)]
                    commands = self.agent.act(obs, scores, dones, infos)
                    # if epoch_no == 1 or epoch_no == 25 or epoch_no == 50:
                    #     print(commands)
                    obs, scores, dones, infos = self.env.step(commands)

                # Let the agent know the game is done.
                self.agent.act(obs, scores, dones, infos)
                score = sum(scores) / self.agent.batch_size

                score, possible_points, percentage = get_points(score, infos['extra.walkthrough'][0])
                print('Score for game {}: {}/{}'.format(game_no+1, score, possible_points))
                accuracy += percentage
                with open("./results/rewards_with_e.txt",'a',encoding = 'utf-8') as f:
                    reward_str = "Env_id: " + str(idx) + " Score: " + str(score) + "/" + str(possible_points) + "\n" 
                    f.write(reward_str)

            print('Accuracy {}'.format(accuracy/len(self.env.games)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train an agent.")
    parser.add_argument('--games', action='store', type=str, help='Directory of the games used for training.')
    args = parser.parse_args()

    Trainer(args.games).train()

    # env = Environment("./train_games/")
    # env.setup_env()














































