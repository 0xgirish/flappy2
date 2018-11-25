import os

from Flappy import Flappy
from model import model


def main():

    clf, mean, std = model("svm")   # decision tree classifier
    print("training completed")
    flappy = Flappy(fps=120, no_of_birds=2)
    bird_images = ["res/img/frame-{}.png".format(i) for i in range(1, 5)]
    pipe_image = "res/img/pipe.png"
    background = "res/img/background.png"

    flappy.init(background, bird_images, pipe_image)
    flappy.smart_run([clf, clf], mean, std)
    # flappy.run(filename1="zeros1.txt", filename2="ones1.txt")


if __name__ == '__main__':
    PATH = os.path.dirname(os.path.abspath(__file__))
    os.chdir(PATH)
    print("In Directory {}".format(PATH))
    main()
