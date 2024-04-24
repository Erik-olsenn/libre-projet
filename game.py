import pygame
import neat
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 700

JOUEUR_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "penguin1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("images", "penguin2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("images", "penguin3.png")))]
OBSTACLE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "sand.png")))
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "space.png")))
SETT = ["gap", "velocity"]
DEFAULT = "210,5"

STAT_FONT = pygame.font.Font("fonts/ARCADECLASSIC.ttf", 50)

if os.path.isfile(os.path.join("configs", "settings.txt")):
    fichier = open("configs/settings.txt", "r")
    setting = fichier.read().split(",")
    settings = {}
    for i in range(len(setting)):
        settings[SETT[i]] = setting[i]
    fichier.close()
    SETTINGS = settings
else:
    fichier = open("configs/settings.txt", "w+")
    fichier.write(DEFAULT)
    settings = {}
    for i in range(len(DEFAULT)):
        settings[SETT[i]] = DEFAULT[i]
    fichier.close()
    SETTINGS = settings
    


class Joueur:
    IMGS = JOUEUR_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2
        
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
class Obstacle:
    GAP = 210
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.OBSTACLE_TOP = pygame.transform.flip(OBSTACLE_IMG, False, True)
        self.OBSTACLE_BOTTOM = OBSTACLE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 380)
        self.top = self.height - self.OBSTACLE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.OBSTACLE_TOP, (self.x, self.top))
        win.blit(self.OBSTACLE_BOTTOM, (self.x, self.bottom))

    def collision(self, joueur):
        joueur_mask = joueur.get_mask()
        top_mask = pygame.mask.from_surface(self.OBSTACLE_TOP)
        bottom_mask = pygame.mask.from_surface(self.OBSTACLE_BOTTOM)

        top_offset = (self.x - joueur.x, self.top - round(joueur.y))
        bottom_offset = (self.x - joueur.x, self.bottom - round(joueur.y))

        b_point = joueur_mask.overlap(bottom_mask, bottom_offset)
        t_point = joueur_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        return False
    
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        
    
def draw_window(win, joueurs, obstacles, base, score):
    win.blit(BACKGROUND_IMG, (0, 0))

    for obstacle in obstacles:
        obstacle.draw(win)

    text = STAT_FONT.render("Score " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)

    for joueur in joueurs:
        joueur.draw(win)

    pygame.display.update()


def main(genomes, config):
    nets = []
    genom = []
    joueurs = []

    for _, ge in genomes:
        net = neat.nn.FeedForwardNetwork.create(ge, config)
        nets.append(net)
        joueurs.append(Joueur(230, 350))
        ge.fitness = 0
        genom.append(ge)

    base = Base(730)
    obstacles = [Obstacle(730)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        obstacle_ind = 0
        if len(joueurs) > 0:
            if len(obstacles) > 1 and joueurs[0].x > obstacles[0].x + obstacles[0].OBSTACLE_TOP.get_width():
                obstacle_ind = 1
        else:
            run = False
            break

        for joueur in list(joueurs):
            joueur.move()
            genom[joueurs.index(joueur)].fitness += 0.075

            output = nets[joueurs.index(joueur)].activate((joueur.y, abs(joueur.y - obstacles[obstacle_ind].height), abs(joueur.y - obstacles[obstacle_ind].bottom)))

            if output[0] > 0.5:
                joueur.jump()

        add_obstacle = False
        rem = []        
        for obstacle in obstacles:
            for joueur in list(joueurs):
                if obstacle.collision(joueur):
                    genom[joueurs.index(joueur)].fitness -= 1
                    nets.pop(joueurs.index(joueur))
                    genom.pop(joueurs.index(joueur))
                    joueurs.remove(joueur)

                if not obstacle.passed and obstacle.x < joueur.x:
                    obstacle.passed = True
                    add_obstacle = True

            if obstacle.x + obstacle.OBSTACLE_TOP.get_width() < 0:
                rem.append(obstacle)

            obstacle.move()

        if add_obstacle:
            score += 1
            for g in genom:
                g.fitness += 3.5
            obstacles.append(Obstacle(700))

        for r in rem:
            obstacles.remove(r)

        for joueur in list(joueurs):
            if joueur.y + joueur.img.get_height() >= 730 or joueur.y < 0:
                nets.pop(joueurs.index(joueur))
                genom.pop(joueurs.index(joueur))
                joueurs.remove(joueur)

        base.move()

        draw_window(win, joueurs, obstacles, base, score)




def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, 
                                neat.DefaultStagnation, 
                                config_path)
    
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "configs/config-neet.txt")
    run(config_path)