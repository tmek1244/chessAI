# https://github.com/suragnair/alpha-zero-general/blob/master/main.py

import logging

import coloredlogs

from Coach import Coach
from Game import Game
from NeuralNet import NeuralNet as nn
from common import *

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.

args = dotdict({
    'numIters': 10,
    'numEps': 10,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 3,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 2,         # Number of games moves for MCTS to simulate.
    'arenaCompare': 4,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('./temp/','best'),
    'numItersForTrainExamplesHistory': 20,
})


def main():
    log.info('Loading %s...', Game.__name__)
    g = Game()

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)

    if args.load_model:
        log.info(f'Loading checkpoint {args.load_folder_file[0]}/{args.load_folder_file[1]}...')
        nnet.load_checkpoint(folder=args.load_folder_file[0], filename=args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()


if __name__ == "__main__":
    main()
