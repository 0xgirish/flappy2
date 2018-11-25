import pygame
import numpy as np

from bird import Bird
from pipes import Pipe


class Flappy:

    def __init__(self, window_size=(380, 600), fps=60):
        pygame.init()

        self.display = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Smart Flappy")
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.window_size = window_size
        self.background = None
        self.bird = None
        self.pipe_image = None
        self.pipes = []
        self.bird_scale = None
        self.score = 0

    def init(self, background, bird_images, pipe_image, bird_scale=(50, 40)):
        self.set_background(background)

        bird_frames = Flappy.get_frames(bird_images, bird_scale)
        self.bird = Bird(bird_frames)
        self.bird_scale = bird_scale

        pipe_image = pygame.image.load(pipe_image)
        self.pipe_image = pipe_image

    def run(self, print_event=False, filename1="zeros1.txt", filename2="ones1.txt", clf=None):
        """
        run Flappy game in classic mode
        """
        file0 = open(filename1, "a")
        file1 = open(filename2, "a")

        crashed = False

        freq_pipe = 120
        is_add = freq_pipe - 40

        data_freq = 20
        is_compl = data_freq

        action = -1

        self.pipes.append(Pipe(self.pipe_image, x=200))

        # action0 = -1
        action1 = -1
        data = ""
        ones = 0

        while not crashed:
            action0 = -1
            data0 = self.get_sample(0, 1, True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

                if event.type == pygame.KEYDOWN:
                    data = self.get_sample(0, 1, True)
                    self.bird.jump()
                    action1 = 1
                    action0 = 1

                if print_event:
                    print(event)

            if is_compl % data_freq == 0 and clf is not None:
                clf_action = self.predict(clf)
                print("action, clf_action = {}, {}".format(action, clf_action))

            if action1 == 1:
                self.collect_data(file1, action1, data)
                action1 = -1

            if is_compl % data_freq == 0:
                if action0 == -1:
                    self.collect_data(file0, action0, data0)
                print("no of zeros = {}\r".format(ones))
                ones += 1
                action = -1

            is_compl = (is_compl + 1) % data_freq

            if is_add % freq_pipe is 0:
                self.pipes.append(Pipe(self.pipe_image))
            is_add = (is_add + 1) % freq_pipe

            self.draw(start=True)

            if self.is_collision():
                crashed = True

        pygame.quit()
        file1.close()
        file0.close()
        print("score = {}".format(self.score))

    def smart_run(self, clf, mean, std):

        crashed = False

        freq_pipe = 120
        is_add = freq_pipe - 40

        # self.pipes.append(Pipe(self.pipe_image, x=0))
        self.pipes.append(Pipe(self.pipe_image, x=200))
        # self.bird.v = -7

        clf_freq = 1
        is_clf = clf_freq
        action = -1

        while not crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

            clf_action = self.predict(clf, mean, std)
            if clf_action == 1:
                action = 1

            if is_clf % clf_freq == 0:
                if action == 1:
                    self.bird.jump()
                    action = -1
            is_clf = (is_clf + 1) % clf_freq
            clf_freq = 10

            if is_add % freq_pipe is 0:
                self.pipes.append(Pipe(self.pipe_image))
            is_add = (is_add + 1) % freq_pipe

            self.draw(True)

            if self.is_collision():
                crashed = True

        pygame.quit()
        print("score = {}".format(self.score))

    def get_sample(self, mean, std, Is=False):
        pipes = []
        for pipe in self.pipes:
            if pipe.x + pipe.width + 10 < self.bird.x:
                continue
            pipes.append(pipe)
        v = self.bird.v
        if len(pipes) >= 1:
            dx, dy = (pipes[0].x - self.bird.x), (self.bird.y - pipes[0].height - 100)
        else:
            dx, dy = 380, self.bird.y - 100

        h = self.window_size[1] - self.bird.y
        sample = "{} {} {} {}".format(v, h, dx, dy)
        if Is:
            return sample
        sample = np.array([float(x) for x in sample.split()]).reshape(1, -1)
        sample = (sample - mean) / std
        return sample

    def predict(self, clf, mean, std):
        sample = self.get_sample(mean, std)
        action_p = clf.predict(sample)[0]
        # print("action = {}".format(action_p))
        return action_p

    def collect_data(self, file, action, data):
        line = "{} {}\n".format(data, action)
        file.write(line)

    def is_collision(self):
        if self.bird.y + self.bird_scale[1] > self.window_size[1]:
            return True

        if self.bird.y < 0:
            return True

        for pipe in self.pipes:
            if pipe.is_touching(self.bird, self.bird_scale):
                return True
        else:
            return False




    def draw(self, start):
        """
        draw background, bird and pipes, update display
        """
        self.display.blit(self.background, (0, 0))
        self.bird.draw(self.display, start)
        self.draw_pipes()

        pygame.display.update()
        self.clock.tick(self.fps)

    def draw_pipes(self):
        """
        draw pipes on the display and remove zombie pipes
        """
        no_of_pipes = len(self.pipes)
        zombie_pipes = []
        for i in range(no_of_pipes):
            if not self.pipes[i].is_seen():
                zombie_pipes.append(i)
                self.score += 1
                continue
            self.pipes[i].draw(self.display)

        for index in zombie_pipes:
            self.pipes.pop(index)

    @staticmethod
    def get_frames(images, scale):
        """
        :param images: bird frame images list
        :param scale: bird image scale
        :return: pygame.Surface list for images
        """
        frames = []
        for image in images:
            frame = pygame.image.load(image)
            frame = pygame.transform.scale(frame, scale)
            frames.append(frame)

        return frames

    def set_background(self, background):
        """
        :param background: background image address
        """
        background = pygame.image.load(background)
        background = pygame.transform.scale(background, self.window_size)
        self.background = background
