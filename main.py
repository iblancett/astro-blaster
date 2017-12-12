import pygame
import numpy as np
import math
import time
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
wndw_size = [400, 600]

class Asteroid():
    def __init__(self, center):
        self.points = [[0,3],
                       [-1,1],
                       [-3,0],
                       [-1,-1],
                       [0,-3],
                       [1,-1],
                       [3,0],
                       [1,1]]
        self.center = center
        self.scale = 3
        self.graph_points = [0]*len(self.points)
        self.color = GREEN
    def grab_points(self):
        for i in range(len(self.points)):
            self.graph_points[i] = [self.points[i][0]*self.scale + self.center[0], self.points[i][1]*self.scale + self.center[1]]
        return self.graph_points

class Cluster():
    def __init__(self):
        self.centers = [[50,50],[100,50],[150,50],[200,50],[250,50],[300,50],[350,50],
                       [75,75],[125,75],[175,75],[225,75],[275,75],[325,75]]
        self.colors = [GREEN for center in self.centers]
        self.astros = [0]*len(self.centers)
        self.directionx = 1
        self.directiony = -1
        self.offsetx = 0
        self.offsety = 0

    def make_astros(self):
        for i, center in enumerate(self.centers):
            self.astros[i] = Asteroid([center[0] + self.offsetx, center[1] + self.offsety]).grab_points()
        if self.astros[0][0][0] < 25 or self.astros[6][0][0] > 375:
            self.directionx = self.directionx*-1
        if self.astros[0][0][1] < 25 or self.astros[0][0][1] > 225:
            self.directiony = self.directiony*-1
        self.offsetx += self.directionx
        self.offsety += self.directiony
        return self.astros


class Laser():
    def __init__(self, ship):
        self.blaster1 = ship.graph_points[16]
        self.blaster2 = ship.graph_points[6]
        self.width = 3.0
        self.length = 7.0
        self.xaxis = ship.xaxis
        self.yaxis = ship.yaxis
        self.frame = 0
        self.color = RED
        self.graph_points = []
        self.draw_left = True
        self.draw_right = True
    def grab_points(self):
        self.frame += 5
        points1 = [(-self.width/2, -self.length),
                   (-self.width/2, 0),
                   (self.width/2, 0),
                   (self.width/2, -self.length)]
        points2 = [(-self.width/2, -self.length),
                   (-self.width/2, 0),
                   (self.width/2, 0),
                   (self.width/2, -self.length)]
        for i in range(len(points1)):
            x1 = points1[i][0]
            y1 = points1[i][1] - self.frame
            x2 = points2[i][0]
            y2 = points2[i][1] - self.frame
            x_prime1 = x1*self.xaxis[0] + y1*self.yaxis[0]
            y_prime1 = x1*self.xaxis[1] + y1*self.yaxis[1]
            x_prime2 = x2*self.xaxis[0] + y2*self.yaxis[0]
            y_prime2 = x2*self.xaxis[1] + y2*self.yaxis[1]
            points1[i] = [self.blaster1[0] - x_prime1, self.blaster1[1] + y_prime1]
            points2[i] = [self.blaster2[0] - x_prime2, self.blaster2[1] + y_prime2]

        self.graph_points = [points1, points2]
        return [points1, points2]

class Spaceship():
    def __init__(self):
        self.bottom_dist = 50.0
        self.height = 50.0
        self.color = BLUE
        self.xaxis = [1,0]
        self.yaxis = [0,1]
        self.shift = 0
        self.rotation = 0
        self.graph_points = []
    def grab_points(self):
        theta = self.rotation * math.pi/180.0
        wndw_w = wndw_size[0]
        wndw_h = wndw_size[1]
        self.xaxis = [math.cos(theta), -math.sin(theta)]
        self.yaxis = [math.sin(theta), math.cos(theta)]
        points = [[0,8],[-1.5,6],[-1,5],[-2,3],[-1,1],[-3,2],[-4,4],[-5,1],[-4,-1],
                  [-4,-2],[-2,-1],[0,-2],[2,-1],[4,-2],[4,-1],[5,1],[4,4],[3,2],
                  [1,1],[2,3],[1,5],[1.5,6]]

        for i in range(len(points)):
            x = points[i][0]
            y = points[i][1]
            x_prime = x*self.xaxis[0] + y*self.yaxis[0]
            y_prime = x*self.xaxis[1] + y*self.yaxis[1]
            points[i] = [x_prime, y_prime]

        self.graph_points = [0]*len(points)
        for i in range(len(points)):
            self.graph_points[i] = [wndw_w/2 + points[i][0]*self.height/10.0 + self.shift, wndw_h - self.bottom_dist - points[i][1]*self.height/10.0]

        return self.graph_points

