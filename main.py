import pygame
import neat
import os
import Bird
import Pipe
pygame.font.init()

WIDTH, HEIGHT = 600, 800

birdImgs = [pygame.transform.scale2x(pygame.image.load("images/bird1.png")),
            pygame.transform.scale2x(pygame.image.load("images/bird2.png")),
            pygame.transform.scale2x(pygame.image.load("images/bird3.png"))]

pipeImg = pygame.transform.scale2x(pygame.image.load("images/pipe.png"))
bg = pygame.transform.scale(pygame.image.load("images/bg.png"), (600, 800))
baseImg = pygame.transform.scale2x(pygame.image.load("images/base.png"))

statFont = pygame.font.SysFont("arial", 50)


def drawWindow(win, birds, pipes, base, score):
    win.blit(bg, (0, 0))
    for pipe in pipes:
        pipe.draw(win)

    text = statFont.render(f"Score: {score}", 1, 'white')
    win.blit(text, (WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)

    pygame.display.update()


def main(genomes, config):
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird.Bird(birdImgs, 230, 350))
        g.fitness = 0
        ge.append(g)

    base = Pipe.Base(baseImg, 700)
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pipes = [Pipe.Pipe(600, pipeImg)]

    score = 0
    run = True
    pipeInd = 0

    while run:


        clock.tick(70)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[pipeInd].x + pipes[pipeInd].pipeTop.get_width():
                pipeInd += 1
        else:
            run = False
            break

        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1

            output = nets[i].activate((bird.y, abs(bird.y - pipes[pipeInd].height),
                                       abs(bird.y - pipes[pipeInd].bottom)))

            if output[0] > 0.5:
                bird.jump()

        rem = []
        addPipe = False
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[i].fitness -= 1
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    addPipe = True
            if (pipe.x + pipe.pipeTop.get_width() < 0):
                rem.append(pipe)

            pipe.move()

        if addPipe:
            score += 1
            pipes.append(Pipe.Pipe(600, pipeImg))

            for g in ge:
                g.fitness += 5

        #for r in rem:
            #pipes.remove(r)
            #pipeInd -= 1

        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        base.move()
        drawWindow(win, birds, pipes, base, score)


def run(configPath):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 500)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    localDir = os.path.dirname(__file__)
    configPath = os.path.join(localDir, 'config.txt')
    run(configPath)
