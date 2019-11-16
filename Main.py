import sys
from time import time
from random import randint

import pygame

from DynamicObjects import Circle
from Vec2 import Vec2

class Game:
    def __init__(self):
        pygame.init()
        self.Screen = pygame.display.set_mode((1200, 600))
        self.ScreenRect = self.Screen.get_rect()
        pygame.display.set_caption("School")

        self.Font = pygame.sysfont.SysFont(None, 48)

        self.Backgrounds = (
            (0, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
        )

        self.BackgroundIndex = 0

        # This will be hard-coded until the map creator is made:
        self.Points = ((77, 552), (131, 170), (386, 270), (487, 83), (640, 321), (742, 529), (478, 481), (1108, 28), (1100, 251), (971, 412))


        self.Circles = []
        for x in range(10):
            self.Circles.append(Circle(Vec2(self.Points[x]), randint(10, 50), Vec2(0, 0), 400, (255, 255, 255), self.Screen, self.ScreenRect))
            self.Circles[-1].ClampToScreen()

        self.SelectedCircle = None

        self.fStartingTime = time()

        fFrameElapsedCounter = 0
        nFrameCounter = 0
        self.FPS = 0
        while True:
            fOld = self.fStartingTime
            self.fStartingTime = time()
            self.fElapsedTime = self.fStartingTime - fOld
            fFrameElapsedCounter += self.fElapsedTime
            nFrameCounter += 1

            try:
                self.FPS = round(1 / self.fElapsedTime)
            except ZeroDivisionError:
                self.FPS = self.FPS

            self.MousePos = Vec2(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.KeydownEvents(event)
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    self.MouseEvents(event)

            Collided = False
            for circle in self.Circles:
                if circle is not self.SelectedCircle and self.SelectedCircle is not None:
                    if circle.CheckCircleCollision(self.SelectedCircle):
                        self.SelectedCircle.Color = self.SelectedCircle.CollisionColor
                        circle.Color = circle.CollisionColor
                        Collided = True
                    else:
                        circle.Color = circle.InitColor

            if self.SelectedCircle is not None:
                self.SelectedCircle.Update(self.fElapsedTime, self.MousePos)
                self.SelectedCircle.ClampToScreen()

                if Collided:
                    self.SelectedCircle.Color = self.SelectedCircle.CollisionColor
                else:
                    self.SelectedCircle.Color = self.SelectedCircle.SelectedColor

            self.Screen.fill(self.Backgrounds[self.BackgroundIndex])

            for circle in self.Circles:
                if circle is not self.SelectedCircle or self.SelectedCircle is None:
                    circle.Draw()

            if self.SelectedCircle is not None:
                self.SelectedCircle.Draw()

            self.Screen.blit(pygame.font.Font.render(self.Font, str(self.FPS), True, (255, 255, 255)), (0, 0))
            pygame.display.flip()

    def KeydownEvents(self, event):
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.key == pygame.K_1:
            self.BackgroundIndex += 1

            if self.BackgroundIndex >= len(self.Backgrounds):
                self.BackgroundIndex = 0

        if event.key == pygame.K_2:
            self.BackgroundIndex -= 1

            if self.BackgroundIndex < 0:
                self.BackgroundIndex = len(self.Backgrounds) - 1

    def MouseEvents(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for circle in self.Circles:
                if circle.CollidePoint(self.MousePos):
                    if self.SelectedCircle is not None:
                        self.SelectedCircle.Deselect()
                        if circle is self.SelectedCircle:
                            self.SelectedCircle.Deselect()
                            self.SelectedCircle = None
                        else:
                            self.SelectedCircle = circle
                            self.SelectedCircle.Select()
                    else:
                        self.SelectedCircle = circle
                        self.SelectedCircle.Select()

Game()
