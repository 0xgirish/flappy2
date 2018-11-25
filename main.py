import os
import argparse
import pickle

from Flappy import Flappy
from model import get_model


def get_arguments():
    parser = argparse.ArgumentParser(description='provide model by command line flags --model')
    parser.add_argument("--model", type=str)
    args = parser.parse_args()
    return args.model


def main():
    game = Flappy()
    game.init()
    model_name = get_arguments()
    if model_name.upper() == "GAN":
        neural_list = get_model(model_name)
        best_neural = game.smart_run(neural_list)
        with open("model/gan.model", "wb") as f:
            pickle.dump(best_neural, f)


if __name__ == '__main__':
    PATH = os.path.dirname(os.path.abspath(__file__))
    os.chdir(PATH)
    print("In Directory {}".format(PATH))
    main()