class Game():
    def __init__(self):
        self.running = True
        self.screen = None
        self.size = self.width, self.height = wndw_size[0], wndw_size[1]
        self.title = "Astro Blaster"
        self.high_score = 0

    def begin_app(self):
        pygame.init()
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.running = True
        ready = self.draw_menu()
        while not ready:
                ready = self.draw_instructions()
        self.start_game()

    def start_game(self):
        self.running = True
        self.ship = Spaceship()
        self.cluster = Cluster()
        self.astros = self.cluster.make_astros()
        self.astro_rects = []
        self.lasers = []
        self.laser_rects = []
        self.last_shot = 0
        self.score = 0
        self.init_time = time.time()

        self.screen.fill(BLACK)
        pygame.draw.polygon(self.screen, self.ship.color, self.ship.grab_points(), 0)
        for i, astro in enumerate(self.astros):
            self.astro_rects.append(pygame.draw.polygon(self.screen, self.cluster.colors[i], astro, 0))
        pygame.display.flip()
        pygame.key.set_repeat(50, 20)

        while(self.running):
            for event in pygame.event.get():
                self.on_event(event)

        self.draw_ending()


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.ship.rotation -= 2
            if event.key == pygame.K_DOWN:
                self.ship.rotation += 2
            if event.key == pygame.K_RIGHT:
                self.ship.shift += 3
            if event.key == pygame.K_LEFT:
                self.ship.shift -= 3
            if event.key == pygame.K_SPACE and pygame.time.get_ticks() - self.last_shot > 100:
                self.last_shot = pygame.time.get_ticks()
                pygame.time.set_timer(USEREVENT+1, 1)
                pygame.event.post(pygame.event.Event(USEREVENT+1))
                pygame.event.pump()
                self.lasers.append(Laser(self.ship))
                self.lasers[-1].grab_points()
                rect1 = pygame.draw.polygon(self.screen, self.lasers[-1].color, self.lasers[-1].graph_points[0], 0)
                rect2 = pygame.draw.polygon(self.screen, self.lasers[-1].color, self.lasers[-1].graph_points[1], 0)
                self.laser_rects.append([rect1,rect2])
        if event.type == pygame.USEREVENT + 1:
            for laser in self.lasers:
                laser.grab_points()
            self.astros = self.cluster.make_astros()
            for i, astro in enumerate(self.astros):
                self.astro_rects[i] = pygame.draw.polygon(self.screen, self.cluster.colors[i], astro, 0)


        self.screen.fill(BLACK)
        view = self.screen.get_rect()
        pygame.draw.polygon(self.screen, self.ship.color, self.ship.grab_points(), 0)

        for i, astro in enumerate(self.astros):
            pygame.draw.polygon(self.screen, self.cluster.colors[i], astro, 0)

        lasers_hit = []
        if self.lasers:
            for i, laser in enumerate(self.lasers):
                if laser.draw_left:
                    self.laser_rects[i][0] = pygame.draw.polygon(self.screen, laser.color, laser.graph_points[0], 0)
                if laser.draw_right:
                    self.laser_rects[i][1] = pygame.draw.polygon(self.screen, laser.color, laser.graph_points[1], 0)
                if (not view.contains(self.laser_rects[i][0]) and not view.contains(self.laser_rects[i][1])) or (not laser.draw_left or not laser.draw_right):
                    lasers_hit.append(laser)
                for j, rect in enumerate(self.astro_rects):
                    if self.cluster.colors[j] == BLACK:
                        continue
                    laser.draw_left = not rect.contains(self.laser_rects[i][0])
                    laser.draw_right = not rect.contains(self.laser_rects[i][1])
                    if not laser.draw_left or not laser.draw_right:
                        self.score  += 100 - (time.time() - self.init_time)
                        self.cluster.colors[j] = BLACK
                        if all([self.cluster.colors[i] == BLACK for i in range(len(self.astros))]):
                            self.running = False
                        pygame.draw.polygon(self.screen, self.cluster.colors[j], self.astros[j], 0)
            if lasers_hit:
                for laser in lasers_hit:
                    del self.laser_rects[self.lasers.index(laser)]
                    self.lasers.remove(laser)

        pygame.display.flip()

    def draw_menu(self):
        menu_font = pygame.font.SysFont('Magneto', 48, True, False)

        title_text = menu_font.render(self.title, True, RED)
        self.screen.blit(title_text, [(self.width - title_text.get_width()) // 2, (self.height - title_text.get_height()) // 2 - 200])

        play_text = menu_font.render("Play", True, RED)
        play_button = self.screen.blit(play_text, [(self.width - play_text.get_width()) // 2, (self.height - play_text.get_height()) // 2])

        howto_text = menu_font.render("Instructions", True, RED)
        howto_button = self.screen.blit(howto_text, [(self.width - howto_text.get_width()) // 2, (self.height - howto_text.get_height()) // 2 + 100])

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if play_button.collidepoint(pos):
                        return True

                    if howto_button.collidepoint(pos):
                        return False

    def draw_instructions(self):

        self.screen.fill(BLACK)
        menu_font = pygame.font.SysFont('Magneto', 48, True, False)
        title_text = menu_font.render("Instructions", True, BLUE)
        howto_font = pygame.font.SysFont('Agency FB', 24, True, False)
        howto_text1 = howto_font.render('Your goal is to save our universe!  No pressure...', True, GREEN)
        howto_text2 = howto_font.render('Right Arrow: Move ship right', True, GREEN)
        howto_text3 = howto_font.render('Left Arrow: Move ship left', True, GREEN)
        howto_text4 = howto_font.render('Up Arrow: Turn ship counterclockwise', True, GREEN)
        howto_text5 = howto_font.render('Down Arrow: Turn ship clockwise', True, GREEN)
        howto_text6 = howto_font.render('Spacebar: Astro blast those invaders!', True, GREEN)
        self.screen.blit(title_text, [(self.width - title_text.get_width()) // 2, (self.height - title_text.get_height()) // 2 - 200])
        self.screen.blit(howto_text1, [(self.width - howto_text1.get_width()) // 2, (self.height - howto_text1.get_height()) // 2 - 125])
        self.screen.blit(howto_text2, [(self.width - howto_text2.get_width()) // 2, (self.height - howto_text2.get_height()) // 2 - 75])
        self.screen.blit(howto_text3, [(self.width - howto_text3.get_width()) // 2, (self.height - howto_text3.get_height()) // 2 - 25])
        self.screen.blit(howto_text4, [(self.width - howto_text4.get_width()) // 2, (self.height - howto_text4.get_height()) // 2 + 25])
        self.screen.blit(howto_text5, [(self.width - howto_text5.get_width()) // 2, (self.height - howto_text5.get_height()) // 2 + 75])
        self.screen.blit(howto_text6, [(self.width - howto_text6.get_width()) // 2, (self.height - howto_text6.get_height()) // 2 + 125])
        play_text = menu_font.render("Play", True, RED)
        play_button = self.screen.blit(play_text, [(self.width - play_text.get_width()) // 2, (self.height - play_text.get_height()) // 2 + 200])

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if play_button.collidepoint(pos):
                        return True
                if event.type == pygame.QUIT:
                    pygame.quit()

    def draw_ending(self):
        self.screen.fill(BLACK)
        title_font = pygame.font.SysFont('Magneto', 48, True, False)
        title_text = title_font.render("GAME OVER", True, RED)
        details_font = pygame.font.SysFont('Agency FB', 24, True, False)
        details_text1 = details_font.render('Thank you for saving our universe!', True, BLUE)
        details_text2 = details_font.render('You scored %d points.' % self.score, True, BLUE)
        if self.high_score and self.high_score < self.score:
            details_text3 = details_font.render('You beat your high score: %d points.' % self.high_score, True, BLUE)
            self.high_score = self.score
        elif not self.high_score:
            details_text3 = details_font.render('Play again to beat your score!', True, BLUE)
            self.high_score = self.score
        else:
            details_text3 = details_font.render('Try to beat your high score: %d points.' % self.high_score, True, BLUE)
        play_text = title_font.render("Play Again", True, RED)
        self.screen.blit(title_text, [(self.width - title_text.get_width()) // 2, (self.height - title_text.get_height()) // 2 - 200])
        self.screen.blit(details_text1, [(self.width - details_text1.get_width()) // 2, (self.height - details_text1.get_height()) // 2 - 100])
        self.screen.blit(details_text2, [(self.width - details_text2.get_width()) // 2, (self.height - details_text2.get_height()) // 2])
        self.screen.blit(details_text3, [(self.width - details_text3.get_width()) // 2, (self.height - details_text3.get_height()) // 2 + 100])
        play_button = self.screen.blit(play_text, [(self.width - play_text.get_width()) // 2, (self.height - play_text.get_height()) // 2 + 200])
        pygame.display.flip()

        play_again = False
        while not play_again:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if play_button.collidepoint(pos):
                        play_again = True

        self.start_game()

    def on_cleanup(self):
        pygame.quit()

if __name__ == "__main__" :
    theApp = Game()
    theApp.begin_app()
